import { openAIApiConnector } from "../../llm/openAiConnector";

const openAiQueryTool = async (query:string) => {
    try{
        const response = await openAIApiConnector(query);
            console.log(response?.choices?.[0]?.message?.content);
            return (response?.choices?.[0]?.message?.content);
        } 
        catch (error) {
            console.log('Failed to fetch summary.');
            return("error");
        }
    }

export default openAiQueryTool;