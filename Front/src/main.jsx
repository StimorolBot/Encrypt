import React from 'react'
import ReactDOM from 'react-dom/client'
import {createBrowserRouter, RouterProvider } from "react-router-dom";

import {App} from './App.jsx'


const router = createBrowserRouter([
    {
        path: "/",
        element: <App/>, 
    },
    {
        path: "/test",
        element: <h2>TEST</h2>, 
    },
]);


ReactDOM.createRoot(document.getElementById('root')).render(
    <RouterProvider router={router}/>

)
