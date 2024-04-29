import { api } from "/src/api/api"
import { useEffect, useState } from "react";
import { useFetch } from "../hook/useFetch";
import { getFileInfo } from "../../api/http";
import { CreateList } from "../list/CreateList";
import { ContextMenu } from "../ui/menu/ContextMenu";

import "/src/style/components/sidebar/file_info.sass"


export function FileInfo() {
    const [fileData, setFileData] = useState([]);

    const [fetchFile, fileLoad, error] = useFetch(async () => {
        const response = await getFileInfo();
        setFileData(response);
    });

    const delFile = async (index, event) =>  {
        event.preventDefault();
        
        setFileData(fileData.filter(file => file.name !== fileData[index].name)); // Удаление элементов из списка
        console.log(fileData.length); 

        await api.delete("/file/file-delete", {data:{"file_name": fileData[index].name}})
        .then((response) => {
            console.log(response.data);    
        })
        .catch((err) => {
            console.log(err);   
        });
    }

    const downloadFile = async (index, event) => {
        event.preventDefault();
        
        await api.get(`/file/download/user@mail.ru/${fileData[index].name}`, { responseType: 'blob' })
        .then((response) => {
            /* Вынести в отдельную функцию */
            let url = URL.createObjectURL(response.data);
            let anchor = document.createElement("a");
            
            anchor.href = url;
            anchor.download = fileData[index].name;
            document.body.append(anchor);
            anchor.style = "display: none";
            anchor.click();
            anchor.remove();
        })
        .catch((error) => {
            console.log(error);
        });
    }

    useEffect(() => {
        fetchFile();
    }, []);

    return (
        <ul className="sidebar__file-container">
            <div className="sidebar__username-container">
                <h3 className="sidebar-username">UserName</h3>
            </div>
            
            <div className="wrapper file__wrapper">
                {fileData.length !== 0
                    ?<CreateList list={fileData}>
                        <img className="sidebar-file-ico" src="../../public/file-regular.svg" alt="file.ico"/>
                        <ContextMenu downloadFile={downloadFile} delFile={delFile}/>
                    </CreateList>
                    :<h4 className="file-none">У вас еще нет файлов</h4>
                }
            </div>
        </ul>
    );
}
