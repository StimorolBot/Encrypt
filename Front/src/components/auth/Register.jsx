import api from "/src/config/api";
import {useState} from "react";

import "/src/style/elements/btn.sass";
import "/src/style/elements/form.sass";
import "/src/style/components/auth/register.sass";

import {Header} from "/src/components/header/Header.jsx";
import {Input} from "./../elements/input";


export function Register() {
    const [username, setUsername] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");

    const register = async (event) => {
        event.preventDefault();
        
        await api.post("/register", {"user_name": username, "email":email, "password": password}).then((response) => {
                console.log(response.data);
            })
            .catch((error) =>{
                console.log(error);
            });
    }

    return (
        <>
            <Header/>
            <div className="wrapper wrapper__body">
                <form className="main__form register__form" method="POST" onSubmit={register}>
                    <div className="register__inpit-container">
                        <Input lblText={"Имя"} maxLen={16} setVal={setUsername} type={"text"}/>
                        <Input lblText={"Логин"} maxLen={24} setVal={setEmail} type={"email"}/>
                        <Input lblText={"Код подтверждения"} maxLen={24} setVal={setEmail} type={"email"}/>
                        <Input lblText={"Пароль"} maxLen={24} setVal={setPassword} type={"password"}/>
                        <Input lblText={"Подтвердите пароль"} maxLen={24} setVal={setPassword} type={"password"}/> 
                    </div>
                    <div className="register__form-help">
                        
                    </div>   
                    <button className="main-btn" type="submit">Зарегистрироваться</button>
                </form>
            </div>
        </>
    )
}