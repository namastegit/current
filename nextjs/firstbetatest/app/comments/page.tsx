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
        page 11
    </div>
};

export default runPythonScript;
