import {App} from './../App.jsx'
import {Register} from './../components/auth/Register.jsx';
import {Login} from './../components/auth/Login.jsx';
import {PageNotFound} from "./../components/PageNotFound.jsx";
import {createBrowserRouter} from "react-router-dom";


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
