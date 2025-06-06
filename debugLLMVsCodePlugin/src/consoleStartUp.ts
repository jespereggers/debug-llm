/** 
 * This file is to directly feed inputs to the extension helper 
 * functions from the command line and log the outputs
 * 
 * This file runs independent to the plugin
 */

/**
 * RUM WITH COMMAND: ts-node consoleStartUp.ts
 */
import { helperFunctions } from './extensionsHelper/extensionsHelper';
import { execSync } from 'child_process';
import * as fs from 'fs';
import * as path from 'path';
import { createObjectCsvWriter } from 'csv-writer';


const runFromCommandLine:boolean = true;

async function llmDebugger(code: string): Promise<any> {

    return await helperFunctions.bugFixHelper(runFromCommandLine,llmDebugger);
};

// Function to check for compiler/runtime errors
function checkForErrors(debuggedCode: string, language: string): boolean {
    const filename = `temp_code.${language === 'typescript' ? 'ts' : 'js'}`;
    fs.writeFileSync(filename, debuggedCode);

    try {
        if (language === 'typescript') {
            execSync(`tsc ${filename}`);
        } else {
            execSync(`node ${filename}`);
        }
        return false;
    } catch (error) {
        console.error(`Error during compilation/execution: ${error}`);
        return true;
    } finally {
        if (fs.existsSync(filename)) {
            fs.unlinkSync(filename);
        }
    }
}

// Function to process and evaluate the code files
async function processAndEvaluate(
    llmFunction: (code: string) => Promise<any>,
    inputDirectories: { [key: string]: string },
    outputCsv: string
) {
    const results: any[] = [];

    for (const [directory, language] of Object.entries(inputDirectories)) {
        const files = fs.readdirSync(directory).filter(file => file.endsWith('.js') || file.endsWith('.ts'));
        
        for (const filename of files) {
            const filePath = path.join(directory, filename);
            const code = fs.readFileSync(filePath, 'utf-8');

            const startTime = Date.now();
            console.log(startTime);
            const debuggedCode = await llmFunction(code);
            console.log("debuggedCode: ", debuggedCode);
            const endTime = Date.now();

            const hasErrors = checkForErrors(debuggedCode, language);
            const timeTaken = (endTime - startTime) / 1000;

            results.push({
                filename,
                directory,
                time_taken: timeTaken,
                has_errors: hasErrors
            });

            console.log("RESULTS: ", results)
        }
    }

    // Write results to CSV
    const csvWriter = createObjectCsvWriter({
        path: outputCsv,
        header: [
            { id: 'filename', title: 'Filename' },
            { id: 'directory', title: 'Directory' },
            { id: 'time_taken', title: 'Time Taken (s)' },
            { id: 'has_errors', title: 'Has Errors' }
        ]
    });

    await csvWriter.writeRecords(results);
}

const inputDirectories = {
    "../bugsTestCases/short_bugs": "javascript",
    "../bugsTestCases/medium_bugs": "javascript",
    "../bugsTestCases/long_bugs": "javascript",
};

// Output CSV file path
const outputCsv = "debugger_results.csv";

console.log("HELLO++++++++++++++++++")
// Execute the function
processAndEvaluate(llmDebugger, inputDirectories, outputCsv).then(() => {
    console.log('Processing and evaluation completed.');
}).catch(error => {
    console.error('Error during processing and evaluation:', error);
});

