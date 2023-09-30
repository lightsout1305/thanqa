import './main.css';
import {Text} from "./Text";
import {Search} from "./Search";
import {NoContentText} from "./NoContentText";

export const TestCasesTable = () => {
    const changeAddTestRunIconOnMoveIn = (event) => {
        event.target.className = 'thanqa-add-test-case-icon-on-hover';
    };

    const changeAddTestRunIconOnMoveOut = (event) => {
        event.target.className = 'thanqa-add-test-case-icon-initial';
    };

    return (
        <div className="thanqa-test-cases">
            <Text title="Test Runs"/>
            <div
                className="thanqa-add-test-case-icon-initial"
                onMouseMove={changeAddTestRunIconOnMoveIn}
                onMouseLeave={changeAddTestRunIconOnMoveOut}
            />
            <Search id="searchInput" placeholder="Search test runs by title"/>
            <NoContentText text="No Test Runs Yet..."/>
        </div>
    )
}
