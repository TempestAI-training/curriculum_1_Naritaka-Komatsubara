import "./App.css";
import App from "./App";
import { useState }  from "react";

function Chat2 () {

    const [page, backpage]  = useState<"Page" | "Chat">("Chat");

    const [text, setText] = useState("")

    const handleNameChange = (event: any) => {
        setText(event.target.value)
    }
        
    const [chatMessages, setChatMessages] = useState<any[]>([])

    function sendMessages() {
        setChatMessages([
            ...chatMessages,
            {
                message: text,
                sender:'user'
            }
        ]);

        setText("")
    }

    if(page == "Page"){
        return <App/>
    }

    return (
        <header className="Box">
            <div className="top">
                <div className="study">
                政策チャットボット
                </div>

                <div className="return" onClick={() => backpage("Page")}>
                戻る
                </div>
            </div>

            <div className="message">
            {chatMessages.map((msg) => (
                <>
                <div className="UserMessage">
                {msg.message}
                </div>

                <div className="Response">
                高市さんは日本の総理大臣です。
                </div>
                </>
            ))}
            </div>

            <div className="chatInputWrap">
                <input type="text" className="chatInput" placeholder='例)天気やニュースなど気になることを入力' value={text} onChange={(e) => setText(e.target.value)}>
                </input>
                <div className="sendButton" onClick={sendMessages}>
                送信
                </div>              
            </div>

        </header>
    );       
}

export default Chat2;