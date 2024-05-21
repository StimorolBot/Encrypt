import "./context_menu.sass";

import { useRef, useState } from "react";
import { useClickOutside } from "../../hook/useClickOutside";


export function ContextMenu({ children }) {
    const [visible, setVisible] = useState(false);
    const menuRef = useRef();

    useClickOutside(menuRef, setVisible);
    
    return(
        <menu className="context-menu" ref={ menuRef }>
            <ul className="context-menu-btn" onClick={() => setVisible((state) => !state)}>
                <li className="context-menu-btn-point"></li>
                <li className="context-menu-btn-point"></li>
                <li className="context-menu-btn-point"></li>
            </ul>

            <ul className={`context-menu__container_${visible}`}>
                { children }
            </ul>   
        </menu>
    );
}
