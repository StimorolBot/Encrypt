import "./main_btn.sass";


export function MainBtn({children, ...props}){
    return(
        <button {...props} className="main-btn">
            {children}
        </button>
    );
}
