export const Search = ({id, placeholder}) => {
    return (
        <div className="thanqa-search">
            <div className="thanqa-search-icon">
                <input
                    id={id}
                    className="thanqa-search-input"
                    placeholder={placeholder}
                />
            </div>
        </div>
    )
}