// import { NextApiRequest, NextApiResponse } from 'next';
// import { exec } from 'child_process';
// import path from 'path';

// export  async function GET(req: NextApiRequest, res: NextApiResponse) {
//     if (req.method !== 'GET') {
//         res.status(405).end(); // Method Not Allowed
//         return;
//     }

//     const pythonScriptPath = path.join(process.cwd(), 'py2.py');

//     // Use await to ensure the exec function is completed before continuing
//     await new Promise<void>((resolve, reject) => {
//         exec(`python ${pythonScriptPath}`, (error, stdout, stderr) => {
//             if (error) {
//                 console.error(`Error: ${error.message}`);
//                 res.status(500).json({ error: 'Internal Server Error' });
//                 reject(error);
//                 return;
//             }
//             if (stderr) {
//                 console.error(`stderr: ${stderr}`);
//                 res.status(500).json({ error: 'Internal Server Error' });
//                 reject(new Error(stderr));
//                 return;
//             }
//             console.log(`stdout: ${stdout}`);
//             resolve();
//         });
//     }).catch(error => {
//         console.error('Error executing Python script:', error);
//     });
// }

// import { NextApiRequest, NextApiResponse } from 'next';
// import { exec } from 'child_process';
// import path from 'path';


// export async function GET(req: NextApiRequest, res: NextApiResponse) {
//     if (req.method !== 'GET') {
//         return res.status(405).end(); // Method Not Allowed
//     }

//     const pythonScriptPath = path.join(process.cwd(), 'py2.py');
    
//     await new Promise<void>((resolve, reject) => {
//         exec(`python ${pythonScriptPath}`, (error, stdout, stderr) => {
//             if (error) {
//                 console.error(`Error: ${error.message}`);
//                 res.status(500).json({ error: 'Internal Server Error' });
//                 reject(error);
//                 return;
//             }
//             if (stderr) {
//                 console.error(`stderr: ${stderr}`);
//                 res.status(500).json({ error: 'Internal Server Error' });
//                 reject(new Error(stderr));
//                 return;
//             }
//             console.log(`stdout: ${stdout}`);
//             resolve();
//         });
//     }).catch(error => {
//         console.error('Error executing Python script:', error);
//     });

//     // Returning NextResponse.json() directly
//     return res.json({ message: 'Python script execution initiated' });
// }





import { NextApiRequest, NextApiResponse } from 'next';
import { exec } from 'child_process';
import path from 'path';
import { NextResponse } from 'next/server';
import fs from 'fs';


export const dynamic = 'force-dynamic'
export async function POST(req: Request) {
    // Extract the `messages` from the body of the request
    const { messages } = await req.json();
    console.log("HERE IS YOUR INPUT", messages);
  
    // Get the content from the first message object
    const content = messages[0].content;
  
    // Define the path to the .env file
    const envPath = path.join(process.cwd(), '.env.production');
  
    // Write the content to the .env file
    fs.writeFileSync(envPath, `LATEST_URL=${content}`);
  
    return NextResponse.json({ messages });
  }
  

export async function GET(req: NextApiRequest, res: NextApiResponse) {
    if (req.method !== 'GET') {
        return res.status(405).end(); // Method Not Allowed
    }

    const pythonScriptPath = path.join(process.cwd(), 'py2.py');
    
    await new Promise<void>((resolve, reject) => {
        exec(`python ${pythonScriptPath}`, (error, stdout, stderr) => {
            if (error) {
                console.error(`Error: ${error.message}`);
                res.status(500).json({ error: 'Internal Server Error' });
                reject(error);
                return;
            }
            if (stderr) {
                console.error(`stderr: ${stderr}`);
                res.status(500).json({ error: 'Internal Server Error' });
                reject(new Error(stderr));
                return;
            }
            console.log(`stdout: ${stdout}`);
            resolve();
        });
    }).catch(error => {
        console.error('Error executing Python script:', error);
    });

    // Returning NextResponse.json() directly
    return res.json({ message: 'Python script execution initiated' });
}

