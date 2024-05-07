import api from "/src/api/api";
import { redirect } from "react-router-dom";


export const getFileInfo = async () => {
    const response = await api.get("/");

    switch (response.status){
        case 400: {
            api.post("/auth/refresh").then((r) => {
                localStorage.setItem("access_token", r.data["access_token"]);
            });
            break;
        } 
        case 401:
            return redirect("/auth/login");
            
        case 200:
            return response.data[0];

        default:
            console.log(`Неизвестный статус: ${response.status}`);
        }
}
