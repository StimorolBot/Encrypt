import "./style/auth_user.sass";

import { useState } from "react";
import { MainNav } from "../ui/nav/MainNav";


export function HeaderNav() {

    const [isShowNav, setIsShowNav] = useState(false);
    const headerNav = [
        {"url": "/auth/register", "name": "Регистрация"},
        {"url": "/auth/login", "name": "Вход"}
    ];

    return (
        <>
            <MainNav navItems={ headerNav } active={ isShowNav }/>
            <div className="header__auth-container" onClick={() => setIsShowNav((state) => !state)}>
                <img className="header__auth-btn"
                    src="/public/user-regular.svg" alt="auth-btn" />
            </div>
        </>    
    );
}
