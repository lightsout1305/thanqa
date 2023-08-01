import "./notification.css";

export const Notification = ({ type, description }) => {
    return (
        <div className={`notification notification__${type}`}>
            <p className="notification__text">
                {description}
            </p>
            <img src="../../Check_round_fill.svg" alt="success" />
        </div>
    )
}