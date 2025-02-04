import { getQuestions } from "../../API/api";

const initial_state = {
  prompt: [{ id: 0, example: "", field: 0 },],
};
const SET_PROMPT = "SET_PROMPT"
const PromptReducer = (state = initial_state, action) => {
  switch (action.type) {
    case SET_PROMPT:
    return {
        ...state,
        prompt:action.prompt
    }
    default:
      return state;
  }
};
export const setPrompt = (prompt) => ({
  type: SET_PROMPT,
  prompt,
});
export const PromptThunk = (field_id) => async (dispatch) => {
  try {
    let res = await (await getQuestions(field_id)).data
    dispatch(setPrompt(res))
  } catch (error) {
    console.log(error)
  }
}
export default PromptReducer
