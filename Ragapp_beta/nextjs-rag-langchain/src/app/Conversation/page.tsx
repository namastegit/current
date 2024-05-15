

'use client'
import { ChangeEvent, useState, useEffect } from 'react';
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { useChat } from "ai/react"
import { useRef } from 'react'


// Custom Radio Button Component
function RadioButton({ id, value, checked, onChange, children }: any) {
    return (
        <div className="flex items-center space-x-2">
            <input
                type="radio"
                id={id}
                value={value}
                checked={checked}
                onChange={onChange}
            />
            <label htmlFor={id}>{children}</label>
        </div>
    );
}

const getApiEndpoint = (option: string) => {
    switch (option) {
        case 'option-one':
            return 'api/ex7';
        case 'option-two':
            return 'api/ex8';
        case 'option-three':
            return 'api/ex9';
        default:
            return 'api/ex7';
    }
};

// Chat Component
export default function Chat() {
    const [selectedOption, setSelectedOption] = useState(() => {
        // Retrieve the selected option from localStorage, if available
        const storedOption = localStorage.getItem('selectedOption');
        return storedOption || 'option-one'; // Default to 'option-one' if no value is stored
    });

    const { messages, input, handleInputChange, handleSubmit } = useChat({
        api: getApiEndpoint(selectedOption),
        onError: (e) => {
            console.log(e)
        }
    });

    const handleRadioChange = (event: ChangeEvent<HTMLInputElement>) => {
        const { value } = event.target;
        setSelectedOption(value);
    };

    const chatParent = useRef<HTMLUListElement>(null);

    useEffect(() => {
        // Store the selected option in localStorage
        localStorage.setItem('selectedOption', selectedOption);
    }, [selectedOption]); // Trigger the effect whenever selectedOption changes

    useEffect(() => {
        const domNode = chatParent.current;
        if (domNode) {
            domNode.scrollTop = domNode.scrollHeight;
        }
    });

    return (
        <main className="flex flex-col w-full h-screen max-h-dvh bg-background">
            <header className="p-4 border-b w-full max-w-3xl mx-auto">
                <h1 className=" text-2xl md:text-4xl font-sans font-bold  text-blue-500"> Discussion Chamber</h1>
            </header>
            <div className="flex  md:mx-20 lg:mx-72 p-4 items-center space-x-2">
                <RadioButton
                    id="option-one"
                    value="option-one"
                    checked={selectedOption === 'option-one'}
                    onChange={handleRadioChange}
                >
                    All
                </RadioButton>
                <RadioButton
                    id="option-two"
                    value="option-two"
                    checked={selectedOption === 'option-two'}
                    onChange={handleRadioChange}
                >
                    Problems
                </RadioButton>
                <RadioButton
                    id="option-three"
                    value="option-three"
                    checked={selectedOption === 'option-three'}
                    onChange={handleRadioChange}
                >
                    Questions
                </RadioButton>
            </div>

            <section className="p-4">
                <form onSubmit={handleSubmit} className="flex w-full max-w-3xl mx-auto items-center">
                    <Input className="flex-1 min-h-[40px]" placeholder="Type your question here..." type="text" value={input} onChange={handleInputChange} />
                    <Button className="ml-2" type="submit">
                        Submit
                    </Button>
                </form>
            </section>
            <section className="container px-0 pb-10 flex flex-col flex-grow gap-4 mx-auto max-w-3xl">
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
                </ul>
            </section>
        </main>
    );
}













// 'use client'
// import { ChangeEvent } from 'react';
// import { Input } from "@/components/ui/input"
// import { Button } from "@/components/ui/button"
// import { useChat } from "ai/react"
// import { useRef, useEffect, useState } from 'react'
//   import { Label } from "@/components/ui/label"
// import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group"


// export function Chat() {

//     const [selectedOption, setSelectedOption] = useState('');


//     const { messages, input, handleInputChange, handleSubmit, } = useChat({
//         api: 'api/ex7',
//         onError: (e) => {
//             console.log(e)
//         }
//     });
//     const handleRadioChange = (event: ChangeEvent<HTMLInputElement>) => {
//         const { value } = event.target;
//         setSelectedOption(value);
//     };

//     const chatParent = useRef<HTMLUListElement>(null)

//     useEffect(() => {
//         const domNode = chatParent.current
//         if (domNode) {
//             domNode.scrollTop = domNode.scrollHeight
//         }
//     })
    

//     return (
//         <main className="flex flex-col w-full h-screen max-h-dvh bg-background">

//             <header className="p-4 border-b w-full max-w-3xl mx-auto">
//                 <h1 className="text-2xl font-bold">LangChain Chat</h1>
//             </header>
//             <RadioGroup onChange={handleRadioChange} defaultValue="option-one" className="flex p-4">
//   <div className="flex items-center space-x-2">
//     <RadioGroupItem value="option-one" id="option-one" />
//     <Label htmlFor="option-one">All</Label>
//   </div>
//   <div className="flex items-center space-x-2">
//     <RadioGroupItem value="option-two" id="option-two" />
//     <Label htmlFor="option-two">Problems</Label>
//   </div>
//   <div className="flex items-center space-x-2">
//     <RadioGroupItem value="option-three" id="option-three" />
//     <Label htmlFor="option-two">Questions</Label>
//   </div>
  
