import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

function LoginForm() {
    const navigate = useNavigate();
    const [validated, setValidated] = useState(false);
    const [form, setForm] = useState({});
    const [error, setError ] = useState(null);
    const inputStyle = {
        marginLeft: "35px",
        marginBottom: "35px",
    }
    const buttonStyle = {
        marginTop: "52px",
        marginLeft: "130px",
        marginBottom: "90px"
    }

    const textStyle = {
        marginTop: "35px",
        marginBottom: "35px",
        marginLeft: "153px",
        marginRight: "152px"
    }

    const iconStyle = {
        marginTop: "75px",
        marginBottom: "35px",
        marginLeft: "182px"
    }

    const textButtonStyle = {
        color: "white",
        fontFamily: "Roboto"
    }


    const handleSubmit = (event) => {
        event.preventDefault();
        const loginForm = event.currentTarget;

        if (loginForm.checkValidity() === false) {
            event.stopPropagation();
        }

        setValidated(true);

        const data = {
            "user": {
                "email": form.username,
                "password": form.password,
            }
        };

        axios
            .post("http://127.0.0.1:8000/api/users/login/", data)
            .then((res) => {
                localStorage.setItem("auth", JSON.stringify({
                    user: res.data.user.email,
                    token: res.data.user.token
                }));

                navigate("/");
            })
            .catch((err) => {
                if (err.message) {
                    setError(err.request.response);
                }
            });
    }
    return (
        <form
            id="loginForm"
            className="loginForm"
            onSubmit={handleSubmit}
            >
            <div className="sign-in-icon" style={iconStyle}>

            </div>
            <div className="sign-in" style={textStyle}>
                    <h2 className="sign-in">Sign in</h2>
            </div>
                    <input
                        id="loginInput"
                        type="text"
                        placeholder="Enter your E-mail"
                        className="input-qa"
                        value={form.username}
                        onChange={(e) => setForm({ ...form, username: e.target.value })}
                        required
                        style={inputStyle}
                    >
                    </input>
                    <input
                        id="passwordInput"
                        type="text"
                        placeholder="Enter your password"
                        className="input-qa"
                        value={form.password}
                        onChange={(e) => setForm({ ...form, password: e.target.value })}
                        required
                        style={inputStyle}>
                    </input>
                    <button
                        id="enterButton"
                        className="enter-button"
                        type="submit"
                        style={buttonStyle}
                        value="Enter">
                        <h5 style={textButtonStyle}>Enter</h5>
                    </button>
            <h2><a className="forgot-password" href="#">Forgot your password?</a></h2>
        </form>
    )
}

export default LoginForm;