import api from "/src/api/api";
import cookies from "/src/api/cookies";
import { Link } from "react-router-dom";
import { useForm } from "react-hook-form";
import { MainBtn } from "/src/components/ui/btn/MainBtn";
import { MainForm } from "/src/components/ui/form/MainForm";
import { PwdInput } from "../../components/ui/input/PwdInput";
import { MainInput } from "/src/components/ui/input/MainInput";

import "/src/style/components/page/auth/login.sass";


export function Login() {
    const { register, handleSubmit, reset, formState: { errors, isValid }} = useForm({mode: "onBlur"});
 
    const loginUser = async (event) => {
        event.preventDefault();
        
        await api.post("/auth/login", userData)
            .then((response) => {
                localStorage.setItem("access_token", response.data["access_token"]);
                cookies.set("refresh_token", response.data["refresh_token"],
                    { maxAge: response.data["refresh_max_age"] }
                );
            })
            .catch((error) => {
                if (error.response["status"] === 400){
                    alert(error.response.data["detail"]);
                }
            });
        };
    
    const validateForm = async (data) => {
        let userDict = {
             "email": data.email,
             "password": data.password
        }
        await loginUser(userDict);
    }

    return (
        <MainForm onSubmit={ handleSubmit(validateForm) }>
            <div className="wrapper login__wrapper">
                <section className="lodin-input__container">
                    <MainInput lblText={ "Логин" } maxLength={ 30 } type="text" required
                        register={ register("email", {
                            minLength: { value: 8, message: "Длинна поля должна быть от 8 символов" },
                            pattern: { value: /(^[a-zA-Z0-9_-]+@[mail|gmail|]+\.[ru|com]+)/, message: "Неверный формат почты" }
                        })} errorsMessage={errors?.email?.message} 
                    />

                    <PwdInput lblText={"Пароль"} maxLength={ 24 } type="password" required
                        register={ register("password", {
                            minLength: { value: 4, message: "Длинна поля должна быть 4 символов" },
                        })} errorsMessage={errors?.password?.message} 
                    />
                </section>
                
                <section className="login__link-container">
                    <Link className="login-link" to="/auth/reset-password">
                        Сбросить пароль
                    </Link> <br />
                    <Link className="login-link" to="/auth/register">
                        Создать учетную запись 
                    </Link>
                </section>
                <div className="login__btn-container">
                    <MainBtn>Войти</MainBtn>
                </div> 
                
            </div>
        </MainForm>
    );
}
