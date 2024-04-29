import { HeaderNav } from "./HeaderNav";
import { Link, Outlet } from "react-router-dom";
import "/src/style/components/header/header.sass";



export function Header() {
    return (
        <>
            <header className="header__container">
                <div className="wrapper wrapper__header">
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
