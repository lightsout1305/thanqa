import {Input} from "./Input";

export const Form = (
    {formId, onSubmit, formClassName, type, placeholder, inputId, inputStyle, onChange, value } ) => {
    return (
        <form
            id={formId}
            onSubmit={onSubmit}
            className={formClassName}
        >
            <Input
                id={inputId}
                type={type}
                placeholder={placeholder}
                style={inputStyle}
                onChange={onChange}
                value={value}>
            </Input>
            <Input
                id={inputId}
                type={type}
                placeholder={placeholder}
                style={inputStyle}
                onChange={onChange}
                value={value}>
            </Input>
        </form>
    )
}