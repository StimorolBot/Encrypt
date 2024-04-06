import "/src/style/file_info.sass"
import api from "../api.js";


export function FileInfo() {
    return (
        <ul className="sidebar__file-container">
            <li className="sidebar__file-info">
                <img className="sidebar-file-ico" src="../../public/file.png" alt="file.ico"/>
                <div className="sidebar__file-name"></div>
                <div className="sidebar__file-date-create">02.04.2024</div>
                <button className="sidebar__file-delete">X</button>
            </li>
        </ul>
    )
}