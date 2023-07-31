import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import {Button} from "./Button";
import {Input} from "./Input";


function LoginForm() {
    const navigate = useNavigate();
    const [validated, setValidated] = useState(false);
    const [form, setForm] = useState({});
    const [error, setError] = useState(null);
    const inputStyle = {
        marginLeft: "35px",
        marginBottom: "35px"
    };
    const buttonStyle = {
        marginTop: "52px",
        marginLeft: "130px",
        marginBottom: "90px",
        color: "white",
        fontFamily: "Roboto"
    };
    const textStyle = {
        marginTop: "35px",
        marginBottom: "35px",
        marginLeft: "153px",
        marginRight: "152px"
    };

    const iconStyle = {
        marginTop: "75px",
        marginBottom: "35px",
        marginLeft: "182px"
    }

    const handleSubmit = (event) => {
        event.preventDefault();

        setValidated(true);

        if (form.username == null || form.username === "") {
            event.stopPropagation();
            form.error = "Email is required";
            const requiredLogin = document.createElement("p");
            requiredLogin.style.marginTop = "0px";
            requiredLogin.style.marginLeft = "35px";
            requiredLogin.style.marginBottom = "0px";
            requiredLogin.style.color = "#F00";
            requiredLogin.style.fontFamily = "Inter";
            requiredLogin.style.fontSize = "15px";
            requiredLogin.style.fontStyle = "normal";
            requiredLogin.style.fontWeight = "400";
            requiredLogin.style.lineHeight = "normal";
            requiredLogin.textContent = form.error;
            document.getElementById("loginInput").style.border = "2px solid #FE0D0D";
            document.getElementById("loginInput").insertAdjacentElement("beforebegin", requiredLogin);
            document.getElementById("loginInput").style.marginBottom = "14px";
        }

        if (form.password == null || form.password === "") {
            event.stopPropagation();
            form.error = "Password is required";
            const requiredPassword = document.createElement("p");
            requiredPassword.style.marginTop = "0px";
            requiredPassword.style.marginLeft = "35px";
            requiredPassword.style.marginBottom = "0px";
            requiredPassword.style.color = "#F00";
            requiredPassword.style.fontFamily = "Inter";
            requiredPassword.style.fontSize = "15px";
            requiredPassword.style.fontStyle = "normal";
            requiredPassword.style.fontWeight = "400";
            requiredPassword.style.lineHeight = "normal";
            requiredPassword.textContent = form.error;
            document.getElementById("passwordInput").style.border = "2px solid #FE0D0D";
            document.getElementById("passwordInput").insertAdjacentElement("beforebegin", requiredPassword);
            document.getElementById("passwordInput").style.marginBottom = "14px";
        }

        else {

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
    }

    const changeButtonColorMouseIn = (event) => {
        event.target.style.background = "rgba(0, 0, 0, 0.73)";
    }

    const changeButtonColorMouseOut = (event) => {
        event.target.style.background = 'black';
    }

    return (
        <form
            id="loginForm"
            className="loginForm"
            onSubmit={handleSubmit}
            noValidate
            >
            <div className="sign-in-icon" style={iconStyle}>

            </div>
            <div className="sign-in" style={textStyle}>
                    <h2 className="sign-in">Sign in</h2>
            </div>
                    <Input
                        id="loginInput"
                        type="text"
                        placeholder="Enter your E-mail"
                        className="input-qa"
                        value={form.username}
                        onChange={(e) => setForm({ ...form, username: e.target.value })}
                        required
                        style={inputStyle}
                        title="Enter your E-mail"
                    >
                    </Input>
                    <Input
                        id="passwordInput"
                        type="password"
                        placeholder="Enter your password"
                        className="input-qa"
                        value={form.password}
                        onChange={(e) => setForm({ ...form, password: e.target.value })}
                        required
                        style={inputStyle}
                        title="Enter your password"
                        minLength="8">
                    </Input>
                    <Button
                        id="enterButton"
                        value="Enter"
                        type="submit"
                        onMouseMove={changeButtonColorMouseIn}
                        onMouseOut={changeButtonColorMouseOut}
                        style={buttonStyle}
                    />
            <h2><a className="forgot-password" href="#">Forgot your password?</a></h2>
        </form>
    )
}

export default LoginForm;