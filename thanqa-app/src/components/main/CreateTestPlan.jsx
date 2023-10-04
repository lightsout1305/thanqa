import './main.css';
import {Checkbox} from "./Checkbox";

export const CreateTestPlan = () => {
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
                                    <input
                                        className="thanqa-datepicker-input"
                                        placeholder="Select test plan date"
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
                        <div className="thanqa-modal-author">
                                <span className="thanqa-modal-author-placeholder">
                                        Select author
                                </span>
                        </div>
                        <Checkbox/>
                        <p className="thanqa-modal-checkbox-text">
                            Choose this test-plan as current
                        </p>
                </div>
            </div>
        )
}
