import initialState from "./initiaState"
import { SET_USER_INPUT } from "./actionTypes";


const reducer = (state = initialState, action) => {
    switch (action.type) {
        case SET_USER_INPUT:
            return {
                ...state, userInput: action.payload
            }

        default:
            return state;
    }

}


export default reducer