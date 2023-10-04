import './main.css';
import {useState} from "react";


export const Checkbox = () => {
    const [checked, setChecked] = useState(false);

    const handleChange = () => {
        setChecked(!checked);
    }

    return (
        <input className="thanqa-checkbox"
            checked={checked}
            onChange={handleChange}
            type="checkbox"/>
    )
}