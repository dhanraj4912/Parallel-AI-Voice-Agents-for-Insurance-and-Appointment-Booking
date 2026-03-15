import React, { createContext, useRef, useState } from "react";
import { runGemini } from "../api/gemini";

export const datacontext = createContext();

function UserContext({ children }) {

  const [messages, setMessages] = useState([]);
  const [status, setStatus] = useState("Idle");

  async function aiResponse(prompt) {

    setMessages(prev => [...prev,{sender:"Patient",text:prompt}])

    const response = await runGemini(prompt)

    setMessages(prev => [...prev,{sender:"Assistant",text:response}])
  }

  function connect(){
    setStatus("Listening")
  }

  function disconnect(){
    setStatus("Idle")
  }

  const value = {
    connect,
    disconnect,
    messages,
    status
  }

  return(
    <datacontext.Provider value={value}>
      {children}
    </datacontext.Provider>
  )
}

export default UserContext