const vscode = require('vscode');
const replaceCodeInEditor = async (newCode:any) => {
    const editor = vscode.window.activeTextEditor;
    if (editor) {
        const document = editor.document;
        const firstLine = document.lineAt(0);
        const lastLine = document.lineAt(document.lineCount - 1);
        const textRange = new vscode.Range(firstLine.range.start, lastLine.range.end);
        editor.edit((editBuilder:any) => {
            editBuilder.replace(textRange, newCode.replace(/```python/g, '').replace(/```/g, ''))
        }).then((success:any) => {
            if (success) {
                vscode.window.showInformationMessage('Code replaced successfully!');
                return("success");
            } else {
                vscode.window.showErrorMessage('Failed to replace code.');
                return("failure");
            }
        });
    } else {
        vscode.window.showInformationMessage('No active editor found!');
    }
}


export default replaceCodeInEditor;