import { api } from "/src/api/api"
import { createUrlDownload } from "../../api/url";
import { ContextMenu } from "../ui/menu/ContextMenu";
import { TransitionGroup, CSSTransition } from "react-transition-group";

import "/src/style/components/sidebar/file_info.sass"


export function FileInfo({ fileData, setFileData }) {

    const deleteFile = async (event, index) =>  {
        event.preventDefault();
        const name = fileData["file_name"][index];
        // Удаление элемента из списка
        setFileData({...fileData, file_name: fileData["file_name"].filter( item => item != name )}); 
        await api.delete("/file/file-delete", {data: {"name": name}})
    }

    const downloadFile = async (event, index) => {
        event.preventDefault();
        const name = fileData["file_name"][index];
        
        await api.get(`/file/download/user@mail.ru/${name}`, { responseType: 'blob' })
        .then((response) => {
            createUrlDownload(response.data, name);
        })
        .catch((error) => {
            console.log(error);
        });
    }

    return (
        <ul className="sidebar__file-container">

            <div className="sidebar__username-container">
                <h3 className="sidebar-username">
                    {fileData["user_name"] !== undefined && fileData["user_name"]}
                </h3>
            </div>

            <div className="wrapper file__wrapper">
                { fileData === undefined ? <h4 className="file-none">У вас еще нет файлов</h4>
                : fileData["user_name"] !== undefined &&
                    <TransitionGroup className="file-list">
                        { fileData["file_name"].map((item, index) =>
                            <CSSTransition classNames="sidebar__file-transition" 
                                key={index}  timeout={ 500 }>
                                
                                <li className="sidebar__file-info">
                                    <img className="sidebar-file-ico" src="../../public/file-regular.svg" alt="file.ico"/>
                    
                                    <ContextMenu>
                                        <li className="context-menu-item" 
                                            onClick={(e) => downloadFile(e, index)}>
                                            Скачать
                                        </li> 
                                        
                                        <li className="context-menu-item"
                                            onClick={(e) => deleteFile(e, index)}>
                                            Удалить
                                        </li>
                                    </ContextMenu>
                                    <p className="sidebar-file">{ item }</p>
                                </li>
                                
                            </CSSTransition>
                        )}
                    </TransitionGroup>
                }
            </div>
        </ul>
    );
}
