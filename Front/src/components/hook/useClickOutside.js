import { useEffect } from "react";

export const useClickOutside = (ref, func) =>{
    const handleClick = (e) => {
        console.log(ref)
        if (ref.currnet && !ref.target.contains(e.target)){
            func();
        }
    };

    useEffect(() => { 
        document.addEventListener("mousedown", handleClick);
        return () => {
            document.removeEventListener("mousedown", handleClick);
        };
    });
}