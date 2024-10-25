import { useDispatch, useSelector } from "react-redux"
import { setUserInput } from "../redux/actions";

const UserInput = () => {
    const userInput = useSelector(state => state.userInput)
    const dispatch = useDispatch()

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
          const response = await fetch('http://127.0.0.1:5000/submit', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text: userInput }),
          });
          const data = await response.json();
          console.log(data)
          
        } catch (error) {
          console.error('Error:', error);
        }
      };

    const handleChange = (text) => {
        dispatch(setUserInput(text))

    }

    return (
        <>
        <div className="d-flex justify-content-center">
            <div className="col-5 d-flex justify-content-center flex-column" style={{ minHeight: '100vh' }}>
            <h3>Your comment</h3>
            <div class="text-center">
                    <form onSubmit={handleSubmit}>
                        <div className="mb-3">
                            <input
                            type="text"
                            className="form-control"
                            placeholder="Enter text here"
                            value={userInput}
                            onChange={(e) => handleChange(e.target.value)}
                            />
                        </div>
                        <button type="submit" className="btn btn-primary" onSubmit={() => handleSubmit()}>
                            Submit
                        </button>
                </form>
            </div>
            </div>
        </div>
            
        </>
    )
}

export default UserInput