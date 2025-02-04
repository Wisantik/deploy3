import React, { useEffect, useState } from "react";
import s from "./Dialog.module.css";
import Message from "./Message/Message";
import Prompt from "../Aside_propmpt/Prompt";
import ai_logo from "../../image/ai_logo.png"
const Dialog = (props) => {
  const [message, setMessage] = useState("");
  const [disabled, setDisabled] = useState(false);
  useEffect(() => {
    props.getHistoryChat(props.session_id);
  }, [props.session_id, props.active]);
  useEffect(() => {
    props.PromptThunk(props.study_field_id);
  }, []);
  const sendMessage = (event) => {
    setDisabled(true);
    props.createMessage(
      message,
      props.historyId,
      props.session_id,
      props.study_field_id
    );
    setMessage("");
    setDisabled(false);
  };
  const handleKeyPress = (event) => {
    if (event.key === "Enter") {
      props.createMessage(
        message,
        props.historyId,
        props.session_id,
        props.study_field_id
      );
      setMessage("");
    }
  };
  props.message.length == 2 && props.setTitleChat(props.session_id)
  return (
    <div className={s.dialog}>
      <div className={s.dialog_window}>
        <div className={s.user_window}>
          {props.message.length > 1 &&
            props.message.map((e) => e.message != "" && <Message item={e} />)}
        </div>
        <div className={s.prompt}>
            <span className={s.prompt_name}>Примеры запросов</span>
          <div className={s.prompt_block}>
            <ul class="list-group">
            {props.prompt.map((e) => (
              <Prompt
                study_field_id={props.study_field_id}
                session_id={props.session_id}
                historyId={props.historyId}
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
        />
        <button
          className={s.input_btn}
          disabled={disabled}
          onClick={sendMessage}
        >
          Отправить
          <img className={s.ai_img} src={ai_logo}/>
        </button>
      </div>
    </div>
  );
};
export default Dialog;
