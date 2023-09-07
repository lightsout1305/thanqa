import React from "react";
import Sidebar from "../components/sidebar/Sidebar";
import TestCasesTable from "../components/main/TestCasesTable";

function Main() {
    return (
        <div className="main">
            <Sidebar/>
            <TestCasesTable/>
        </div>
    )
}

export default Main;