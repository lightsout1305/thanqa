export const Input = ({ type, id, placeholder, value, onChange }) => {
    return (
        <input
            id={id}
            type={type}
            className="input-qa placeholder: opacity-50"
            placeholder={placeholder}
            value={value}
            onChange={onChange}
        />
    )
}


