"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var fs = require("fs");
var path = require("path");

function saveDataStructureToJson(data, fileName) {
    var jsonContent = JSON.stringify(data, null, 2);
    var filePath = path.join(__dirname, fileName);
    fs.writeFileSync(filePath, jsonContent, 'utf8');
    console.log("Data saved to ".concat(filePath));
}
/**
 * Extracts function names, their arguments, and return types from a TypeScript file.
 * @param filePath The path to the TypeScript file.
 * @returns A list of objects each containing the function name, arguments, and return type.
 */
function extractFunctionDetails(filePath) {
    var content = fs.readFileSync(filePath, 'utf8');
    var functionDetailsPattern = /(?:function (\w+)\(([^)]*)\)(?::\s*([^{\n]+))?|(\w+)(?::\s*\w+\s*=)?\s*=\s*\(([^)]*)\)\s*=>\s*(?::{\s*([^{\n]+)}|{))/g;
    var functions = [];
    var match;
    while (match = functionDetailsPattern.exec(content)) {
        var name_1 = match[1] || match[4];
        var argsMatch = match[2] || match[5];
        var returnType = match[3] || match[6];
        var args = argsMatch ? argsMatch.split(',')
            .map(function (arg) { return arg.trim().replace(/:.*/, '').trim(); })
            .filter(Boolean) : [];
        functions.push({ name: name_1, args: args, returnType: returnType === null || returnType === void 0 ? void 0 : returnType.trim() });
    }
    return functions;
}
/**
 * Performs a depth-first search on the given directory, collecting TypeScript function details.
 * @param dirPath The starting directory path.
 * @param result An object to accumulate results.
 * @returns An object with paths as keys and function details as values.
 */
function dfs(dirPath, result) {
    if (result === void 0) { result = {}; }
    try {
        var items = fs.readdirSync(dirPath);
        items.forEach(function (item) {
            var fullPath = path.join(dirPath, item);
            var stats = fs.statSync(fullPath);
            if (fullPath.endsWith(".ts")) {
                var funcDetails = extractFunctionDetails(fullPath);
                if (funcDetails.length > 0) {
                    result[fullPath] = funcDetails;
                }
                //console.log(fullPath.split("\\").pop()); // Changed to 'pop' for compatibility with all OS
            }
            if (stats.isDirectory()) {
                dfs(fullPath, result);
            }
        });
    }
    catch (error) {
        console.error("Error accessing path ".concat(dirPath, ": ").concat(error));
    }
    return result;
}
var projectPath = "C:/Users/jespe/OneDrive/Dokumente/GitHub/24SS-DebugLLM/debugLLMVsCodePlugin/src";

var startPath = projectPath + process.argv[2];
var indexList = dfs(startPath, {});
console.log(indexList);
saveDataStructureToJson(indexList, "indexList.json");
