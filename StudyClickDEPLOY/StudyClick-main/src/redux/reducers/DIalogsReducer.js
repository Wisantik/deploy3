import { deleteChat, get_titles_history } from "../../API/api";
import { Clear_chat } from "./MessageReducer";

let initial_state = {
  dialogs_data: [
    { title: "main chat", session_id: 1},
  ],
  history_id: null,
  dialogs_history:[]
};
const SET_DIALOGS_TITLE_HISTORY = "SET_DIALOGS_TITLE_HISTORY"
const DELETE_CHAT = "DELETE_CHAT"
const SET_HISTORY_ID = "SET_HISTORY_ID"
const ADD_DIALOGS = "ADD_DIALOGS";
const CHANGE_TITLE = "CHANGE_TITLE"
const DialogsReducer = (state = initial_state, action) => {
  switch (action.type) {
    case ADD_DIALOGS: {
      return {
        ...state,
        dialogs_data: [
          ...state.dialogs_data,
          { title: action.name, session_id: action.id },
        ],
      };
    }
    case SET_DIALOGS_TITLE_HISTORY:
      return{
        ...state,
        dialogs_data:action.titles
      }
      case CHANGE_TITLE:
        return{
          ...state,
          dialogs_data: 
            state.dialogs_data.map(e => 
              e.session_id === action.session_id ?
              {...e,title:action.title}:
              e
            ),
          
        }
        case SET_HISTORY_ID:
          return {
            ...state,
            history_id: action.history_id
          }
          case DELETE_CHAT:
            return {
              ...state,
              dialogs_data: state.dialogs_data.filter(e => e.session_id !== action.id)
            }
            default: 
            console.log(state)
              return state;
            }
};
export const onChangeTitle = (session_id,title) => ({
  type: CHANGE_TITLE,
  session_id,
  title
})
export const setTitlesHistory = (titles) => ({
  type:SET_DIALOGS_TITLE_HISTORY,
  titles
})
export const delDialog = (id) => ({
  type:DELETE_CHAT,
  id
})
export const setHistory_id = (history_id) => ({
  type: SET_HISTORY_ID,
  history_id
})
export const AddDialogs = (name, id) => ({
  type: ADD_DIALOGS,
  name,
  id,
});
export const getDialogsHistoryChat = (history_id) => async (dispatch) => {
  try {
    let res = await get_titles_history(history_id)
    dispatch(setTitlesHistory(res.data.chats))
  } catch (error) {
    
  }

}
export const deleteDialog = (id) => (dispatch) => {
  try {
    deleteChat(id)
    dispatch(Clear_chat())
    dispatch(delDialog(id))
  } catch (error) {
    console.log(error)
  }
}
export default DialogsReducer;
