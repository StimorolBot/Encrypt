import "./style/code_input.sass";

import api from "/src/api/api";
import { useState } from "react";
import { Timer } from "../../timer/Timer";
import { MainInput } from "/src/components/ui/input/MainInput";


export const CodeInput = ({email, user_name, error, ...props}) => {
  const delay = 59;
  const [date, setDate] = useState();
  const [seconds, setSeconds] = useState(delay);
  const [isShown, setIsShown] = useState(false);
  
  const codeConfirm = async (event) => {
    event.preventDefault();
    console.log(error)
    
    if ( email && error === undefined) {
      setDate(Date.now());
      setIsShown((state) => ! state);
      await api.post("/auth/email-confirm", userData ).cath((error) => {
        console.log(error)
      });
    }
  }
    
  return(
      <MainInput {...props}>
          <div className="code-input-btn__container">
            <button className="code-input-btn" onClick={(event) => codeConfirm(event)} disabled={isShown} >
              { isShown ? 
                <Timer date={ date } seconds={ seconds } setSeconds={ setSeconds } 
                  setIsShown={ setIsShown } delay={ delay } /> 
                : "Отправить"
              }
            </button>
          </div>
      </MainInput>
    );
}
