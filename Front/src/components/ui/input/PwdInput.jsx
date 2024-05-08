import { useState } from "react";
import { MainInput } from "/src/components/ui/input/MainInput";

import "/src/style/components/ui/input/pwd_input.sass"

export const PwdInput = ({...props}) => {
    const [hidden, setHidden] = useState(true);

    if (hidden)
        props["type"] = "password";
    else
        props["type"]="text";

    return(
        <div className="hidden-btn__container">
            <img className="hidden-btn" 
                src={ hidden ? "/public/eye-solid.svg" : "/public/eye-slash-solid.svg" }
                onClick={() => { setHidden((state) => !state) }}
                alt="hidden-password"
            />
            <MainInput {...props}/>
        </div>
    );
}
