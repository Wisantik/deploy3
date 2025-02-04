import axios from "axios";

const api_obj = axios.create({
    baseURL: "http://127.0.0.1:8000/api/",
    withCredentials:true,
})
export const getFields = () => {
    return api_obj.get("fields/")
}
export const postMessage = (message,history_id,session_id,study_field_id) => {
    return api_obj.post("chat/",{"message":message,"history_id":history_id,"session_id":session_id,"study_field_id":study_field_id})
}
export const getChat = (session_id) => {
    return api_obj.get("chat/",{params:{
        session_id
    }})
}
export const getDialogs = (history_id) => {
    return api_obj.get("chats",{params:{history_id}})
}
export const getQuestions = async (id) => {
    let res = api_obj.get("study-field/questions",{params:{field_id:id}})
    return res
}
export const deleteChat = (session_id) => {
        return api_obj.delete('chat/delete',{params:{
            session_id
        }}).catch(e => console.log(e))
}
export const get_title_chat = (session_id) => {
    return api_obj.get("chat/get_chat_title",{params:{session_id}}).catch(e => console.log(e))
}
export const get_titles_history = (history_id) => {
    return api_obj.get("chat/get_chat_titles_by_history_id",{params:{history_id}}).catch(e => console.log(e))
}