export const NotificationQA = ({type, description}) => {
    if (type === "successful") {
        return (
        <div id="successNotification" className={`notification__${type}`}>
            <p className="notification__text">
                {description}
            </p>
            <div className="notification__icon"/>
        </div>
        )
    }
}