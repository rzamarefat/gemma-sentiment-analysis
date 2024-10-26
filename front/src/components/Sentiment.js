import { useDispatch, useSelector } from "react-redux"
import { setSentiment, setUserInput } from "../redux/actions";

const Sentiment = ({sentiment, userInput}) => {
    const dispatch = useDispatch()


    const handleClick = () => {
        dispatch(setSentiment(null))
        dispatch(setUserInput(""))
    }

    return (
        <>
        <div className="d-flex justify-content-center">
            <div className="col-5 d-flex justify-content-center flex-column" style={{ minHeight: '100vh' }}>
            <div class="text-center">
                <h1>
                <p>The sentiment for <strong className="text-danger">{userInput}</strong> is  <strong className="text-danger">{sentiment}</strong></p>    
                </h1>
                <button type="button" className="btn btn-dark" onClick={handleClick}>Back to home</button>
                
            </div>
            </div>
        </div>
            
        </>
    )
}

export default Sentiment