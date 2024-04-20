import { App } from '/src/App.jsx'
import { Login } from '/src/page/auth/Login';
import { Register } from '/src/page/auth/Register';
import { createBrowserRouter } from "react-router-dom";
import { Header } from "/src/components/header/Header";
import { PageNotFound } from "/src/page/error/PageNotFound";


const router = createBrowserRouter([
    {
        path: "/",
        element: [<Header/>, <App/>],
        errorElement: <PageNotFound/>,
    },
    {
        path: "/auth/",
        element: <Header/>,
        children:[
            {
                path: "register",
                element: <Register/>
            },
            {
                path: "login",
                element: <Login/>, 
            },
            {
                path: "logout",
                element: <h2>logout</h2>, 
            }
        ]
    }
]);
 
export default router;
