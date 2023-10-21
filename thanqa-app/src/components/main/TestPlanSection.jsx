import {Text} from "./Text";
import {TestPlanButton} from "./TestPlanButton";
import {CreateTestPlan} from "./CreateTestPlan";
import axios from "axios";
import showNotification from "../notification/notification";
import {useNavigate} from "react-router-dom";
import './main.css';
import {useEffect, useState} from "react";


export const TestPlanSection = () => {
    const navigate = useNavigate();
    const [modal, openModal] = useState(false);
    const token = JSON.parse(localStorage.getItem('auth')).token;
    const config = {
        headers: {
            Authorization: `Bearer ${token}`
        }
    };
    const onClick = (event) => {
        openModal(true);
        const testButton = document.getElementById('testPlanButton');

        if (testButton.textContent === 'Create Test Plan') {
            axios
                .get('http://127.0.0.1:8000/api/users/all/', config)
                .then((res) => {

                })
                .catch((err) => {
                    if (err.response) {
                        showNotification('error', 'Server Error');
                    }
                })
        }
    }

    const onMouseUp = () => openModal(false);
    let modalWindow = null;
    function chooseModal(){
        const testButton = document.getElementById('testPlanButton');
        if (testButton.textContent === 'Create Test Plan') {
            modalWindow = <CreateTestPlan/>;
        }
        return modalWindow;
    }

    const changeTestPlanSection = (buttonText, testPlanTitle, startDate, endDate) => {
        const testPlanButton = document.getElementById('testPlanButton');

        if (buttonText === 'Open Test Plan') {
            if (testPlanButton.textContent !== 'Open Test Plan') {
                const weekDays = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
                const months = ['January', 'February', 'March', 'April', 'May', 'June',
                    'July', 'August', 'September', 'October', 'November', 'December'];
                const testPlanSection = document.getElementById('testPlanSection');
                const testPlanIcon = document.getElementById('testPlanIcon');
                testPlanIcon.style.bottom = '45%';
                const title = document.createElement('p');
                const firstDate = document.createElement('p');
                const finalDate = document.createElement('p');
                title.className = 'thanqa-test-plan-title';
                title.textContent = testPlanTitle;
                const formattedStartDate = new Date(startDate);
                const firstWeekDay = formattedStartDate.getDay();
                const firstDay = formattedStartDate.getDate();
                const firstMonth = formattedStartDate.getMonth();
                const firstYear = formattedStartDate.getFullYear();
                const formattedEndDate = new Date(endDate);
                const finalWeekDay = formattedEndDate.getDay();
                const finalDay = formattedEndDate.getDate();
                const finalMonth = formattedEndDate.getMonth();
                const finalYear = formattedEndDate.getFullYear();
                firstDate.className = 'thanqa-test-plan-datetime';
                firstDate.textContent = `From: ${weekDays[firstWeekDay]} 
                ${firstDay} ${months[firstMonth]} ${firstYear}`;
                finalDate.className = 'thanqa-test-plan-datetime';
                finalDate.textContent = `Till: ${weekDays[finalWeekDay]} 
                ${finalDay} ${months[finalMonth]} ${finalYear}`;
                const first = testPlanSection.insertAdjacentElement('afterbegin', title);
                const second = first.insertAdjacentElement('afterend', firstDate);
                second.insertAdjacentElement('afterend', finalDate);
                testPlanButton.className = 'thanqa-test-plan-button-with-current-test-plan';
            }
        }
        testPlanButton.textContent = buttonText;

    };

    useEffect(() => {
        axios
            .get('http://127.0.0.1:8000/api/testplan/current/', config)
            .then((res) => {
                if (res.data['test_plan']['test_plan_id']) {
                    const testPlanTitle = res.data['test_plan']['title'];
                    const startDate = res.data['test_plan']['start_date'];
                    const endDate = res.data['test_plan']['end_date'];
                    changeTestPlanSection('Open Test Plan', testPlanTitle, startDate, endDate);
                } else {
                    axios
                        .get('http://127.0.0.1:8000/api/testplan/all/', config)
                        .then((res => {
                            if (res.data['test_plan'].length > 0) {
                                changeTestPlanSection('Choose Test Plan');
                            } else {
                                changeTestPlanSection('Create Test Plan');
                            }
                        }))
                        .catch((err) => {
                            if (err.response) {
                                showNotification('error', 'Server Error');
                            }
                        })
                }
            })
            .catch((err) => {
                if (err.response) {
                    if (err.response.status === 403) {
                        localStorage.removeItem('auth');
                        navigate('/login/');
                    } else {
                        showNotification('error', "Server Error");
                    }
                }
            });
        }, []);


    return (
        <div className="thanqa-current-test-plan">
            <Text title="Current Test Plan"/>
            <div
                id="testPlanSection"
                className="thanqa-current-test-plan-short-info">
                <TestPlanButton onClick={onClick} onMouseUp={onMouseUp}/>
                { modal ? chooseModal() : null }
                <div
                    id='testPlanIcon'
                    className="thanqa-test-plan-icon"
                />
            </div>
        </div>
    )
};