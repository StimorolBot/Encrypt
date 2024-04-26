import { useState } from "react";
import { AuthContex } from "./context/main";
import { Encrypt } from "/src/page/Encrypt";
import { Login } from '/src/page/auth/Login';
import { Route, Routes, Navigate } from "react-router-dom";
import { Register } from '/src/page/auth/Register';
import { Header } from "/src/components/header/Header";
import { PageNotFound } from "/src/page/error/PageNotFound";


export function App() {
    const [isAuth, setIsAuth] = useState(true);

    return (
        <AuthContex.Provider value={{isAuth, setIsAuth}}>
            <Routes>
                <Route path="/" element={<Header/>}>
                    <Route index element={<Encrypt/>} />
                    <Route path="auth/logout" element={<h1>выход</h1>} />
                    <Route path="auth/login" element={<Login/>} />
                    <Route path="auth/register" element={<Register/>} />
                    <Route path="*" element={<PageNotFound/>} />
                </Route>
            </Routes>
        </AuthContex.Provider>
    );
}