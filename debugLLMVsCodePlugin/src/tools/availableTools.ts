
import openAiQueryTool from "./assistTools/openAiQueryTool";
import { getProjectIndex } from "./assistTools/getProjectIndex";
export const availableTools = {
    "openAiQueryTool": openAiQueryTool,
    "getProjectIndex": getProjectIndex
}