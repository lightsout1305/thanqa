export const TestPlanButton = ({text, onMouseMove, onMouseLeave}) => {
    return (
        <button
            className="thanqa-test-plan-button"
            type="submit"
            onMouseMove={onMouseMove}
            onMouseLeave={onMouseLeave}
        >
            {text}
        </button>
    )
}