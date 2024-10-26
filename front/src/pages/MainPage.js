import { useDispatch, useSelector } from "react-redux"
import UserInput from '../components/UserInput'
import Sentiment from '../components/Sentiment'

const MainPage = () => {
    const sentiment = useSelector(state => state.sentiment)
    const userInput = useSelector(state => state.userInput)
    return (
        <>
            {!sentiment && <UserInput />}
            {sentiment && <Sentiment sentiment={sentiment} userInput={userInput} />}
        </>
    )
}

export default MainPage