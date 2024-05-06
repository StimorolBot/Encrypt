import { MainBtn } from "./MainBtn";


export function DownloadBtn({btnText, ...props}){
    return(
        <a className="download-btn" {...props}>
            <MainBtn type="button">
                {btnText}
            </MainBtn>
        </a>
    );
}