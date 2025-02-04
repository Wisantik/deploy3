import React, { useEffect } from "react"
import s from "./App.module.css"
import Aside from "./component/Aside/Aside";
import LearnContainer from "./component/Learn/LearnContainer";
import { v4 as uuidv4 } from 'uuid';
import AsideContainer from "./component/Aside/AsideContainer";
import { Route, Routes } from "react-router-dom";
import DialogContainer from "./component/Dialog/DialogContainer";
import Home from "./component/Home/Home";
import { getDialogsHistoryChat, setHistory_id } from "./redux/reducers/DIalogsReducer";
import { connect } from "react-redux";
function App(props) {
   useEffect(() => {
    let history_id = localStorage.getItem('history_id');
      if (!history_id){
        let history_id = uuidv4(); // функция для генерации UUID
        localStorage.setItem('history_id', history_id);
      }
      props.getDialogsHistoryChat(history_id)
      props.setHistory_id(history_id)
   },[])
  return (
    <div className={s.App}>
      <AsideContainer />
      
      <Routes>
      <Route path="/" element={<LearnContainer/>}/>
      <Route path="/dialog/:id?" element={<DialogContainer/>}/>
      <Route path="/" element={<Home/>}/>
      
      </Routes>
    </div>
  );
}
const mapStateToProps = (state) => ({
  historyId:state.dialogs.history_id
})
export default connect(mapStateToProps,{setHistory_id,getDialogsHistoryChat})(App);
