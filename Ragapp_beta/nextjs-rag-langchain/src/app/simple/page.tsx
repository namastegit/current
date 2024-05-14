// // // Your frontend component
// // "use client"
// // import React, { useState } from 'react';
// // import axios from 'axios';

// // const YourComponent = () => {
// //     const [inputData, setInputData] = useState<string | undefined>('button');
// //     const runPythonScript = async () => {
// //         try {
// //             if (!inputData) {
// //                 console.error('Input data is empty');
// //                 return;
// //             }

// //             const response = await axios.get('http://localhost:3000/api',

// //             {
// //                 params: {
// //                     input: inputData // Include input data in the request
// //                 }
// //             }
// //              );
// //             console.log(response.data);
// //         } catch (error) {
// //             console.error('Error:', error);
// //         }
// //     };

// //     const handleChange = (e:any) => {
// //         setInputData(e.target.value);
// //         console.log('Input value:', e.target.value);
// //     };

// //     return (
// //         <div className='flex flex-col space-y-3 justify-center items-center h-screen'>
// //             <input className='border-2 rounded-full' value={inputData} onChange={handleChange}></input>
// //             <button onClick={runPythonScript}>{inputData}</button>
// //         </div>
// //     );
// // };

// // export default YourComponent;


// Your frontend component
// "use client"
// import React, { useState } from 'react';
// import axios from 'axios';


// const YourComponent = () => {
//     const [inputData, setInputData] = useState('');

//     // Function to handle saving the URL to local storage
//     const saveToLocalStorage = (url:any) => {
//         localStorage.setItem('savedUrl', url);
//     };

//     const handleChange = (e:any) => {
//         setInputData(e.target.value);
//     };

//     const handleSubmit = () => {
//         // Save the input data (URL) to local storage
//         saveToLocalStorage(inputData);
        
//         // Perform other actions as needed, such as submitting the form or making API calls
//     };
//     const runPythonScript = async () => {
//         try {
          

//             const response = await axios.get('http://localhost:3000/api'
//              );
//             console.log(response.data);
//         } catch (error) {
//             console.error('Error:', error);
//         }
//     };

   
//     return (
//         <div className='flex flex-col space-y-3 justify-center items-center h-screen'>

// <input className='border-2 rounded-full' value={inputData} onChange={handleChange}></input>
//             <button onClick={handleSubmit}>Save to Local Storage</button>
            
//             <button onClick={runPythonScript}>Submit</button>
//         </div>
//     );
// };


// export default YourComponent;



//
"use client"
import React from 'react';
import axios from 'axios';
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { useChat } from "ai/react"
import { useRef, useEffect } from 'react'


export function Chatting(){
      
    const { messages, input, handleInputChange, handleSubmit, } = useChat({
        api: 'http://localhost:3000/api',
        onError: (e) => {
            console.log(e)
        }
    });
    const chatParent = useRef<HTMLUListElement>(null)

 useEffect(() => {
        const domNode = chatParent.current
        if (domNode) {
            domNode.scrollTop = domNode.scrollHeight
        }
    })




    const runPythonScript = async () => {
        try {
          

            const response = await axios.get('http://localhost:3000/api'
             );
            console.log(response.data);
        } catch (error) {
            console.error('Error:', error);
        }
    };

   
    return (
        <div className='flex flex-col space-y-3 justify-center items-center h-screen'>

<section className="p-4">
                <form onSubmit={handleSubmit} className="flex w-full max-w-3xl mx-auto items-center">
                    <Input className="flex-1 min-h-[40px]" placeholder="Type your question here..." type="text" value={input} onChange={handleInputChange} />
                    <Button className="ml-2" type="submit">
                        Submit
                    </Button> 
                </form>
            </section>
            <section className="container px-0 pb-10  flex-col flex-grow gap-4 mx-auto max-w-3xl hidden opacity-0">
                <ul ref={chatParent} className="h-1 p-4 flex-grow bg-muted/50 rounded-lg overflow-y-auto flex flex-col gap-4">
                    {messages.map((m, index) => (
                        <div key={index}>
                            {m.role === 'user' ? (
                                <li key={m.id} className="flex flex-row">
                                    <div className="rounded-xl p-4 bg-background shadow-md flex">
                                        <p className="text-primary">{m.content}</p>
                                    </div>
                                </li>
                            ) : (
                                <li key={m.id} className="flex flex-row-reverse">
                                    <div className="rounded-xl p-4 bg-background shadow-md flex w-3/4">
                                        <p className="text-primary">{m.content}</p>
                                    </div>
                                </li>
                            )}
                        </div>
                    ))}
                </ul >
            </section>
            <button onClick={runPythonScript}>Submit</button>
        </div>
    );
};


export default Chatting;