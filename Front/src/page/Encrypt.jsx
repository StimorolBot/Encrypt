import api from "/src/api/api";
import { getFileInfo } from "../api/http";
import { useState, useEffect } from "react";
import { useFetch } from "../components/hook/useFetch";
import { MainBtn } from "/src/components/ui/btn/MainBtn";
import { Sidebar } from "/src/components/sidebar/Sidebar";
import { PwdInput } from "../components/ui/input/PwdInput";
import { MainForm } from "/src/components/ui/form/MainForm";
import { BtnInput } from "/src/components/ui/input/BtnInput";
import { DownloadBtn } from "/src/components/ui/btn/DownloadBtn";

import "/src/style/components/page/encrypt.sass";

export function Encrypt() {
    let encryptBtnClass = ["encrypt-btn"]
    const [fileName, setFileName] = useState(""); 
    const [urlFile, setUrlFile] = useState(null);
    
    const [fileData, setFileData] = useState({
        "user_name": "", "email": "", "file_name": [] 
    });
    const [userData, setUserDate] = useState({
        "file": "", "password": ""
    });

    const [fetchFile, isLoad, errorResponse] = useFetch(async () => {
            const response = await getFileInfo();
            setFileData({...fileData,
                user_name: response["user_name"],
                email: response["email"],
                file_name: response["path"]["file_name"].map(file => file["name"])
            });    
        }
    );

    const uploadFile = async (event) => {
        event.preventDefault();

        const formData = new FormData();
        formData.append('file', userData.file);
        formData.append('password', userData.password);

        await api.post("/file", formData, { responseType: 'blob'}).then((response) => { 
            setFileName(response.headers["content-disposition"]);
            setUrlFile(URL.createObjectURL(response.data));
            
            setFileData({...fileData,
                user_name: fileData["user_name"],
                email: fileData["email"],
                file_name: [...fileData["file_name"], response.headers["content-disposition"]]
            });
        })
    };

    if ( urlFile )
        encryptBtnClass.push("encrypt-btn_active");
    
    useEffect(() => {
        fetchFile();
    }, []);
    
    return(
        <div className="wrapper encrypt__wrapper">
            <MainForm onSubmit={ uploadFile }>
                <BtnInput file_name={ userData.file.name }
                    btn_name={ "Загрузить" }
                    type="file" id="file" required
                    onChange={(event) => setUserDate(
                        {...userData, file: event.target.files[0]}
                    )}
                />
                    
                <PwdInput lblText={ "Пароль" } 
                    type="password" maxLength={ 32 }
                    required onChange={(event) => setUserDate(
                        {...userData, password: event.target.value}
                    )}
                />
                <section className="encrypt__btn-container">                    
                    <div className={ encryptBtnClass.join(" ") }>
                        <MainBtn> Зашифровать </MainBtn>
                    </div>
                      
                    <DownloadBtn btnText={ "Скачать" }  
                        href={ urlFile } download={ fileName }/> 
                </section>    
            </MainForm>            
            <Sidebar fileData={ fileData } setFileData={ setFileData }/>
        </div>
    );
}
