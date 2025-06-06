import * as vscode from 'vscode';

async function isCompilable(filePath: string): Promise<boolean> {
    try {
        // Open doc
        const document = await vscode.workspace.openTextDocument(filePath);
        await vscode.window.showTextDocument(document);

        const diagnostics: vscode.Diagnostic[] = vscode.languages.getDiagnostics(document.uri);

        // Check for errors
        const errors = diagnostics.filter(diagnostic => diagnostic.severity === vscode.DiagnosticSeverity.Error);

        if (errors.length > 0) {
            console.log(`The file ${filePath} contains syntax errors.`);
            errors.forEach((error: vscode.Diagnostic) => {
                console.log(`Error: ${error.message} at line ${error.range.start.line + 1}, column ${error.range.start.character + 1}`);
            });
            return false;
        } else {
            console.log(`The file ${filePath} has no syntax errors.`);
            return true; // in case of no syntax errors
        }
    } catch (error) {
        console.error(`Failed to check for syntax errors`);
        return false;
    }
}