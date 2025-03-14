import React, { useState } from "react";
import axios from "axios";
import "./App.css"; // Import the external CSS file

function App() {
  const [query, setQuery] = useState("");
  const [messages, setMessages] = useState([]);
  const [typingResponse, setTypingResponse] = useState("");
  const [isTyping, setIsTyping] = useState(false);

  const handleSend = async () => {
    if (!query.trim()) return;

    setMessages((prev) => [...prev, { sender: "user", text: query }]);
    setQuery("");

    try {
      setIsTyping(true);
      const res = await axios.post("http://127.0.0.1:8000/ask", { query });
      const botResponse = res.data.response;

      setTypingResponse("");
      let i = 0;
      const typingInterval = setInterval(() => {
        if (i < botResponse.length) {
          setTypingResponse((prev) => prev + botResponse[i]);
          i++;
        } else {
          clearInterval(typingInterval);
          setIsTyping(false);
          setMessages((prev) => [...prev, { sender: "bot", text: botResponse }]);
        }
      }, 20);
    } catch (error) {
      console.error("Error:", error);
      setIsTyping(false);
      setMessages((prev) => [...prev, { sender: "bot", text: "Error fetching response. Try again." }]);
    }
  };

  return (
    <div className="container">
      <div className="chatBox">
        <h1 className="title">AI Chatbot</h1>
        <h1 className="title">Enhancing Customer Experience</h1>
        <div className="chatWindow">
          {messages.map((msg, index) => (
            <div key={index} className={msg.sender === "user" ? "userBubble" : "botBubble"}>
              {msg.text}
            </div>
          ))}
          {isTyping && <div className="botBubble">{typingResponse || "..."}</div>}
        </div>
        <div className="inputArea">
          <input
            type="text"
            placeholder="Ask something..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            className="input"
          />
          <button onClick={handleSend} className="button">Send</button>
        </div>
      </div>
    </div>
  );
}

export default App;
