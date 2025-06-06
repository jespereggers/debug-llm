import { availableTools } from '../../tools/availableTools';
import discoverBugHelper from './discoverBugHelper';
import { replaceOrReturnCode } from '../../utils';

const bugFixHelper = async (runFromCommandLine:boolean=false, inputCode:any= null) => {
    const {bug, code} = await discoverBugHelper(runFromCommandLine,inputCode);
    const query = `Fix this bug: ${bug} in the given code and only return the code, do not offer any explaination : ${code}`;
    const codeFix = await availableTools.openAiQueryTool(query);
    console.log("codeFix: ", codeFix)
    return codeFix;
};

export default bugFixHelper;