import {Input} from "./Input";

export const Form = ( {id, onSubmit, className} ) => {
    return (
        <form
            id={id}
            onSubmit={onSubmit}
            className={className}
        >
            <Input onChange={null}>

            </Input>
        </form>
    )
}