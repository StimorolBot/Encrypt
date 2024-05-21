import "./main_form.sass";

export function MainForm({ children, ...props }) {
    return(
        <form className="main__form" {...props} >
            { children }
        </form>
    );
}