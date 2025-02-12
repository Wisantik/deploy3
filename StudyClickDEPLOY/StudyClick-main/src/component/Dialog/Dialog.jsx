import React, { useEffect, useState, useCallback, useRef } from "react";
import s from "./Dialog.module.css";
import Message from "./Message/Message";
import Prompt from "../Aside_propmpt/Prompt";
import ai_logo from "../../image/ai_logo.png";
import { useMemo } from "react";

const Dialog = (props) => {
  const id = localStorage.getItem("session_id");
  const history = localStorage.getItem("history_id");
  const field_id = localStorage.getItem("study_field_id");
  const [message, setMessage] = useState("");
  const [disabled, setDisabled] = useState(false);

  useEffect(() => {
    props.getHistoryChat(id);
  }, [id, props.getHistoryChat]);

  useEffect(() => {
    props.PromptThunk(field_id);
  }, [field_id, props.PromptThunk]);

  const sendMessage = useCallback(() => {
    if (message.trim() === "") return;
    setDisabled(true);
    props.createMessage(message, history, id, field_id);
    setMessage("");
    setDisabled(false);
  }, [message, history, id, field_id, props.createMessage]);

  const handleKeyPress = useCallback((event) => {
    if (event.key === "Enter") {
      sendMessage();
    }
  }, [sendMessage]);


  useEffect(() => {
    if (props.message.length === 2 && message === "") {
      props.setTitleChat(id);
    }
  }, [props.message.length, message, id, props.setTitleChat]);

  const messages = useMemo(() => {
    return props.message.filter((e) => e.message !== "").map((e) => <Message key={e.id} item={e} />);
  }, [props.message]);


  const messagesEndRef = useRef(null);
  const scrollToBottom = useCallback(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, []);
  
  useEffect(() => {
    scrollToBottom();
  }, [props.message, scrollToBottom]);
  
  if (props.dialogs_data.length === 0) {
    return <div></div>;
  }
  return (
    <div className={s.dialog}>
      <div className={s.dialog_window}>
        <div className={s.user_window}>
          {props.message.length > 1 && messages} {/* Use memoized messages */}

        <div ref={messagesEndRef} style={{ float: "left", clear: "both" }} />
        </div>
        <div className={s.prompt}>
          <span className={s.prompt_name}>Примеры запросов</span>
          <div className={s.prompt_block}>
            <ul className="list-group">
              {props.prompt.map((e) => (
                <Prompt
                  key={e.id} // Add key prop for React
                  study_field_id={field_id}
                  session_id={id}
                  historyId={history}
                  createMessage={props.createMessage}
                  item={e}
                />
              ))}
            </ul>
          </div>
        </div>
      </div>
      <div className={s.input_wrapper}>
        <input
          value={message}
          onKeyUp={handleKeyPress}
          onChange={(e) => setMessage(e.target.value)}
          className={s.dialog_input}
          type="text"
          placeholder="Введите сообщение..." // Added placeholder for better UX
        />
        <button
          className={s.input_btn}
          disabled={disabled}
          onClick={sendMessage}
        >
          Отправить
          <img className={s.ai_img} src={ai_logo} alt="AI Logo" /> {/* Added alt text for accessibility */}
        </button>
      </div>
    </div>
  );
};

export default Dialog;
