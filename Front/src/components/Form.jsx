import "/src/style/form.sass"
import {useState} from "react";
import api from "../api.js";
import {Sidebar} from "./components/Sidebar.jsx";

export function Form() {
    const [file, setFile] = useState(null);
    const [password, setPassword] = useState("");

    const sendFile = async (event) => {
        event.preventDefault();
        
        const formData = new FormData();
        formData.append('upload_file', file);
        formData.append('password', password);

        await api.post("/file", formData).then((response) => {
                console.log(response.data);
            })
            .catch((error) =>{
                console.log(error);
            });
    };

    return (
    
        <form className="encrypt__form" method="POST" encType="multipart/form-data" onSubmit={sendFile}>
            <div className="file-input-container">
                <label className="file-input-text" htmlFor="file">Загрузить файл</label>
                <span className="file-input-name"></span>
                <input className="file-input" type="file" name="file" id="file" required
                       onChange={(event) => setFile(event.target.files[0])}/>
            </div>
            <input className="encrypt__form-input" type="password" name="password" required
            onChange={(event) => setPassword(event.target.value)}/>
            <button className="encrypt__form-btn" type="submit">Зашифровать</button>
        </form>

    )
}