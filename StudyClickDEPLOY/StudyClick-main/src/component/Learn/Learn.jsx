import React, { useState } from "react";
import s from "./Learn.module.css";
import { NavLink } from "react-router-dom";
import { v4 as uuidv4 } from 'uuid';
const Learn = ({ getCurrentFields, learn, setFieldId, AddDialogs,setId }) => {
  const watchingLearn = () => {
    getCurrentFields();
  };
  const session_id  = uuidv4();
  const onFieldCurrent = (element) => {
    setFieldId(element.id, element.name, element.prompt)
    AddDialogs("New chat", session_id)
    setId(session_id)
    localStorage.setItem("session_id",session_id)
    localStorage.setItem("study_field_id",element.id)
  }
  return (
    <div className={s.wrapper}>
      <div className={s.learn_block}>
      <div class="dropdown">
        <button
          class="btn btn-secondary dropdown-toggle"
          type="button"
          id="dropdownMenuButton1"
          data-bs-toggle="dropdown"
          aria-expanded="false"
          onClick={() => watchingLearn()}
        >
          Выберите сферу для обучения
        </button>
        <ul class="dropdown-menu" aria-labelledby="dropdownMenuButton1">
        {learn.map((e) => (
       <li class={s.field}>
       <NavLink href="#" to={"/dialog/" + session_id}
     onClick={() => onFieldCurrent(e)}>
          {e.name}
       </NavLink>
     </li>
      ))}  
        </ul>
      </div>
      </div>
    </div>
  );
};
export default Learn;
