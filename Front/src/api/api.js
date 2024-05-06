import axios from "axios";

export const api = axios.create({baseURL:"http://127.0.0.1:8000", 
    withCredentials: true, 
    sameSite: "none",
});

api.interceptors.request.use((config) => {
    const token = localStorage.getItem("access_token");
    
    if (!token){
        config.headers.Authorization = null;
    }else{
        config.headers.Authorization = `Bearer ${token}`;
    }

    return config;
});

api.interceptors.response.use((response) => {
    return response;
    }, (error) => {
        return error.response;
    }
);

export default api;