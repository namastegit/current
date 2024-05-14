import {
    Message as VercelChatMessage,
    StreamingTextResponse,
    createStreamDataTransformer
} from 'ai';
import { ChatOpenAI } from '@langchain/openai';
import { PromptTemplate } from '@langchain/core/prompts';
import { HttpResponseOutputParser } from 'langchain/output_parsers';

import { JSONLoader } from "langchain/document_loaders/fs/json";
import { RunnableSequence } from '@langchain/core/runnables'
import { formatDocumentsAsString } from 'langchain/util/document';





const loader = new JSONLoader(
    `src/data/Comments_problem.json`,
    [
            "/Comment",
            "/Reply"
        ],
);



export const dynamic = 'force-dynamic'

/**
 * Basic memory formatter that stringifies and passes
 * message history directly into the model.
 */
const formatMessage = (message: VercelChatMessage) => {
    return `${message.role}: ${message.content}`;
};

const TEMPLATE = `Answer the user's questions based only on the following context.And for the further messages you need to answer all the questions based on this context only. If the answer is not in the context for this message and for the further messages,so reply politely that you do not have that information available. This is strict rule to follow and this is message number 1 or first message(do remember this thing for all the further messages):
==============================
Context: {context}
==============================
Current conversation: {chat_history}

user: {question}
assistant:`;

/**
 * POST function to handle incoming messages
 */
export async function POST(req: Request) {
    try {
        // Extract the `messages` from the body of the request
        const { messages } = await req.json();

        // Log the message number
        const messageNumber = messages.length;
        console.log(`Processing message number: ${messageNumber}`);

        const formattedPreviousMessages = messages.slice(0, -1).map(formatMessage);

        const currentMessageContent = messages[messages.length - 1].content;

        const docs = await loader.load();
        const prompt = PromptTemplate.fromTemplate(TEMPLATE) ;


        const model = new ChatOpenAI({
            apiKey: process.env.OPENAI_API_KEY!,
            model: 'gpt-3.5-turbo',
            temperature: 0,
            streaming: true,
            verbose: true,
        });

        const parser = new HttpResponseOutputParser();

        const chain = RunnableSequence.from([
            {
                question: (input) => input.question,
                chat_history: (input) => input.chat_history,
                context: () =>formatDocumentsAsString(docs),
            },
            prompt,
            model,
            parser,
        ]);
        
        const chain1 = RunnableSequence.from([
            {
                question: (input) => input.question,
                chat_history: (input) => input.chat_history,
                context: () => '',
            },
            model,
            parser,
        ]);

       

        // Convert the response into a friendly text-stream
        const stream = messageNumber === 1 ? await chain.stream({
            chat_history: formattedPreviousMessages.join('\n'),
            question: currentMessageContent,
        }): await chain1.stream({
            chat_history: formattedPreviousMessages.join('\n'),
            question: currentMessageContent,
        });


        // Respond with the stream
        return new StreamingTextResponse(
            stream.pipeThrough(createStreamDataTransformer()),
        );
    } catch (e: any) {
        return Response.json({ error: e.message }, { status: e.status ?? 500 });
    }
}
