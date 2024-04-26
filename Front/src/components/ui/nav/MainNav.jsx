import { Link } from "react-router-dom";
import "/src/style/components/ui/nav/main_nav.sass";


export function MainNav({navItems, active}) {
    let classNav = ["header__auth-items"];

    if (active)
        classNav.push("header__auth-items_active");
    else
        classNav = ["header__auth-items"];
        
    return(
        <nav className={classNav.join(" ")}>
            {navItems.map((item) => 
                <Link className="header__auth-item" to={item.url} key={item.url}>
                    {item.name}
                </Link>
            )}
        </nav>
    );
}