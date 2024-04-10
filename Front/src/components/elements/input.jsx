import "/src/style/elements/input.sass"

export function Input({lblText,  maxLen, setVal, type}) {
    return(
        <div className="input__container">
            <input className="input-main" type={type} required autoComplete="off"
            minLength="4" maxLength={maxLen} onChange={(event) => setVal(event.target.value)}/>
            <label className="input-lbl">{lblText}</label>
        </div>
    );
};
