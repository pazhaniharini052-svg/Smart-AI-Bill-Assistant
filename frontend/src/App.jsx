import { useState } from "react";
import { Streamlit } from "streamlit-component-lib";
import "./App.css";


function App() {

  const [open, setOpen] = useState(false);
  const [question, setQuestion] = useState("");


  function sendMessage(){

    if(question){

      Streamlit.setComponentValue(question);

      setQuestion("");

    }

  }


  return (

    <>

      <button
        className="chat-button"
        onClick={() => setOpen(!open)}
      >
        🤖
      </button>


      {open && (

        <div className="chat-box">

          <div className="chat-header">

            🤖 AI Bill Assistant

            <button
              onClick={()=>setOpen(false)}
            >
              ✖
            </button>

          </div>


          <input

            value={question}

            onChange={
              (e)=>setQuestion(e.target.value)
            }

            placeholder="Ask about your bills..."

          />


          <button onClick={sendMessage}>
            Send
          </button>


        </div>

      )}

    </>

  );

}


export default App;