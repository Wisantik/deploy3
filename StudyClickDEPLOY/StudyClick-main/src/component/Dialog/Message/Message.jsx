import React from "react";
import s from "./Message.module.css";
import user_logo from "../../../image/user_logo.jpg"
const Message = (props) => {
  return (
    <div className={s.ai}>
      <div className={s.ai_ava_block}>
        {props.item.role == "bot" ? (
          <img className={s.ai_ava} src="https://i.namu.wiki/i/AMk1eXIzzjYQwO3lBV61vl7c819FzRa89v0MlUZRrlmkPREt0rSJxD7kd2TM3N9M1-jlqRLppXI2fo40tSpVxw.webp" alt="" />
        ) : (
          <img className={s.user_ava} src={user_logo}/>
        )}

        <div>{props.item.role}</div>
      </div>
      {props.item.role == "bot" ? 
      <div className={s.ai_text_block}>
      <div className={s.message_text}>
        {props.item.message}
    </div>
    </div>
    :
    <div className={s.user_text_block}>
        <div className={s.message_text}>
          {props.item.message}
      </div>  
    </div>}
    </div>
  );
};
export default Message;
