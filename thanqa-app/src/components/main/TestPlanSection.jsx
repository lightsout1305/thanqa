import {Text} from "./Text";
import {TestPlanButton} from "./TestPlanButton";

export const TestPlanSection = () => {

    const changeButtonColorOnMoveIn = (event) => {
        event.target.style.background = "rgba(0, 0, 0, 0.73)";
    };

    const changeButtonColorOnMoveOut = (event) => {
        event.target.style.background = '#000';
    }

    return (
        <div className="thanqa-current-test-plan">
            <Text title="Current Test Plan"/>
            <div className="thanqa-current-test-plan-short-info">
                <TestPlanButton
                    onMouseMove={changeButtonColorOnMoveIn}
                    onMouseLeave={changeButtonColorOnMoveOut}
                    text="Create test plan"/>
                <div className="thanqa-test-plan-icon"/>
            </div>
        </div>
    )
}