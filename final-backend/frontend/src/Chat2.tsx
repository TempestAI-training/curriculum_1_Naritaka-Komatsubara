import "./App.css";
import App from "./App.tsx";
import { useState }  from "react";

function Chat2 () {

    const [page, backpage]  = useState<"Page" | "Chat">("Chat");

    const [text, setText] = useState("")

    const handleNameChange = (event: any) => {
        setText(event.target.value)
    }

    type Message = {
        message : string;
        sender : "user" | "ai";
    }
        
    const [chatMessages, setChatMessages] = useState<Message[]>([])

    const [reply, setReply] = useState("")
  
    const lateApi = async (ms :string) => {

        console.log("lateApi開始", ms);

        const res = await fetch("http://localhost:8000/chat", {
            method:"POST",
            headers: {
                "Content-type" : "application/json",
            },
            body: JSON.stringify({
                message: ms,
                conversation_id: "room1"
            })
        }
        )

        console.log("fetch完了", res)

        type ChatResponse = {
            reply:string
        }

        const json: ChatResponse = await res.json()

        console.log("json取得", json)
        return json.reply
    };

    const sendMessages = async ()  => {
        const newMessages = [
            ...chatMessages,
            {
                message: text,
                sender:'user'
            }
        ];

        setChatMessages(newMessages)
        setText("")

        const aiReply = await lateApi(text)

        setChatMessages(
            [
                ...newMessages, {
                    message: aiReply,
                    sender: "ai"
                }
            ]
        )

        console.log("テキスト取得", aiReply)
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
            {chatMessages.map((msg, index) => (
                <div key={index}>
                    {msg.sender == 'user' ? (
                        <div className="UserMessage">
                            {msg.message}
                        </div>
                        ) : (
                        <div className="Response">   
                            {msg.message}
                        </div> 
                        )
                    }
                </div>

                /* <>
                    <div className="UserBox"> 
                        <div className="UserMessage">
                            {msg.message}
                        </div>
                    </div>

                    <div className="ResponseBox">
                        <div className="Response">   
                            {reply}
                        </div>
                    </div>
                </> */
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