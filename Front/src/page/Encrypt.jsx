import "./encrypt.sass";

import api from "./../api/api";
import { getFileInfo } from "../api/http";
import { useForm } from "react-hook-form";
import { useState, useEffect } from "react";
import { useFetch } from "../components/hook/useFetch";
import { MainBtn } from "./../components/ui/btn/MainBtn";
import { Sidebar } from "./../components/sidebar/Sidebar";
import { PwdInput } from "../components/ui/input/PwdInput";
import { MainForm } from "./../components/ui/form/MainForm";
import { BtnInput } from "./../components/ui/input/BtnInput";
import { DownloadBtn } from "./../components/ui/btn/DownloadBtn";


export function Encrypt() {
    let encryptBtnClass = ["encrypt-btn"]
    const [fileName, setFileName] = useState(""); 
    const [urlFile, setUrlFile] = useState(null);
    const { register, handleSubmit, reset, formState: { errors, isValid }} = useForm({mode: "onBlur"});
    
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
        <main className="encrypt">
            <MainForm onSubmit={ uploadFile }>
                <div className="wrapper">
                    <div className="encrypt__input-container">
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
                    </div>
                    <div className="encrypt__btn-container">
                        <div className={ encryptBtnClass.join(" ") }>
                            <MainBtn> Зашифровать </MainBtn>
                            <DownloadBtn btnText={ "Скачать" }  
                                href={ urlFile } download={ fileName }/>
                        </div>
                    </div> 
                </div>
            </MainForm>
            <Sidebar fileData={ fileData } setFileData={ setFileData }/>
        </main>
    );
}
