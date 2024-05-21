import "./style/register.sass";

import api from "/src/api/api";
import { useState } from "react";
import { Link } from "react-router-dom";
import { useForm } from "react-hook-form";
import { MainBtn } from "../../components/ui/btn/MainBtn";
import { MainForm } from "../../components/ui/form/MainForm";
import { PwdInput } from "../../components/ui/input/PwdInput";
import { MainInput } from "../../components/ui/input/MainInput";
import { CodeInput } from "../../components/ui/input/CodeInput";


export function Register() {
    const [email, setEmail] = useState("");
    const { register, handleSubmit, reset, formState: { errors, isValid }} = useForm({mode: "onBlur"});

    const registerUser = async ( formData ) => {
        await api.post("/auth/register", formData);
    };
    
    return (
        <MainForm onSubmit={ handleSubmit(registerUser) }>
            <div className="wrapper register__wrapper">
                <section className="register-input__container">
                    <MainInput lblText={ "Имя" } maxLength={ 20 } type="text" required
                        register={ register("user_name", {
                            minLength: { value: 4, message: "Длинна поля должна быть от 4 символов" }
                        })} errorsMessage={errors?.user_name?.message} 
                        onChange={(event) => setUserData(
                            {...userData, user_name: event.target.value}
                        )}
                    />
                   
                    <MainInput lblText={ "Логин" } maxLength={ 30 } required
                        register={register("email", {
                            minLength: { value: 8, message: "Длинна поля должна быть от 8 символов" },
                            pattern: { value: /(^[a-zA-Z0-9_-]+@[mail|gmail|]+\.[ru|com]+)/, message: "Неверный формат почты" }
                        })} errorsMessage={errors?.email?.message} 
                        onChange={(event) => setEmail(event.target.value)}
                    />

                    <CodeInput lblText={ "Код подтверждения" } maxLength={ 6 } type="text" required
                        email={ email } error={ errors?.email?.message }
                        register={register("code_confirm", {
                            minLength: { value: 6, message: "Длинна поля должна быть 6 символов" }
                        })} errorsMessage={errors?.code_confirm?.message} 
                    />

                    <PwdInput lblText={ "Пароль" } maxLength={ 24 } type="password" required
                        register={register("password", {
                            minLength: { value: 4, message: "Длинна поля должна быть 4 символов" }
                        })} errorsMessage={errors?.password?.message} 
                    />

                    <PwdInput lblText={ "Подтвердите пароль" } maxLength={ 24 } type="password" required
                        register={register("password_confirm", {
                            minLength: { value: 4, message: "Длинна поля должна быть 4 символов" },
                        })} errorsMessage={errors?.password_confirm?.message} 
                    /> 
                </section>
                
                <Link className="register__link-login" to="/auth/login">
                    Уже есть учетная запись 
                </Link>

                <div className="register__btn">   
                    <MainBtn >Зарегистрироваться</MainBtn>
                </div>
            </div>
        </MainForm>
    );
}
