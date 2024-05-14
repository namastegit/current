// // it's still not the recommended approach for running Python scripts in a Next.js application due to the potential security risks and limitations of client-side JavaScript.

// // To safely run Python scripts in a Next.js application, it's best to use an API route, as demonstrated in the solution provided earlier. This way, the Python script execution happens server-side, where you have more control over security and access to system resources.


import { exec } from 'child_process';
import path from 'path';

const runPythonScript = () => {
    const pythonScriptPath = path.join(process.cwd(), 'fetch_comments.py');

    exec(`python ${pythonScriptPath}`, (error, stdout, stderr) => {
        if (error) {
            console.error(`Error: ${error.message}`);
            return;
        }
        if (stderr) {
            console.error(`stderr: ${stderr}`);
            return;
        }
        console.log(`stdout: ${stdout}`);
    });

    return<div>
        <button  >hello</button>
    </div>
};

export default runPythonScript;


// // https://chat.openai.com/share/398b5e7b-8039-4ab9-bf82-83df1417d5a3
