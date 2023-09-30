import './main.css';

export const Text = ({title, style}) => {
    return (
        <p className="thanqa-text" style={style}>
            {title}
        </p>
    )
}