// </RadioGroup>
//             <section className="p-4">
//                 <form onSubmit={handleSubmit} className="flex w-full max-w-3xl mx-auto items-center">
//                     <Input className="flex-1 min-h-[40px]" placeholder="Type your question here..." type="text" value={input} onChange={handleInputChange} />
//                     <Button className="ml-2" type="submit">
//                         Submit
//                     </Button>
                  



 

                    
//                 </form>
//             </section>

//             <section className="container px-0 pb-10 flex flex-col flex-grow gap-4 mx-auto max-w-3xl">
//                 <ul ref={chatParent} className="h-1 p-4 flex-grow bg-muted/50 rounded-lg overflow-y-auto flex flex-col gap-4">
//                     {messages.map((m, index) => (
//                         <div key={index}>
//                             {m.role === 'user' ? (
//                                 <li key={m.id} className="flex flex-row">
//                                     <div className="rounded-xl p-4 bg-background shadow-md flex">
//                                         <p className="text-primary">{m.content}</p>
//                                     </div>
//                                 </li>
//                             ) : (
//                                 <li key={m.id} className="flex flex-row-reverse">
//                                     <div className="rounded-xl p-4 bg-background shadow-md flex w-3/4">
//                                         <p className="text-primary">{m.content}</p>
//                                     </div>
//                                 </li>
//                             )}
//                         </div>
//                     ))}
//                 </ul >
//             </section>
//         </main>
//     )
// }
// 'use client'
// import { ChangeEvent, useState } from 'react';
// import { Input } from "@/components/ui/input"
// import { Button } from "@/components/ui/button"
// import { useChat } from "ai/react"
// import { useRef, useEffect } from 'react'
// import { Label } from "@/components/ui/label"
// import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group"

// // Declare the getApiEndpoint function before using it
// const getApiEndpoint = (option: string) => {
//     switch (option) {
//         case 'option-one':
//             return 'api/ex7';
//         case 'option-two':
//             return 'api/ex8';
//         case 'option-three':
//             return 'api/ex9';
//         default:
//             return 'api/ex7';
//     }
// };

// export function Chat() {
//     const [selectedOption, setSelectedOption] = useState('');

//     const { messages, input, handleInputChange, handleSubmit } = useChat({
//         api: getApiEndpoint(selectedOption),
//         onError: (e) => {
//             console.log(e)
//         }
//     });

//     const handleRadioChange = (event: ChangeEvent<HTMLInputElement>) => {
//         const { value } = event.target;
//         setSelectedOption(value);
//     };
    

//     const chatParent = useRef<HTMLUListElement>(null);

//     useEffect(() => {
//         const domNode = chatParent.current;
//         if (domNode) {
//             domNode.scrollTop = domNode.scrollHeight;
//         }
//     });

//     return (
//         <main className="flex flex-col w-full h-screen max-h-dvh bg-background">
//             <header className="p-4 border-b w-full max-w-3xl mx-auto">
//                 <h1 className="text-2xl font-bold">{selectedOption}</h1>
//             </header>
//             <RadioGroup onChange={handleRadioChange} defaultValue={selectedOption} className="flex p-4">
//                 <div className="flex items-center space-x-2">
//                     <RadioGroupItem value="option-one" id="option-one" />
//                     <Label htmlFor="option-one">All</Label>
//                 </div>
//                 <div className="flex items-center space-x-2">
//                     <RadioGroupItem value="option-two" id="option-two" />
//                     <Label htmlFor="option-two">Problems</Label>
//                 </div>
//                 <div className="flex items-center space-x-2">
//                     <RadioGroupItem value="option-three" id="option-three" />
//                     <Label htmlFor="option-two">Questions</Label>
//                 </div>
//             </RadioGroup>
//             <section className="p-4">
//                 <form onSubmit={handleSubmit} className="flex w-full max-w-3xl mx-auto items-center">
//                     <Input className="flex-1 min-h-[40px]" placeholder="Type your question here..." type="text" value={input} onChange={handleInputChange} />
//                     <Button className="ml-2" type="submit">
//                         Submit
//                     </Button>
//                 </form>
//             </section>
//             <section className="container px-0 pb-10 flex flex-col flex-grow gap-4 mx-auto max-w-3xl">
//                 <ul ref={chatParent} className="h-1 p-4 flex-grow bg-muted/50 rounded-lg overflow-y-auto flex flex-col gap-4">
//                     {messages.map((m, index) => (
//                         <div key={index}>
//                             {m.role === 'user' ? (
//                                 <li key={m.id} className="flex flex-row">
//                                     <div className="rounded-xl p-4 bg-background shadow-md flex">
//                                         <p className="text-primary">{m.content}</p>
//                                     </div>
//                                 </li>
//                             ) : (
//                                 <li key={m.id} className="flex flex-row-reverse">
//                                     <div className="rounded-xl p-4 bg-background shadow-md flex w-3/4">
//                                         <p className="text-primary">{m.content}</p>
//                                     </div>
//                                 </li>
//                             )}
//                         </div>
//                     ))}
//                 </ul>
//             </section>
//         </main>
//     )
// }
