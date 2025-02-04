import React from "react";
import Dialog from "./Dialog";
import { connect } from "react-redux";
import {
  createMessage,
  getHistoryChat,
  setTitleChat,
} from "../../redux/reducers/MessageReducer";
import { PromptThunk } from "../../redux/reducers/PromptReducer";
const DialogContainer = (props) => {
  return (
    <Dialog
      message={props.message}
      session_id={props.session_id}
      createMessage={props.createMessage}
      getHistoryChat={props.getHistoryChat}
      study_field_id={props.study_field_id}
      historyId={props.historyId}
      prompt = {props.prompt}
      PromptThunk = {props.PromptThunk}
      active = {props.active}
      setTitleChat = {props.setTitleChat}
    />
  );
};
const mapStateToProps = (state) => ({
  message: state.messages.messages_data.message,
  session_id: state.messages.messages_data.session_id,
  study_field_id: state.learn.current_field.id,
  historyId: state.dialogs.history_id,
  prompt: state.prompt.prompt,
  active:state.messages.messages_data.active
});
export default connect(mapStateToProps, { createMessage, getHistoryChat, PromptThunk, setTitleChat })(
  DialogContainer
);
