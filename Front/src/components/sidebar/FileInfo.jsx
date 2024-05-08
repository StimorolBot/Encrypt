import { api } from "/src/api/api"
import { useEffect, useState } from "react";
import { useFetch } from "../hook/useFetch";
import { getFileInfo } from "../../api/http";
import { createUrlDownload } from "../../api/url";
import { ContextMenu } from "../ui/menu/ContextMenu";
import { TransitionGroup, CSSTransition } from "react-transition-group";

import "/src/style/components/sidebar/file_info.sass"


export function FileInfo() {
    const [data, setData] = useState({
        "user_name": "", "email": "", "file_name": [] 
    });
    
    const [fetchFile, isLoad, errorResponse] = useFetch(async () => {
            const response = await getFileInfo();
            setData({...data,
                user_name: response["user_name"],
                email: response["email"],
                file_name: response["path"]["file_name"].map(file => file["name"])
            });    
        }
    );
  
    const deleteFile = async (event, index) =>  {
        event.preventDefault();
        const name = data["file_name"][index];
        // Удаление элемента из списка
        setData({...data, file_name: data["file_name"].filter( item => item != name )}); 
        await api.delete("/file/file-delete", {data: {"name": name}})
    }

    const downloadFile = async (event, index) => {
        event.preventDefault();
        const name = data["file_name"][index];
        
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
        {/* <div className="sidebar__username-container" onClick={() => t()}>
            <h3 className="sidebar-username">{'data[0]["user_name"]'}</h3>
        </div> */}
        
        <ul className="sidebar__file-container" >
            <div className="wrapper file__wrapper">
                { data === undefined ? <h4 className="file-none">У вас еще нет файлов</h4>
                : data["user_name"] !== undefined &&
                    <TransitionGroup className="todo-list">
                        { data["file_name"].map((item, index) =>
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
                                    <p className="sidebar-file">{ item }</p>
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
