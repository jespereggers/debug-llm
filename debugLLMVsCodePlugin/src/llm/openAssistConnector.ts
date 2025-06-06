import axios, { AxiosError } from 'axios';
import * as readline from 'readline';

const API_KEY = "";
const VERSION = "gpt-4o";
const ASSIST_URL = "https://api.openai.com/v1/assistants";
const THREADS_URL = "https://api.openai.com/v1/threads";

let messagesUrl: string;
let runUrl: string;
let runStepsUrl: string;
let toolOutputsUrl: string;

let assistId: string = "";
let threadId: string = "";

let requestCount: number = 0;
let displayedCreatedAt: string[] = [];
let processingFuncCall: boolean = false;

const temperature = 0.5;
const maxTokens = 1024;

const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

interface AssistantResponse {
    id: string;
    object: string;
}

interface ThreadResponse {
    id: string;
    object: string;
}

interface MessageResponse {
    role: string;
    content: { text: { value: string } }[];
    created_at: string;
}

interface RunStepResponse {
    id: string;
    object: string;
    step_details: {
        type: string;
        tool_calls?: any[];
    };
    status: string;
}

async function createAssistant() {
    const headers = {
        "Content-type": "application/json",
        "Authorization": `Bearer ${API_KEY}`,
        "OpenAI-Beta": "assistants=v2"
    };

    const body = {
        instructions: "You are an expert in TypeScript. Use the getScript tool if you need insights and replaceLine to replace a line in code, for example to fix a bug.",
        name: "VSCodeAssistant",
        tools: [
            {
                type: "function",
                function: {
                    description: "Get the currently opened TypeScript file.",
                    name: "getScript"
                }
            },
            {
                type: "function",
                function: {
                    description: "Replace a line with new code.",
                    name: "replaceLine",
                    parameters: {
                        type: "object",
                        properties: {
                            new_code: {
                                type: "string",
                                description: "The code to replace a line with."
                            },
                            line_number: {
                                type: "integer",
                                description: "Line number to replace with new code."
                            }
                        },
                        required: ["new_code", "line_number"]
                    }
                }
            }
        ],
        model: VERSION
    };

    try {
        const response = await axios.post<AssistantResponse>(ASSIST_URL, body, { headers });
        assistId = response.data.id;
        await createThread();
    } catch (error) {
        handleAxiosError(error as AxiosError);
    }
}

async function createThread() {
    const headers = {
        "Content-type": "application/json",
        "Authorization": `Bearer ${API_KEY}`,
        "OpenAI-Beta": "assistants=v2"
    };

    try {
        const response = await axios.post<ThreadResponse>(THREADS_URL, {}, { headers });
        threadId = response.data.id;
        messagesUrl = `${THREADS_URL}/${threadId}/messages`;
        runUrl = `${THREADS_URL}/${threadId}/runs`;
    } catch (error) {
        handleAxiosError(error as AxiosError);
    }
}

async function addMessage(role: string, message: string) {
    const headers = {
        "Content-type": "application/json",
        "Authorization": `Bearer ${API_KEY}`,
        "OpenAI-Beta": "assistants=v2"
    };

    const body = {
        role: role,
        content: {
            text: message
        }
    };

    try {
        await axios.post(messagesUrl, body, { headers });
    } catch (error) {
        handleAxiosError(error as AxiosError);
    }
}

async function getMessages() {
    const headers = {
        "Content-type": "application/json",
        "Authorization": `Bearer ${API_KEY}`,
        "OpenAI-Beta": "assistants=v2"
    };

    try {
        const response = await axios.get<{ data: MessageResponse[] }>(messagesUrl, { headers });
        handleResponse(response.data);
    } catch (error) {
        handleAxiosError(error as AxiosError);
    }
}

