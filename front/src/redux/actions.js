import {SET_SENTIMENT, SET_USER_INPUT} from './actionTypes'


export const setUserInput = (userInputData) => {
    return {
        type: SET_USER_INPUT,
        payload: userInputData
    }
}


export const setSentiment = (sentiment) => {
    return {
        type: SET_SENTIMENT,
        payload: sentiment
    }
}
