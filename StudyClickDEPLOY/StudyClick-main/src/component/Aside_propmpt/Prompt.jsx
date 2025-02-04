import React from "react";
import s from "./Prompt.module.css"
const Prompt = (props) => {
    const sendMessage = (event) => {
        props.createMessage(
        props.item.example,
          props.historyId,
          props.session_id,
          props.study_field_id
        );  
  }
    return(
        <div >
          <li class="list-group-item" onClick={sendMessage}>{props.item.example}</li>
        {/* <div className={s.prompt_item} onClick={sendMessage}></div> */}
        </div>
    )
}
export default Prompt