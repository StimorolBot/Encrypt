import { useState } from "react";
import { MainNav } from "../ui/nav/MainNav";

import "/src/style/components/header/auth_user.sass";


export function HeaderNav() {

    const [isShowNav, setIsShowNav] = useState(false);
    const headerNav = [
        {"url": "/auth/register", "name": "Регистрация"},
        {"url": "/auth/login", "name": "Вход"}
    ];

    return (
        <div className="header__auth-container">
            <MainNav navItems={headerNav} active={isShowNav}/>
            <div className="" onClick={() => {
                if (isShowNav)
                    setIsShowNav(false);
                else
                    setIsShowNav(true);
                }}>
                <img className="header__auth-btn" 
                    src="/public/user-regular.svg" alt="auth-btn" />
            </div>
        </div>    
    );
}

