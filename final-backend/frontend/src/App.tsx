import React from "react";
import "./App.css";
import { useState } from "react";
import Chat1 from "./Chat1.tsx";
import Chat2 from "./Chat2.tsx";

function App() {
  const [site, setSite] = useState(true);

  return (
    <div className="App">

       {site ? (
              <header className="Box">
        <p>Politics Study</p>
          <h2>早苗さんの政策について学ぼう！</h2>
          <h3>任意のお問い合わせに対して早苗さんの考えを返信します。</h3>
          <div className="butt" onClick={() => setSite(!site)}>
              チャットを始める
          </div>

         
      </header>
       ) : (<Chat2/>)}

    </div>
  );
};

export default App;
