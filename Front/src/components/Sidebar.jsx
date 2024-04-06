import "/src/style/sidebar.sass"
import {FileInfo} from "./FileInfo.jsx"

export function Sidebar() {
    return (
        <section className="sidebar">
            <div className="wrapper wrapper__sidebar">
                <button className="close-sidebar"><i className="fa-regular fa-file"></i></button>
                <FileInfo/>
            </div>
        </section>
    )
}


