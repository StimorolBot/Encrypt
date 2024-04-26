import "/src/style/components/ui/input/main_input.sass"

export function MainInput({lblText, ...props}) {
    return(
        <div className="input__container">
            <input className="input-main" {...props}/>
            <label className="input-lbl">
                <p className="input-lbl-text">{lblText}</p>
            </label>
        </div>
    );
};
