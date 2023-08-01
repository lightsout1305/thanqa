import React from 'react';
import {BrowserRouter, Route, Routes} from "react-router-dom";
import './App.css';
import Login from "./pages/Login";
import ProtectedRoute from "./routes/ProtectedRoute";
import NotificationContainer from "react-notifications";
import Main from "./pages/Main";

function App() {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/" element={
                    <ProtectedRoute>
                        <Main />
                    </ProtectedRoute>} />
                <Route path="/login/" element={ <Login /> } />
            </Routes>
            <NotificationContainer />
        </BrowserRouter>
    );
}

export default App;
