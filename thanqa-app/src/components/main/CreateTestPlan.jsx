import './main.css';
import {Checkbox} from "./Checkbox";
import {useState} from "react";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import {AuthorsList} from "./AuthorsList";


export const CreateTestPlan = () => {
    const [authors, setAuthors] = useState(false);
    const clickOnAuthors = (event) => {
        const authorsListIcon = document.getElementById('thanqaAuthorsListIcon');
        if (!authors) {
            setAuthors(true);
            authorsListIcon.className = 'thanqa-authors-list-expanded';
        }
        else {
            setAuthors(false);
            authorsListIcon.className = 'thanqa-authors-list-hidden';
        }
    };
    const changeCloseIconColorOnMoveIn = (event) => {
        event.target.className = "thanqa-close-modal-on-hover";
    }
    const changeCloseIconOnMoveOut = (event) => {
        event.target.className = "thanqa-close-modal";
    }
    const closeModal = () => {
        const parentComponent = document.getElementById('createTestPlan');
        const modalWindow = document.getElementById('createTestPlanModal');
        parentComponent.removeChild(modalWindow);
    }

    const [startDate, setStartDate] = useState(new Date());
    const [endDate, setEndDate] = useState(null);
    const onChange = (dates) => {
        const [start, end] = dates;
        setStartDate(start);
        setEndDate(end);
    };

    return (
        <div id="createTestPlan">
            <div id="createTestPlanModal"
                className="thanqa-create-test-plan">
                <div className="thanqa-close-modal"
                     onClick={closeModal}
                     onMouseMove={changeCloseIconColorOnMoveIn}
                     onMouseLeave={changeCloseIconOnMoveOut}
                />
                <p className="thanqa-modal-header">
                        Create Test Plan
                </p>
                <p className="thanqa-modal-input-title-description">
                        Title
                </p>
                <input
                    className="thanqa-modal-title-input"
                    placeholder="Enter test plan title"
                />
                <p className="thanqa-modal-datepicker-description">
                    Date
                </p>
                <div className="thanqa-datepicker-background">
                    <div className="thanqa-datepicker-icon">
                        <DatePicker
                            className="thanqa-datepicker-input"
                            placeholderText="Select test plan date"
                            onChange={onChange}
                            selected={startDate}
                            startDate={startDate}
                            endDate={endDate}
                            selectsRange
                            showDisabledMonthNavigation
                            dateFormat="dd.MM.yyyy"
                        />
                    </div>
                </div>
                <p className="thanqa-modal-content-description">
                    Description
                </p>
                <textarea
                    className="thanqa-modal-content"
                    placeholder="Enter test plan description"
                />
                    <p className="thanqa-modal-author-description">
                        Author
                    </p>
                    <div
                        className="thanqa-modal-author"
                        onClick={clickOnAuthors}
                    >
                        <span className="thanqa-modal-author-placeholder">
                            Select author
                        </span>
                        <div
                            id="thanqaAuthorsListIcon"
                            className="thanqa-authors-list-hidden"/>
                        { authors ? <AuthorsList/> : null }
                    </div>
                    <Checkbox/>
                    <p className="thanqa-modal-checkbox-text">
                        Choose this test-plan as current
                    </p>
            </div>
        </div>
    )
}
