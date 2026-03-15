import { GoogleGenAI } from "@google/genai";

const ai = new GoogleGenAI({
  apiKey: import.meta.env.VITE_GEMINI_API_KEY,
});

let conversationHistory = [];

export async function runGemini(prompt) {

  conversationHistory.push(`User: ${prompt}`);

  const response = await ai.models.generateContent({
    model: "gemini-2.0-flash",
    contents: conversationHistory.join("\n"),
  });

  const text =
    response?.candidates?.[0]?.content?.parts?.[0]?.text ||
    "No response";

  conversationHistory.push(`Assistant: ${text}`);

  return text;
}

export function resetConversation() {
  conversationHistory = [];
}