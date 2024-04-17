import { App } from '/src/App.jsx'
import { createBrowserRouter } from "react-router-dom";
import { Login } from '/src/page/auth/Login';
import { Register } from '/src/page/auth/Register';
import { PageNotFound } from "/src/page/error/PageNotFound";


const router = createBrowserRouter([
    {
        path: "/",
        element: <App/>,
        errorElement: <PageNotFound/>
    },
    {
        path: "/register",
        element: <Register/>, 
    },
    {
        path: "/login",
        element: <Login/>, 
    },
    {
        path: "/logout",
        element: <h2>logout</h2>, 
    }
]);

export default router;
