export const TestRunCounterTable = () => {
    return (
        <div className="thanqa-test-runs-counter-table">
            <div className="thanqa-test-runs-form">
                <p className="passed-thanqa-test-runs-counter">
                    0
                </p>
                <p className="thanqa-test-runs-counter-text">
                    Test Runs Completed
                </p>
            </div>
            <div className="thanqa-test-runs-form">
                <p className="in-progress-thanqa-test-runs-counter">
                    0
                </p>
                <p className="thanqa-test-runs-counter-text">
                    Test Runs In Progress
                </p>
            </div>
            <div className="thanqa-test-runs-form">
                <p className="blocked-thanqa-test-runs-counter">
                    0
                </p>
                <p className="thanqa-test-runs-counter-text">
                    Test Runs Blocked
                </p>
            </div>
            <div className="thanqa-test-runs-form">
                <p className="failed-thanqa-test-runs-counter">
                    0
                </p>
                <p className="thanqa-test-runs-counter-text">
                    Test Runs Failed
                </p>
            </div>
        </div>
    )
}