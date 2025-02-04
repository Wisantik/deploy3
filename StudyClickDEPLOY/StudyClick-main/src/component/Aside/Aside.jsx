import React, { useEffect } from "react";
import s from './Aside.module.css'
import { NavLink } from "react-router-dom";
import { v4 as uuidv4 } from 'uuid';
import DialogsContainer from "../Dialogs/DialogsContainer";
import logo from "../../image/logo.png";
const Aside = (props) => {
  const addChat = () => {
    const session_id  = uuidv4();
    props.AddDialogs("New chat", session_id)
  }

  return(
    <aside>
   <div className={s.side_board}>
  <div className={s.aside}>
    <div className={s.logo_block}>
    <NavLink className={s.logo_ref} to={"/"}>
    <img className={s.logo} src={logo}/>
    </NavLink>
    </div>
  <div className={s.dialogs}>
  <span className={s.dialogs_name}>
    History
    </span>
  </div>
  </div>
    <div className={s.dialogs_window}>
    {
      props.dialogs.length > 1 &&
    
    props.dialogs.slice(1).map(e => <DialogsContainer  item = {e}/>)
    }
    <button className={s.add_btn} onClick={() => addChat()}>Add Chat</button>
    </div>
  <div className={s.registration}>
    <div className={s.btn_block}>
  {/* <button className={s.reg_btn}>Log In</button>
  <button className={s.reg_btn}>Registration</button> */}
    </div>
  </div>
   </div>
   <div>

   </div>
  </aside>
  )
}
export default Aside