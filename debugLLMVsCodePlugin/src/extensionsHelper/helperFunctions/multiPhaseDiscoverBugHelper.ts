import { availableTools } from '../../tools/availableTools';
import { extractCodeFromSource } from '../../utils';
const multiPhaseDiscoverBugHelper = async (phase:string, runFromCommandLine:boolean=false, inputCode:any=null) => {
    let code = extractCodeFromSource(runFromCommandLine,inputCode);
    console.log("Discover: ", code);
    const query = "There can be one or many" + phase +" errors in the given code, find every " + phase +" error and report the it. Keep your answer concise, do not fix it: ${code}";
    const bug = await availableTools.openAiQueryTool(query);
    return ({"code": code, "bug": bug});
};

export default multiPhaseDiscoverBugHelper;