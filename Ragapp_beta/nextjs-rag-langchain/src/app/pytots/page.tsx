import { exec } from 'child_process';
import path from 'path';

const runTypeScriptScript = () => {
    const typeScriptScriptPath = path.join(__dirname, 'lib', 'pytots.js');

    exec(`node ${typeScriptScriptPath}`, (error, stdout, stderr) => {
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

    return (
        <div>
            page 11
        </div>
    );
};

export default runTypeScriptScript;
