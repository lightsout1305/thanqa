import React from 'react';
import { Route, Routes } from "react-router-dom";
import './App.css';
import AuthPage from "./pages/Login";
import Login from "./pages/Login";
import ProtectedRoute from "./routes/ProtectedRoute";

function App() {
    return (
        <Routes>
            <Route path="/" element={
                <ProtectedRoute>
                    <AuthPage />
                </ProtectedRoute>} />
            <Route path="/login/" element={ <Login /> } />
        </Routes>
    );
}

export default App;
