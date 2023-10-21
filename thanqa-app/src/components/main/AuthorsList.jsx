import './main.css';
import axios from "axios";
import showNotification from "../notification/notification";
import {useEffect, useState} from "react";

export const AuthorsList = () => {
    const [users, setUsers] = useState([]);
    const token = JSON.parse(localStorage.getItem('auth')).token;
    const config = {
        headers: {
            Authorization: `Bearer ${token}`
        }
    };

    const onHover = (event) => {
        event.target.style.background = 'rgba(217, 217, 217, 0.22)';
    };

    const onLeave = (event) => {
        event.target.style.background = '#FFFFFF';
    }

    useEffect(() => {
        axios
            .get('http://127.0.0.1:8000/api/users/all/', config)
            .then((res) => {
                setUsers(res.data["users"]);
            })
            .catch((err) => {
                if (err.response) {
                    showNotification('error', 'Server Error');
                }
        })
    }, [])


    return (
        <div className="thanqa-authors-list">
            {users ? users.map((user) => {
                return (
                    <div
                        defaultValue="Lele"
                        key={user.id}
                        className="thanqa-author-field"
                        onMouseMove={onHover}
                        onMouseLeave={onLeave}
                    >
                        <span
                            className="thanqa-author"
                        >
                            {user["first_name"] + " " + user["last_name"]}
                        </span>
                    </div>
                );
            }) : null}
        </div>
    )
}