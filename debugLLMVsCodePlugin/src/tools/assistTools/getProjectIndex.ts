import * as fs from 'fs';
import * as path from 'path';


interface FunctionInfo {
    name: string;
    args: any[];
    returnType: string | undefined;
}

interface DataStructure {
    [filePath: string]: FunctionInfo[];
}

function saveDataStructureToJson(data: DataStructure, fileName: string): void {
    const jsonContent = JSON.stringify(data, null, 2);
    const filePath = path.join(__dirname, fileName);
    fs.writeFileSync(filePath, jsonContent, 'utf8');
    console.log(`Data saved to ${filePath}`);
}


/**
 * Extracts function names, their arguments, and return types from a TypeScript file.
 * @param filePath The path to the TypeScript file.
 * @returns A list of objects each containing the function name, arguments, and return type.
 */
function extractFunctionDetails(filePath: string): { name: string; args: string[]; returnType?: string }[] {
    const content = fs.readFileSync(filePath, 'utf8');

    const functionDetailsPattern = /(?:function (\w+)\(([^)]*)\)(?::\s*([^{\n]+))?|(\w+)(?::\s*\w+\s*=)?\s*=\s*\(([^)]*)\)\s*=>\s*(?::{\s*([^{\n]+)}|{))/g;

    const functions: { name: string; args: string[]; returnType?: string }[] = [];

    let match: RegExpExecArray | null;

    while (match = functionDetailsPattern.exec(content)) {
        const name = match[1] || match[4]; 
        const argsMatch = match[2] || match[5]; 
        const returnType = match[3] || match[6];

        const args = argsMatch ? argsMatch.split(',')
            .map(arg => arg.trim().replace(/:.*/, '').trim())
            .filter(Boolean) : [];

        functions.push({ name, args, returnType: returnType?.trim() });
    }

    return functions;
}


/**
 * Performs a depth-first search on the given directory, collecting TypeScript function details.
 * @param dirPath The starting directory path.
 * @param result An object to accumulate results.
 * @returns An object with paths as keys and function details as values.
 */
function dfs(dirPath: string, result: {[key: string]: any[]} = {}): {[key: string]: any[]} {
    try {
        const items = fs.readdirSync(dirPath);

        items.forEach(item => {
            const fullPath = path.join(dirPath, item);
            const stats = fs.statSync(fullPath);
            
            if (fullPath.endsWith(".ts")) {
                const funcDetails = extractFunctionDetails(fullPath);
                if (funcDetails.length > 0) {
                    result[fullPath] = funcDetails;
                }
            }
            
            if (stats.isDirectory()) {
                dfs(fullPath, result);
            }
        });
    } catch (error) {
        console.error(`Error accessing path ${dirPath}: ${error}`);
    }

    return result;
}


export function getProjectIndex(): DataStructure {
    const projectPath = path.join(process.cwd(), "src");
    const startPath = projectPath;
    const indexList = dfs(startPath, {});
    return indexList;
}

console.log(getProjectIndex());