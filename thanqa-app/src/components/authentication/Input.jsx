export const Input = (
    { type, id, placeholder, value, onChange, style, title, minLength, className }) => {
    return (
        <input
            id={id}
            type={type}
            className={className}
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


