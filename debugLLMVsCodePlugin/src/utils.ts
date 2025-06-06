import {availableTools} from "./tools/availableTools";
export const extractCodeFromSource = async(runFromCommandLine:boolean= false,inputCode:any=null)=> {
    return new Promise((resolve) => {
        setTimeout(() => {
            resolve(inputCode); // Replace this with actual debugged code
        }, 1000);
    });
};


export const replaceOrReturnCode = async(runFromCommandLine:boolean=false, code:any) => {

    return new Promise((resolve) => {
        setTimeout(() => {
            resolve(code);
        }, 1000);
    });
};