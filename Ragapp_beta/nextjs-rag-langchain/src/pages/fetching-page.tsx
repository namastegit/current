// src/pages/fetching-page.tsx

import { useState } from 'react';
import { exec } from 'child_process';
import path from 'path';

const runPythonScript = async () => {
    const pythonScriptPath = path.join(process.cwd(), 'py2.py');

    return new Promise((resolve, reject) => {
        exec(`python ${pythonScriptPath}`, (error, stdout, stderr) => {
            if (error) {
                console.error(`Error: ${error.message}`);
                reject(error);
                return;
            }
            if (stderr) {
                console.error(`stderr: ${stderr}`);
                reject(new Error(stderr));
                return;
            }
            console.log(`stdout: ${stdout}`);
            resolve(stdout);
        });
    });
};

const FetchingPage = ({ message }: any) => {
    const [output, setOutput] = useState('');

    const handleClick = async () => {
        try {
            const stdout = await runPythonScript();
            setOutput(stdout);
        } catch (error: Error) { // Explicitly define the type of 'error' as 'Error'
            setOutput(`Failed to run Python script: ${error.message}`);
        }
    };
    

    return (
        <div>
            <p>{message}</p>
            <button onClick={handleClick}>Run Python Script</button>
            <p>Output: {output}</p>
        </div>
    );
};

export default FetchingPage;
