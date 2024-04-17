import "/src/style/components/ui/input/btn_input.sass";

export function BtnInput({file_name, btn_name, ...props}){

    return(
        <div className="btn-input__container">
            <span className="btn-input__file-name-container">
                <p className="btn-input__file-name">{ file_name }</p>
            </span>
            <label className="btn-input__btn-name-container" htmlFor={props.id}>
                <p className="btn-input__btn-name">{ btn_name }</p>
            </label>
                
            <input className="btn-input" {...props} />
        </div>
    );
}
