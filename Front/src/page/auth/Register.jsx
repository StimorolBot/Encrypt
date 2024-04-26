import api from "/src/api/api";
import { useState } from "react";
import { MainBtn } from "/src/components/ui/btn/MainBtn";
import { MainForm } from "/src/components/ui/form/MainForm";
import { MainInput } from "/src/components/ui/input/MainInput";

import "/src/style/components/page/auth/register.sass";


export function Register() {
    const [userData, setUserData] = useState(
        {"user_name": "", "email": "", "password": ""});
    

    const postRegister = async (event) => {
        event.preventDefault();
        
        await api.post("/auth/register", userData).then((response) => {
            console.log(response.data);
            })
            .catch((error) =>{
                console.log(error);
            }
        );
    };

    return (
        <div className="wrapper register__wrapper">
            <MainForm onSubmit={postRegister}>
                <div className="register-input__container">
                    <MainInput lblText={"Имя"} maxLength={16} 
                        type="text" placeholder=" " required
                        onChange={(event) => setUserData(
                            {...userData, user_name: event.target.value}
                        )}
                    />
                    <MainInput lblText={"Логин"} maxLength={24}
                        type="email" placeholder=" " required
                        onChange={(event) => setUserData(
                            {...userData, email: event.target.value}
                        )}
                    />
                    <MainInput lblText={"Код подтверждения"} maxLength={24}
                        type="text" placeholder=" " required
                    />
                    <MainInput lblText={"Пароль"} maxLength={24}
                        type="password" placeholder=" " required
                        onChange={(event) => setUserData(
                            {...userData, password: event.target.value}
                        )}
                    />
                    <MainInput lblText={"Подтвердите пароль"} maxLength={24}
                        type="password" placeholder=" " required
                    /> 
                </div>
                
                <div className="register__form-help">
                        
                </div>   
                <MainBtn>Зарегистрироваться</MainBtn>
            </MainForm>
        </div>
    );
}
