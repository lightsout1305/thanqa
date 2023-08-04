import React from 'react';
import LoginForm from "../components/authentication/LoginForm";

function AuthPage() {
    return (
        <div id="authPage">
            <div className="thanqa-logo"/>
            <LoginForm/>
        </div>
    );
}

export default AuthPage;