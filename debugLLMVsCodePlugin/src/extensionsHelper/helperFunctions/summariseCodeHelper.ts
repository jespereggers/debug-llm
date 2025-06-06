import { availableTools } from '../../tools/availableTools';

const summariseCodeHelper = async (inputCode:string) => {
    const query = `Summarise the given code: ${inputCode}`;
    const codeSummary = await availableTools.openAiQueryTool(query);
};

export default summariseCodeHelper;