import React, {useState} from "react";
import axios from "axios";
import {useNavigate} from "react-router-dom";
import {Icon} from 'react-icons-kit';
import {eyeOff} from 'react-icons-kit/feather/eyeOff';
import {eye} from 'react-icons-kit/feather/eye';
import {Button} from "./Button";
import {Input} from "./Input";
import "./notification.css";
import "./login_page.css";

function LoginForm() {
    const navigate = useNavigate();
    const [form, setForm] = useState({});
    const [type, setType] = useState('password');
    const [icon, setIcon] = useState(eyeOff);

    const handleToggle = () => {
        if (type==='password'){
            setIcon(eye);
            setType('text')
        } else {
            setIcon(eyeOff)
            setType('password')
        }
    }

    const showNotification = (type, serverResponse) => {
        if (type === 'successful') {
            const notification = document.createElement('div');
            notification.id = "successNotification";
            notification.className = "notification__successful";
            const notificationText = document.createElement('p');
            notificationText.textContent = "Authorization successful";
            notificationText.className = "notification__text";
            const notificationIcon = document.createElement('div');
            notificationIcon.className = "notification__successful__icon";
            document.getElementById("root").insertAdjacentElement('afterend', notification);
            notification.insertAdjacentElement('beforeend', notificationText);
            notification.insertAdjacentElement('beforeend', notificationIcon);
            setTimeout(function () {
                notification.remove()
            }, 2000);
        }

        if (type === 'error') {
            const notification = document.createElement('div');
            notification.id = "errorNotification";
            notification.className = "notification__error";
            const notificationText = document.createElement('p');
            notificationText.textContent = serverResponse;
            notificationText.className = "notification__text";
            const notificationIcon = document.createElement('div');
            notificationIcon.className = "notification__error__icon";
            document.getElementById("root").insertAdjacentElement('afterend', notification);
            notification.insertAdjacentElement('beforeend', notificationText);
            notification.insertAdjacentElement('beforeend', notificationIcon);
            setTimeout(function () {
                notification.remove()
            }, 2000);
        }
    }

    const handleSubmit = (event) => {
        event.preventDefault();

        if (form.username == null || form.username === "") {
            event.stopPropagation();
            form.error = "Email is required";
            const checkWarning = document.getElementById("requiredLogin");
            if (checkWarning == null) {
                const requiredLogin = document.createElement("p");
                requiredLogin.id = "requiredLogin";
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
                document.getElementById("loginInput").style.width = "343px";
                document.getElementById("loginInput").style.height = "68px";
                document.getElementById("loginInput").insertAdjacentElement("beforebegin", requiredLogin);
                document.getElementById("loginInput").style.marginBottom = "13px";
                document.getElementById("loginInput").addEventListener("input",
                    function (event) {
                    requiredLogin.remove();
                    document.getElementById("loginInput").style.border = null;
                    document.getElementById("loginInput").style.marginBottom = "35px";
                })
            }
        }

        if (form.password == null || form.password === "") {
            event.stopPropagation();
            form.error = "Password is required";
            const checkWarning = document.getElementById("requiredPassword");
            if (checkWarning == null) {
                const requiredPassword = document.createElement("p");
                requiredPassword.id = "requiredPassword";
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
                document.getElementById("embeddedInput").style.border = "2px solid #FE0D0D";
                document.getElementById("embeddedInput").style.marginBottom = "15px";
                document.getElementById("embeddedInput").insertAdjacentElement("beforebegin",
                    requiredPassword);
                document.getElementById("embeddedInput").style.marginBottom = "-24px";
                document.getElementById("passwordInput").addEventListener("input",
                    function (event) {
                    requiredPassword.remove();
                    document.getElementById("embeddedInput").style.border = null;
                    document.getElementById("embeddedInput").style.marginBottom = "0px";
                })
            }
        }

        else if ((form.username != null && form.username !== "") && (form.password != null && form.password !== "")) {
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
                    navigate("/main/");
                })
                .catch((err) => {
                    if (err.response.data["user"]["errors"]["email"]) {
                        showNotification("error", err.response.data["user"]["errors"]["email"]);
                    }
                    else if (err.response.data["user"]["errors"]["password"]) {
                        showNotification("error", err.response.data["user"]["errors"]["password"]);
                    }
                    else {
                        showNotification("error", err.response.data["user"]["errors"]["error"]);
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
            <div className="sign-in-icon"/>
            <div className="sign-in">
                <p>Sign in</p>
            </div>
            <Input
                id="loginInput"
                type="text"
                placeholder="Enter your E-mail"
                className="input-qa"
                value={form.username}
                onChange={(e) => setForm({ ...form, username: e.target.value })}
                required
                title="Enter your E-mail"
            >
            </Input>
            <div id="embeddedInput" className="embedded-input">
                <Input
                    id="passwordInput"
                    type={type}
                    placeholder="Enter your password"
                    className="input-password-qa"
                    value={form.password}
                    onChange={(e) => setForm({ ...form, password: e.target.value })}
                    required
                    title="Enter your password"
                    minLength="8"
                >
                </Input>
                <span onClick={handleToggle}>
                    <Icon className="absolute mr-10" icon={icon} size={25}/>
                </span>
            </div>
            <Button
                id="enterButton"
                value="Enter"
                type="submit"
                onMouseMove={changeButtonColorMouseIn}
                onMouseOut={changeButtonColorMouseOut}
            />
            <h2><a className="forgot-password" href="#">Forgot your password?</a></h2>
        </form>
    )
}

export default LoginForm;