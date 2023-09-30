import React from "react";
import Sidebar from "../components/sidebar/Sidebar";
import {TestCasesTable} from "../components/main/TestCasesTable";
import {TestRunCounterTable} from "../components/main/TestRunCounterTable";
import {TestPlanSection} from "../components/main/TestPlanSection";

function ThanQAMain() {
    return (
        <div className="main">
            <Sidebar/>
            <TestCasesTable/>
            <TestRunCounterTable/>
            <TestPlanSection/>
        </div>
    )
}

export default ThanQAMain;