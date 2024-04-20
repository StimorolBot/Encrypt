import { useState } from "react";   
import api from "/src/api/api";
import { redirect, Navigate } from "react-router-dom";
import { MainBtn } from "/src/components/ui/btn/MainBtn";
import { MainForm } from "/src/components/ui/form/MainForm";
import { MainInput } from "/src/components/ui/input/MainInput";

import "/src/style/components/page/auth/login.sass";


export function Login() {
    const [userData, setUserData] = useState({"email": "", "password":""});
 
    const postlogin = async (event) => {
        event.preventDefault();
        
        await api.post("/auth/login", userData)
            .then((response) => {
                localStorage.setItem("access_token", response.data["access_token"]);
            })
            .catch((error) =>{
                console.log(error);
            });
        };

    return (
        <div className="wrapper wrapper__body">
            <MainForm onSubmit={postlogin}>
                <MainInput lblText={"Логин"} maxLength={24}
                    type="text" placeholder=" " required
                    onChange={(event) => setUserData({...userData, email: event.target.value})}
                />
                <MainInput lblText={"Пароль"} maxLength={24}
                    type="password" placeholder=" " required
                    onChange={(event) => setUserData({...userData, password: event.target.value})}
                /> 
                <MainBtn>Войти</MainBtn>
            </MainForm>
        </div>
    );
}
