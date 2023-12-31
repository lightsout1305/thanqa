import "./sidebar.css";
import { useNavigate } from "react-router-dom";

function Sidebar() {

    const navigate = useNavigate();

    const changeUserIconOnMoveIn = (event) => {
        if (window.location.href.includes('main')) {
            event.target.className = "thanqa-user-icon-on-hover";
        }
    };

    const changeUserIconOnMoveOut = (event) => {
        if (window.location.href.includes('main')) {
            event.target.className = 'thanqa-user-icon-initial';
        }
    };

    const changeSettingsIconOnMoveIn = (event) => {
        if (window.location.href.includes('main')) {
            event.target.className = 'thanqa-settings-icon-on-hover';
        }
    };

    const changeSettingsIconOnMoveOut = (event) => {
        if (window.location.href.includes('main')) {
            event.target.className = 'thanqa-settings-icon-initial';
        }
    };

    const changeExitIconOnMoveIn = (event) => {
        event.target.className = 'thanqa-exit-icon-on-hover';
    };

    const changeExitIconOnMoveOut = (event) => {
        event.target.className = 'thanqa-exit-icon-initial';
    };

    const getUnauthorized = (event) => {
        localStorage.removeItem('auth');
        navigate('/login/');
    }

    return (
        <div className="thanqa-sidebar">
            <div className="thanqa-sidebar-icon"/>
            <div className="thanqa-home-icon"/>
            <div
                className="thanqa-user-icon-initial"
                onMouseMove={changeUserIconOnMoveIn}
                onMouseLeave={changeUserIconOnMoveOut}
            />
            <div
                className="thanqa-settings-icon-initial"
                onMouseMove={changeSettingsIconOnMoveIn}
                onMouseLeave={changeSettingsIconOnMoveOut}
            />
            <div
                className="thanqa-exit-icon-initial"
                onMouseMove={changeExitIconOnMoveIn}
                onMouseLeave={changeExitIconOnMoveOut}
                onClick={getUnauthorized}
            />
        </div>
    )
}

export default Sidebar;