async function run(prompt: string) {
    await addMessage("user", prompt);

    const headers = {
        "Content-type": "application/json",
        "Authorization": `Bearer ${API_KEY}`,
        "OpenAI-Beta": "assistants=v2"
    };

    const body = {
        assistant_id: assistId,
        instructions: "Keep your answers precise and very short."
    };

    try {
        const response = await axios.post<RunStepResponse>(runUrl, body, { headers });
        runStepsUrl = `${runUrl}/${response.data.id}/steps`;
        toolOutputsUrl = `${runUrl}/${response.data.id}/submit_tool_outputs`;
    } catch (error) {
        handleAxiosError(error as AxiosError);
    }
}

async function getRunSteps() {
    const headers = {
        "Content-type": "application/json",
        "Authorization": `Bearer ${API_KEY}`,
        "OpenAI-Beta": "assistants=v2"
    };

    try {
        const response = await axios.get<{ data: RunStepResponse[] }>(runStepsUrl, { headers });
        handleResponse(response.data);
    } catch (error) {
        handleAxiosError(error as AxiosError);
    }
}

async function sendFuncOutput(toolCalls: any[]) {
    if (toolCalls.length === 0) {
        await getRunSteps();
        return;
    }

    let outputs: any[] = [];

    for (const call of toolCalls) {
        if (call.type === "function") {
            // Assuming these functions are implemented
            if (call.function.name === "getScript") {
                outputs.push({
                    tool_call_id: call.id,
                    output: "current script content" // Implement the actual script content retrieval
                });
            } else if (call.function.name === "replaceLine") {
                // Implement the actual line replacement logic
                const { new_code, line_number } = call.function.arguments;
                outputs.push({
                    tool_call_id: call.id,
                    output: `Replaced line ${line_number} with ${new_code}`
                });
            }
        }
    }

    const headers = {
        "Content-type": "application/json",
        "Authorization": `Bearer ${API_KEY}`,
        "OpenAI-Beta": "assistants=v2"
    };

    const body = {
        tool_outputs: outputs
    };

    try {
        await axios.post(toolOutputsUrl, body, { headers });
    } catch (error) {
        handleAxiosError(error as AxiosError);
    }
}

function handleResponse(response: { data: any }) {
    response.data.forEach((item: any) => {
        if (item.object === "assistant") {
            assistId = item.id;
        } else if (item.object === "thread") {
            threadId = item.id;
            messagesUrl = `${THREADS_URL}/${threadId}/messages`;
            runUrl = `${THREADS_URL}/${threadId}/runs`;
        } else if (item.object === "thread.run") {
            runStepsUrl = `${runUrl}/${item.id}/steps`;
            toolOutputsUrl = `${runUrl}/${item.id}/submit_tool_outputs`;
        } else if (item.object === "thread.run.step") {
            if (item.status === "completed") {
                // Handle step completion
            }
            if (item.step_details.type === "tool_calls") {
                sendFuncOutput(item.step_details.tool_calls);
            } else if (item.step_details.type === "message_creation") {
                getMessages();
            }
        } else if (item.object === "thread.message") {
            const firstMessage = item.content[0];
            if (firstMessage && firstMessage.role === "assistant" && !displayedCreatedAt.includes(firstMessage.created_at)) {
                displayedCreatedAt.push(firstMessage.created_at);
                console.log(firstMessage.text.value);
            }
        }
    });
}

function askQuestion(query: string): Promise<string> {
    return new Promise(resolve => rl.question(query, resolve));
}

function startPolling() {
    setInterval(async () => {
        await getMessages();
        if (runStepsUrl) {
            await getRunSteps();
        }
    }, 1000); // Poll every second
}

function handleAxiosError(error: AxiosError) {
    if (error.response) {
        console.error('Error response:', error.response.data);
    } else if (error.request) {
        console.error('Error request:', error.request);
    } else {
        console.error('Error message:', error.message);
    }
}

(async () => {
    await createAssistant();
    await createThread();

    startPolling();

    while (true) {
        const prompt = await askQuestion("Enter your prompt: ");
        await run(prompt);
    }
})();
