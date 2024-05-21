import "./style/sidebar.sass";

import { FileInfo } from "./../sidebar/FileInfo";


export function Sidebar({ fileData, setFileData}) {
    return (
        <aside className="sidebar">  
            <input className="burger-checkbox" type="checkbox" id="burger-checkbox"/>
            <label className="burger" htmlFor="burger-checkbox"></label>
            <div className="sidebar__container">
                <FileInfo fileData={ fileData } setFileData={ setFileData }/>
            </div>
        </aside>
    );
}
