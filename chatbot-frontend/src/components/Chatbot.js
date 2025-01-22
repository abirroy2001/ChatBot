import React, { useState } from "react";

const Chatbot = () => {
    const [messages, setMessages] = useState([]);
    const [userMessage, setUserMessage] = useState("");

    const sendMessage = async () => {
        if (!userMessage.trim()) return;

        // Add user message to the chat
        setMessages([...messages, { sender: "user", text: userMessage }]);
        setUserMessage(""); // Clear input field

        try {
            // Send the message to the backend
            const response = await fetch("http://127.0.0.1:5000/chat", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ message: userMessage }),
            });

            const data = await response.json();

            console.log("Backend Response:", data);  // Log the response for debugging
            
            // Add bot's response to the chat
            if (data.reply) {
                setMessages((prevMessages) => [
                    ...prevMessages,
                    { sender: "bot", text: data.reply },  // Display the reply from backend
                ]);
            } else {
                setMessages((prevMessages) => [
                    ...prevMessages,
                    { sender: "bot", text: "Sorry, I didn't understand that." },
                ]);
            }
        } catch (error) {
            console.error("Error communicating with the server:", error);
            setMessages((prevMessages) => [
                ...prevMessages,
                { sender: "bot", text: "Sorry, something went wrong!" },
            ]);
        }
    };

    return (
        <div style={{ maxWidth: "600px", margin: "0 auto", textAlign: "center" }}>
            <h1>Chatbot</h1>
            <div
                style={{
                    border: "1px solid #ccc",
                    padding: "10px",
                    marginBottom: "10px",
                    height: "300px",
                    overflowY: "scroll",
                }}
            >
                {messages.map((msg, index) => (
                    <div
                        key={index}
                        style={{
                            textAlign: msg.sender === "user" ? "right" : "left",
                            margin: "5px 0",
                        }}
                    >
                        <strong>{msg.sender === "user" ? "You" : "Bot"}:</strong>{" "}
                        {msg.text}
                    </div>
                ))}
            </div>
            <input
                type="text"
                value={userMessage}
                onChange={(e) => setUserMessage(e.target.value)}
                placeholder="Type a message"
                style={{ width: "80%", padding: "10px" }}
            />
            <button onClick={sendMessage} style={{ padding: "10px" }}>
                Send
            </button>
        </div>
    );
};

export default Chatbot;
