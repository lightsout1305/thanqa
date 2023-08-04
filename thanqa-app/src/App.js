import React from 'react';
import {BrowserRouter, Route, Routes} from "react-router-dom";
import './App.css';
import Login from "./pages/Login";
import ProtectedRoute from "./routes/ProtectedRoute";
import Main from "./pages/Main";

function App() {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/main/" element={
                    <ProtectedRoute>
                        <Main />
                    </ProtectedRoute>} />
                <Route path="/login/" element={ <Login /> } />
            </Routes>
        </BrowserRouter>
    );
}

export default App;
