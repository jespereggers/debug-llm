import { availableTools } from '../../tools/availableTools';
import { extractCodeFromSource } from '../../utils';

const discoverBugHelper = async (runFromCommandLine:boolean=false, code:any=null) => {
    //let code = extractCodeFromSource(runFromCommandLine,inputCode);
    console.log("Discover: ", code);
    const query = `There can be one or many bugs in the given code, find it and report the bug. Keep your answer concise , do not fix it: ${code}`;
    const bug = await availableTools.openAiQueryTool(query);
    return ({"code": code, "bug": bug});
};

export default discoverBugHelper;