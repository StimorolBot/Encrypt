import "/src/style/components/ui/form/main_form.sass";

export function MainForm({children, ...props}) {
    return(
        <form {...props} className="main__form">
            {children}
        </form>
    );
}