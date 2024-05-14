import { NextApiRequest, NextApiResponse } from 'next';
import { ChatOpenAI } from '@langchain/openai';
import { PromptTemplate } from '@langchain/core/prompts';
import { HttpResponseOutputParser } from 'langchain/output_parsers';
import { RunnableSequence } from '@langchain/core/runnables';
import { formatDocumentsAsString } from 'langchain/util/document';
import { JSONLoader } from 'langchain/document_loaders/fs/json';

// Load the entire Comments_Data.json file into memory or cache it when the server starts
const loader = new JSONLoader(
    "src/data/Comments_Data.json",
    [
        // "/Video ID",
        // "/Video Title",
        // "/Video URL",
        // "/View Count",
        // "/Comment Count",
        // "/Channel Title",
        "/Comments/Comment",
        "/Comments/Reply"
    ],
);

// Load the data file and store it in memory
let cachedData: any[] = [];

async function loadData() {
    try {
        cachedData = await loader.load();
    } catch (error) {
        console.error('Error loading data:', error);
        // Handle error loading data
    }
}

// Call loadData function to load data file when the server starts
loadData();

// Define the prompt template for when data is not sent
const TEMPLATE = `Answer the user's questions based only on the following context.And for the further messages you need to answer all the questions based on this context only. If the answer is not in the context for this message and for the further messages,so reply politely that you do not have that information available. This is strict rule to follow  and this is message number 1 or first message(do remember this thing for all the further messages):
==============================
Context: {context}
==============================
Current conversation: {chat_history}

user: {question}
assistant:`;

// Define the prompt template for when data is sent
const DATA_SENT_TEMPLATE = `Answer the user's questions based only on the context provided in the first message and based on the chat history or conversation history or current conversation. If the answer is not in the context for this message and for the further messages, reply politely that you do not have that information available. This is strict rule to follow:
==============================
Current conversation: {chat_history}

user: {question}
assistant:`;

// Define the formatMessage function
const formatMessage = (message: any) => `${message.role}: ${message.content}`;

// Initialize ChatOpenAI model
const model = new ChatOpenAI({
    apiKey: process.env.OPENAI_API_KEY!,
    model: 'gpt-3.5-turbo',
    temperature: 0,
    streaming: true,
    verbose: true,
});

// Initialize output parser
const parser = new HttpResponseOutputParser();

// Construct processing chain for when data is not sent
const chain = RunnableSequence.from([
    {
        question: (input) => input.question,
        chat_history: (input) => input.chat_history,
        context: () => formatDocumentsAsString(cachedData),
    },
    PromptTemplate.fromTemplate(TEMPLATE),
    model,
    parser,
]);

// Construct processing chain for when data is sent
const dataSentChain = RunnableSequence.from([{
    question: (input) => input.question,
        chat_history: (input) => input.chat_history,
},
    PromptTemplate.fromTemplate(DATA_SENT_TEMPLATE),
    model,
    parser,
]);

// Define a variable to track whether the data has been sent or not
let dataSent = false;

// Define the POST handler
 export const POST =async (req: NextApiRequest, res: NextApiResponse) => {
    try {
        // Extract the `messages` from the body of the request
        const { messages } = req.body;

        const formattedPreviousMessages = messages.slice(0, -1).map(formatMessage);
        const currentMessageContent = messages[messages.length - 1].content;

        // Choose the appropriate processing chain based on whether data has been sent
        const currentChain = dataSent ? dataSentChain : chain;

        // Process the message
      // Process the message
const output = await currentChain.invoke({
    chat_history: formattedPreviousMessages.join('\n'),
    question: currentMessageContent,
});


        // Set dataSent to true after sending the data for the first time
        if (!dataSent) {
            dataSent = true;
        }

        // Respond with the output
        res.status(200).json({ output });
    } catch (error) {
        console.error('Error processing request:', error);
        // Handle error processing request
        res.status(500).json({ error: 'Internal server error' });
    }
};




