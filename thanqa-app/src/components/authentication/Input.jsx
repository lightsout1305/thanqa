export const Input = ({ type, id, placeholder, value, onChange, style, title, minLength }) => {
    return (
        <input
            id={id}
            type={type}
            className="input-qa placeholder: opacity-70"
            placeholder={placeholder}
            value={value}
            style={style}
            onChange={onChange}
            required
            title={title}
            minLength={minLength}
        />
    )
}


