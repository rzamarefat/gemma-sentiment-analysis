import {SET_USER_INPUT} from './actionTypes'


export const setUserInput = (userInputData) => {
    return {
        type: SET_USER_INPUT,
        payload: userInputData
    }
}