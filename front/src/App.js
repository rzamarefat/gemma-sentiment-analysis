import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom"
import { Provider } from 'react-redux'
import Store from './redux/store'

import MainPage from "./pages/MainPage"


const App = () => {
    return (
        <Provider store={Store}>
            <Router>
                <Routes>
                    <Route path="/" element={<MainPage />} />
                </Routes>
            </Router>
        </Provider>
        
        
    )
}


export default App