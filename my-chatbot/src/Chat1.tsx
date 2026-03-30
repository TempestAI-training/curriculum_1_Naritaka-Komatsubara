import Chat2 from "./Chat2"

function Chat1 () {
    return (
        <div>
            <header className="Box">
                <div className="study">Politics Study</div>
                <h2>早苗さんの政策について学ぼう！</h2>
                <h3>任意のお問い合わせに対して早苗さんの考えを返信します。</h3>
                <div className="butt" onClick={() => <Chat2/>}>
                    チャットを始める
                </div>
            </header>
        </div>
    );

}

export default Chat1;