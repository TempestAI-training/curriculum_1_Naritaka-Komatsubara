import './App.css';
import { useState } from "react";

function App() {
  const [isVisible, setIsVisible] = useState(true);
  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");
  const [tag, setTag] = useState("");
  const handleSave = () => {
    console.log("保存するメモ:", {
      title: title,
      content: content,
      tag: tag,
    });
  };
  return (
    <div className="App">
      <header className="App-header">
        <h2>簡易メモアプリケーション</h2>

        <p>
        このアプリでは、タイトル・内容・タグを入力して
        メモを作成できます。
        </p>

        <button
          onClick={() =>
             console.log("このアプリはメモ管理用のReactアプリです")
          }
        >
          このアプリについて
        </button>

        <button onClick={() => setIsVisible(!isVisible)}>
          フォーム表示切り替え
        </button>

        {isVisible && (
          <div
            style={{
              display: "flex",
              flexDirection: "column",
              gap: 10,
              padding: 20,
              border: "1px solid #61dafb",
              marginTop: 20,
              width: 300,
            }}
          >
            <label>
              タイトル
              <input
                type="text"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
              />
            </label>

            <label>
              内容
              <textarea
                value={content}
                onChange={(e) => setContent(e.target.value)}
              />
            </label>

            <label>
              タグ
              <input
                type="text"
                value={tag}
                onChange={(e) => setTag(e.target.value)}
              />
            </label>

            <button onClick={handleSave}>保存</button>
          </div>
        )}

      </header>
    </div>
  );
}

export default App;