// import { NextApiRequest, NextApiResponse } from 'next';
// import { ChatOpenAI } from '@langchain/openai';
// import { PromptTemplate } from '@langchain/core/prompts';
// import { HttpResponseOutputParser } from 'langchain/output_parsers';
// import { RunnableSequence } from '@langchain/core/runnables';
// import { formatDocumentsAsString } from 'langchain/util/document';
// import { JSONLoader } from 'langchain/document_loaders/fs/json';

// // Load the entire Comments_Data.json file into memory or cache it when the server starts
// const loader = new JSONLoader(
//     "src/data/Comments_Data.json",
//     [
//         // "/Video ID",
//         // "/Video Title",
//         // "/Video URL",
//         // "/View Count",
//         // "/Comment Count",
//         // "/Channel Title",
//         "/Comments/Comment",
//         "/Comments/Reply"
//     ],
// );

// // Load the data file and store it in memory
// let cachedData: any[] = [];

// async function loadData() {
//     try {
//         cachedData = await loader.load();
//     } catch (error) {
//         console.error('Error loading data:', error);
//         // Handle error loading data
//     }
// }

// // Call loadData function to load data file when the server starts
// loadData();

// // Define the prompt template for when data is not sent
// const TEMPLATE = `Answer the user's questions based only on the following context.And for the further messages you need to answer all the questions based on this context only. If the answer is not in the context for this message and for the further messages,so reply politely that you do not have that information available. This is strict rule to follow  and this is message number 1 or first message(do remember this thing for all the further messages):
// ==============================
// Context: {context}
// ==============================
// Current conversation: {chat_history}

// user: {question}
// assistant:`;

// // Define the prompt template for when data is sent
// const DATA_SENT_TEMPLATE = `Answer the user's questions based only on the context provided in the first message and based on the chat history or conversation history or current conversation. If the answer is not in the context for this message and for the further messages, reply politely that you do not have that information available. This is strict rule to follow:
// ==============================
// Current conversation: {chat_history}

// user: {question}
// assistant:`;

// // Define the formatMessage function
// const formatMessage = (message: any) => `${message.role}: ${message.content}`;

// // Initialize ChatOpenAI model
// const model = new ChatOpenAI({
//     apiKey: process.env.OPENAI_API_KEY!,
//     model: 'gpt-3.5-turbo',
//     temperature: 0,
//     streaming: true,
//     verbose: true,
// });

// // Initialize output parser
// const parser = new HttpResponseOutputParser();

// // Construct processing chain for when data is not sent
// const chain = RunnableSequence.from([
//     {
//         question: (input) => input.question,
//         chat_history: (input) => input.chat_history,
//         context: () => formatDocumentsAsString(cachedData),
//     },
//     PromptTemplate.fromTemplate(TEMPLATE),
//     model,
//     parser,
// ]);

// // Construct processing chain for when data is sent
// const dataSentChain = RunnableSequence.from([{
//     question: (input) => input.question,
//         chat_history: (input) => input.chat_history,
// },
//     PromptTemplate.fromTemplate(DATA_SENT_TEMPLATE),
//     model,
//     parser,
// ]);

// // Define a variable to track whether the data has been sent or not
// let dataSent = false;

// // Define the POST handler
// export default async function handlePostRequest(req: NextApiRequest, res: NextApiResponse) {
//     try {
//         // Check if user is authenticated
      
//         // Extract the `messages` from the body of the request
//         const { messages } = req.body;

//         const formattedPreviousMessages = messages.slice(0, -1).map(formatMessage);
//         const currentMessageContent = messages[messages.length - 1].content;

//         // Choose the appropriate processing chain based on whether data has been sent
//         const currentChain = dataSent ? dataSentChain : chain;

//         // Process the message
//         const output = await currentChain.invoke({
//             chat_history: formattedPreviousMessages.join('\n'),
//             question: currentMessageContent,
//         });

//         // Set dataSent to true after sending the data for the first time
//         if (!dataSent) {
//             dataSent = true;
//         }

//         // Respond with the output
//         res.status(200).json({ output });
//     } catch (error) {
//         console.error('Error processing request:', error);
//         // Handle error processing request
//         res.status(500).json({ error: 'Internal server error' });
//     }
// }
