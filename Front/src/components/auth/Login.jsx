import "/src/style/elements/form.sass";
import "/src/style/elements/btn.sass";
import "/src/style/components/auth/login.sass";

import { useState } from "react";
import api from "/src/config/api.js";
import { Input } from "../elements/input";
import { redirect } from "react-router-dom";
import { Header } from "/src/components/header/Header.jsx";


export function Login() {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");

    const login = async (event) => {
        event.preventDefault();
        
        const formData = new FormData();
        formData.append('email', email);
        formData.append('password', password);

        await api.post("/login", {"email": email, "password": password}, {withCredentials: true})
            .then(() => {
                return redirect("/");
            })
            .catch((error) =>{
                console.log(error);
                return redirect("/");
        });
            return redirect("/");
    };

    return (
        <>
            <Header/>
            <div className="wrapper wrapper__body">
                <form className="main__form login__form" method="POST" onSubmit={login}>
                    <Input lblText={"Логин"} maxLen={24} type={"text"} setVal={setEmail}/>
                    <Input lblText={"Пароль"} maxLen={24} type={"password"} setVal={setPassword}/> 
                    <button className="main-btn" type="submit">Войти</button>
                </form>
            </div>
        </>
    )
}