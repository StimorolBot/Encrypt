import "./main_nav.sass";
import { Link } from "react-router-dom";


export function MainNav({ navItems, active }) {
    return(
        <nav className={ active ? 
            "header__auth-items header__auth-items_active" 
            : "header__auth-items"}
        >
            { navItems.map((item) => 
                <Link className="header__auth-item" to={item.url} key={item.url}>
                    {item.name}
                </Link>
            )}
        </nav>
    );
}