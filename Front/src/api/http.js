import api from "/src/api/api";


export async function getFileInfo(){
    const response = await api.get("/");
    return response.data;
}
