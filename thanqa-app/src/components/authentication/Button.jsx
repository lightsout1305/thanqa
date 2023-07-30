export const Button = ({ id, value, onMouseMove, onMouseOut, type, style }) => {
    return (
        <button
            type={type}
            id={id}
            onMouseMoveCapture={onMouseMove}
            onMouseOut={onMouseOut}
            className="enter-button"
            style={style}
        >
            {value}
        </button>
    )
}
