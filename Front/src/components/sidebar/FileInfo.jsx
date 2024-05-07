import { api } from "/src/api/api"
import { useEffect, useState } from "react";
import { useFetch } from "../hook/useFetch";
import { getFileInfo } from "../../api/http";
import { createUrlDownload } from "../../api/url";
import { ContextMenu } from "../ui/menu/ContextMenu";
import { TransitionGroup, CSSTransition } from "react-transition-group";

import "/src/style/components/sidebar/file_info.sass"


export function FileInfo() {
    const [fileData, setFileData] = useState([]);
    
    const [fetchFile, isLoad, errorResponse] = useFetch(async () => {
            const response = await getFileInfo();
            setFileData(response);
        }
    );

    const deleteFile = async (event, index) =>  {
        event.preventDefault();
        let name = fileData[0]["path"]["file_name"][index].name;
        
        // Удаление элементов из списка
        setFileData(fileData.filter(file => file.name !== name));
        
        await api.delete("/file/file-delete", {data: {"name": name}})
        .then((response) => {
            console.log(response.data);    
        })
        .catch((err) => {
            console.log(err);   
        });
    }

    const downloadFile = async (event, index) => {
        event.preventDefault();
        let name = fileData[0]["path"]["file_name"][index].name;
        
        await api.get(`/file/download/user@mail.ru/${name}`, { responseType: 'blob' })
        .then((response) => {
            createUrlDownload(response.data, name);
        })
        .catch((error) => {
            console.log(error);
        });
    }

    useEffect(() => {
        fetchFile();
    }, []);


    return (
        <> 
        <div className="sidebar__username-container" onClick={() => t()}>
            <h3 className="sidebar-username">{'fileData[0]["user_name"]'}</h3>
        </div>
        
        <ul className="sidebar__file-container" >
            <div className="wrapper file__wrapper">
                { fileData === undefined ? <h4 className="file-none">У вас еще нет файлов</h4>
                : fileData["user_name"] !== undefined &&
                    <TransitionGroup className="todo-list">
                        { fileData["path"]["file_name"].map((item, index) =>
                            <CSSTransition classNames="sidebar__file-ransition" 
                                key={index}  timeout={ 100 }>
                                
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
                                    <p className="sidebar-file">{ item.name }</p>
                                </li>
                                
                            </CSSTransition>
                        )}
                    </TransitionGroup>
                }
            </div>
        </ul>
        </>
    );
}
