function showNotification(type, serverResponse) {
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

export default showNotification;