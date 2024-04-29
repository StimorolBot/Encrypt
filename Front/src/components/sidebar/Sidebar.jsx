import {FileInfo} from "/src/components/sidebar/FileInfo";

import "/src/style/components/sidebar/sidebar.sass";


export function Sidebar() {
    return (
        <>  
            <input className="burger-checkbox" type="checkbox" id="burger-checkbox"/>
            <label className="burger" htmlFor="burger-checkbox"></label>
            <div className="sidebar">
                <div className="wrapper sidebar__wrapper">
                    <FileInfo/>
                </div>
            </div>
        </>
    );
}
