import { availableTools } from '../../tools/availableTools';
import multiPhaseDiscoverBugHelper from './multiPhaseDiscoverBugHelper';
import { replaceOrReturnCode } from '../../utils';
const multiPhaseBugFixHelper = async (runFromCommandLine:boolean=false) => {
    // Concept is to direct the attention of intelligence to certain 
    // types of error that are particularly likely to occur.

    // Phase 1: Syntax-fix
    const { bug: syntaxBug, code: syntaxCode } = await multiPhaseDiscoverBugHelper("syntax",runFromCommandLine);
    const syntaxQuery = `Only find and fix any syntax errors, that might occure here: ${syntaxBug} in the given code and only return the code, do not offer any explaination : ${syntaxCode}`;
    const syntaxCodeFix = await availableTools.openAiQueryTool(syntaxQuery);
    

    // Phase 2: Semantic-fix
    const { bug: semanticBug, code: semanticCode } = await multiPhaseDiscoverBugHelper("semantic",runFromCommandLine);
    const semanticQuery = `Only find and fix any semantic errors, that might occure here: ${semanticBug} in the given code and only return the code, do not offer any explaination : ${semanticCode}`;
    const semanticCodeFix = await availableTools.openAiQueryTool(semanticQuery);
    return await replaceOrReturnCode(runFromCommandLine,semanticCodeFix);
};

export default multiPhaseBugFixHelper;


