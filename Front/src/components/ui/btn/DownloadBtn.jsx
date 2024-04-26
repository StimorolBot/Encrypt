import { MainBtn } from "./MainBtn";

import "/src/style/components/ui/btn/download_btn.sass";

export function DownloadBtn({btnText,...props}){
    return(
        <a className="download-btn" {...props}>
            <MainBtn type="button">
                {btnText}
            </MainBtn>
        </a>
    );
}