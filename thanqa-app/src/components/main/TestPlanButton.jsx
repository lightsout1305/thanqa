export const TestPlanButton = ({text, onClick, onMouseUp}) => {

    const changeButtonColorOnMoveIn = (event) => {
        event.target.style.background = "rgba(0, 0, 0, 0.73)";
    };

    const changeButtonColorOnMoveOut = (event) => {
        event.target.style.background = '#000';
    };

    return (
        <button
            id="testPlanButton"
            className="thanqa-test-plan-button-no-current-test-plan"
            type="submit"
            onMouseMove={changeButtonColorOnMoveIn}
            onMouseLeave={changeButtonColorOnMoveOut}
            onMouseUp={onMouseUp}
            onClick={onClick}
        >
            {text}
        </button>
    )
}