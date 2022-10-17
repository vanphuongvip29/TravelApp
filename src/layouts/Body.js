import { BrowserRouter, Route, Routes } from "react-router-dom";
import Home from "../pages/Home";
import Login from "../pages/Login";
import Register from "../pages/register";
import TourDetail from "../pages/TourDetail";
import UserDetail from "../pages/UserDetail";
import Footer from "./Footer";
import Header from "./Header";

export default function Body(){
    return(
        <>
            
            <BrowserRouter>
                <Header />
                <Routes>
                    
                    <Route path="/" element={<Home />}/>
                    <Route path="/tours/:tourId/imageTour" element={<TourDetail />}/>
                    <Route path="/login" element={<Login />}/>
                    <Route path="/register" element={<Register />}/>
                    <Route path="/user" element={<UserDetail />}/>

                    
                </Routes>
                <Footer/>               
            </BrowserRouter>
            
        </>
       
    )
}