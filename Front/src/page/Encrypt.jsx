import api from "/src/api/api";
import {  Navigate } from "react-router-dom";
import { AuthContex } from "../context/main";
import { useContext, useState } from "react";
import { MainBtn } from "/src/components/ui/btn/MainBtn";
import { Sidebar } from "/src/components/sidebar/Sidebar";
import { MainForm } from "/src/components/ui/form/MainForm";
import { BtnInput } from "/src/components/ui/input/BtnInput";
import { MainInput } from "/src/components/ui/input/MainInput";
import { DownloadBtn } from "/src/components/ui/btn/DownloadBtn";

import "/src/style/components/page/encrypt.sass";


export function Encrypt() {
    const {isAuth, setIsAuth} = useContext(AuthContex);
    const [userData, setUserDate] = useState(
        {"file": "", "password": ""}
    );
    const [urlFile, setUrlFile] = useState(null);

    const uploadFile = async (event) => {
        
        event.preventDefault();
        const formData = new FormData();
        formData.append('file', userData.file);
        formData.append('password', userData.password);

        await api.post("/file", formData, { responseType: 'blob' }) // получить имя из заголовка 
        .then((response) => { 
            console.log(response.data)
            setUrlFile(URL.createObjectURL(response.data));
        })
        .cath((error) => {
            alert("ошибка")
           console.log(error);   
        });
    };

    if (isAuth === false)
        return <Navigate to={"/auth/login"}/>

    return(
        <div className="wrapper encrypt__wrapper">
            <MainForm onSubmit={uploadFile}>
                <BtnInput file_name={userData.file.name}
                    btn_name={"Загрузить"}
                    type="file" id="file" required
                    onChange={(event) => setUserDate(
                        {...userData, file: event.target.files[0]}
                    )}
                />
                    
                <MainInput lblText={"Пароль"} 
                    type="password" maxLength={32}
                    required placeholder=" "
                    onChange={(event) => setUserDate(
                        {...userData, password: event.target.value}
                    )}
                />
                <section className="encrypt__btn-container">
                    <MainBtn> Зашифровать </MainBtn>
                    <DownloadBtn btnText={"Скачать"}  
                        href={urlFile} /> {/*download="test.txt"*/}
                </section>    
            </MainForm>            
            <Sidebar/>
        </div>
    );
}
