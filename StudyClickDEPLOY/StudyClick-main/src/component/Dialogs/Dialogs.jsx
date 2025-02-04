import React from "react";
import s from './Dialogs.module.css'
import { NavLink } from "react-router-dom";
const Dialogs = ({setId,item,deleteDialog}) => {
    return (
            <NavLink className={data => data.isActive ? s.navigate_active :s.navigate} to={"/dialog/" + item.session_id} onClick={() => setId(item.session_id)}>
            <div className={s.dialog}>
                <div>{item.title}</div>
                <img onClick={() => deleteDialog(item.session_id)} className={s.delete_btn} src="https://cdn-icons-png.flaticon.com/512/1345/1345823.png" alt="" />
                </div>
                </NavLink>
        
    )
}
export default Dialogs