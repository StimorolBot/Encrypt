import { useState } from "react";
import { AuthContex } from "/src/context/main";
import { Encrypt } from "/src/page/Encrypt";
import { Login } from '/src/page/auth/Login';
import { Route, Routes } from "react-router-dom";
import { Register } from '/src/page/auth/Register';
import { Header } from "/src/components/header/Header";
import { PageNotFound } from "/src/page/error/PageNotFound";


export function MyRouter() {
    const [isAuth, setIsAuth] = useState(""); // исправить ! folse после перезагрузки 

    return (
        <AuthContex.Provider value={{isAuth, setIsAuth}}>
            <Routes>
                <Route path="/" element={<Header/>}>
                    <Route index element={<Encrypt/>} />
                    <Route path="auth/logout" element={<h1>выход</h1>} />
                    <Route path="auth/login" element={<Login/>} />
                    <Route path="auth/register" element={<Register/>} />
                    <Route path="auth/reset-password" element={<h1>Сброс Пароля</h1>} />
                    <Route path="*" element={<PageNotFound/>} />
                </Route>
            </Routes>
        </AuthContex.Provider>
    );
}
