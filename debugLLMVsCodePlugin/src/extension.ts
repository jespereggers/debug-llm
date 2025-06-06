import * as vscode from 'vscode';
import { helperFunctions } from './extensionsHelper/extensionsHelper';
export function activate(context: vscode.ExtensionContext) {
    console.log('Congratulations, your extension "extract-code" is now active!');

    let extractCodeSubscription = vscode.commands.registerCommand('extension.extractCode', () => {
        helperFunctions.getScriptsHelper()
    });
    let summariseCodeSubscription = vscode.commands.registerCommand('extension.summariseCode', () => {
        helperFunctions.summariseCodeHelper()
    });
    let discoverBugSubscription = vscode.commands.registerCommand('extension.discoverBug', () => {
        helperFunctions.discoverBugHelper()
    });
    let bugFixSubscription = vscode.commands.registerCommand('extension.bugFix', () => {
        helperFunctions.bugFixHelper()
    });
    let multiPhaseBugFixSubscription = vscode.commands.registerCommand('extension.multiPhaseBugFix', () => {
        helperFunctions.multiPhaseBugFixHelper()
    });
    const subscriptionArray = [
        extractCodeSubscription,
        summariseCodeSubscription,
        discoverBugSubscription,
        bugFixSubscription,
        multiPhaseBugFixSubscription
    ]
    context.subscriptions.push(...subscriptionArray);
}

export function deactivate() {}
