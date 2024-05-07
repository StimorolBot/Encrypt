import api from "/src/api/api";
import { useState } from "react";  
import cookies from "/src/api/cookies"
import { Link } from "react-router-dom";
import { MainBtn } from "/src/components/ui/btn/MainBtn";
import { MainForm } from "/src/components/ui/form/MainForm";
import { PwdInput } from "../../components/ui/input/PwdInput";
import { MainInput } from "/src/components/ui/input/MainInput";

import "/src/style/components/page/auth/login.sass";


export function Login() {
    const [userData, setUserData] = useState({"email": "", "password":""});
 
    const postlogin = async (event) => {
        event.preventDefault();
        
        await api.post("/auth/login", userData)
            .then((response) => {
                localStorage.setItem("access_token", response.data["access_token"]);
                cookies.set("refresh_token", response.data["refresh_token"],
                    { maxAge: response.data["refresh_max_age"] }
                );
            })
            .catch((error) => {
                if (error.response["status"] === 400){
                    alert(error.response.data["detail"]);
                }
            });
        };

    // использовать useEffect
    //if (isAuth == true)
      //  return <Navigate to={"/"}/>    

    return (
        <div className="wrapper login__wrapper">
            <MainForm onSubmit={postlogin}>
                <MainInput lblText={"Логин"} maxLength={24}
                    type="text" placeholder=" " required
                    onChange={(event) => setUserData({...userData, email: event.target.value})}
                />
                <PwdInput lblText={"Пароль"} maxLength={24}
                    type="password" placeholder=" " required
                    onChange={(event) => setUserData({...userData, password: event.target.value})}
                />
                <div className="login__reset-password-container">
                    <Link className="login__reset-password" to="/auth/reset-password">
                        Сбросить пароль
                    </Link>
                </div> 

                <MainBtn>Войти</MainBtn>
            </MainForm>
        </div>
    );
}
