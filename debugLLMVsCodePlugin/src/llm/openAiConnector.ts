// src/api.ts
import axios from 'axios';


const apiKey = "";  // Replace with your actual OpenAI API key


export async function openAIApiConnector(query:string): Promise<any> {
    const url = 'https://api.openai.com/v1/chat/completions';
    const headers = {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${apiKey}`
    };
    const data = {
        model: 'gpt-4o',
        messages: [
            {
                role: 'system',
                content: `You are an expert software developer. ${query}`
            }
        ]
    };


    try {
        const response = await axios.post(url, data, { headers });
        return response.data;
    } catch (error) {
        console.error('Error fetching data:', error);
        throw error;
    }
}
