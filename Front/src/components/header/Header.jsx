import "./style/header.sass";

import { HeaderNav } from "./HeaderNav";
import { Link, Outlet } from "react-router-dom";


export function Header() {
    return (<>
        <header className="header">
            <div className="wrapper">
                <h1 className="header__title">
                    <Link className="header-title-link" to="/">Encrypt</Link>
                </h1>
                <HeaderNav/>
            </div>
        </header>
        <Outlet />
        </>
    );
}
