import { MainInput } from "/src/components/ui/input/MainInput";

import "/src/style/components/ui/input/code_input.sass";

export const CodeInput = ({func, ...props}) => {
    return(
      <MainInput {...props}>
        <div className="code-input-btn__container">
            <p className="code-input-btn" onClick={ func }>
                Отправить
            </p>
        </div>
      </MainInput>
    );
}
