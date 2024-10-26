import initialState from "./initiaState"
import { SET_USER_INPUT, SET_SENTIMENT } from "./actionTypes";


const reducer = (state = initialState, action) => {
    switch (action.type) {
        case SET_USER_INPUT:
            return {
                ...state, userInput: action.payload
            }
        
        case SET_SENTIMENT:
            return {
                ...state, sentiment: action.payload
            }

        default:
            return state;
    }

}


export default reducer