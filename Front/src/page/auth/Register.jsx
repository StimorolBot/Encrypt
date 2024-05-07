import api from "/src/api/api";
import { useState } from "react";
import { Link } from "react-router-dom";
import { MainBtn } from "/src/components/ui/btn/MainBtn";
import { MainForm } from "/src/components/ui/form/MainForm";
import { PwdInput } from "../../components/ui/input/PwdInput";
import { MainInput } from "/src/components/ui/input/MainInput";
import { CodeInput } from "/src/components/ui/input/CodeInput";

import "/src/style/components/page/auth/register.sass";


export function Register() {
    const [userData, setUserData] = useState(
        {"user_name": "", "email": "", "password": "", "code_confirm": ""});
    

    const registerUser = async (event) => {
        event.preventDefault();
        await api.post("/auth/register", userData);
    };

    const codeConfirm = async (event) =>{
        event.preventDefault();
        
        if (userData["email"] && userData["user_name"]){
            await api.post("/auth/email-confirm", 
                { "user_name": userData["user_name"], "email":userData["email"] }
            )
        }
    }

    return (
        <div className="wrapper register__wrapper">
            <MainForm onSubmit={ registerUser }>
                <section className="register-input__container">
                    <MainInput lblText={ "Имя" } maxLength={16} type="text"
                        required onChange={(event) => setUserData(
                            {...userData, user_name: event.target.value}
                        )}
                    />
                    <MainInput lblText={ "Логин" } maxLength={24} type="email"
                        required onChange={(event) => setUserData(
                            {...userData, email: event.target.value}
                        )}
                    />
                    <CodeInput lblText={ "Код подтверждения" } maxLength={6} type="text"
                    required func={ codeConfirm } onChange={(event) => setUserData(
                        {...userData, code_confirm: event.target.value}
                    )}/>
                    <PwdInput lblText={ "Пароль" } maxLength={24}
                        type="password" required
                        onChange={(event) => setUserData(
                            {...userData, password: event.target.value}
                        )}
                    />
                    <PwdInput lblText={ "Подтвердите пароль" } maxLength={24}
                        type="password" required
                    /> 
                </section>
                
                <section className="register__go-to-login">
                    <Link className="register__link-login" to="/auth/login">
                        Уже есть учетная запись 
                    </Link>
                </section>

                <div className="register__btn">   
                    <MainBtn>Зарегистрироваться</MainBtn>
                </div>
            </MainForm>
        </div>
    );
}
