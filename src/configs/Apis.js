import axios from "axios"

export let endpoints = {
    "tours": "/tours/",
    "imageTours": (tourId) => `/tours/${tourId}/imageTour/`,
    "oauth2-info" : "/oauth2-info/",
    "login" :"/o/token/",
    "current-user": "/users/current-user/",
    "comments": (tourId) => `/tours/${tourId}/comments/`,
    "add-comment":(tourId) => `/tours/${tourId}/add-comment/`,
    "rating":(tourId) => `/tours/${tourId}/rating/`,
    "register" : "/users/",
    "booktour" : "/booktours/",
    "getbill" : "/users/get_bill_paid/",
    "thanhtoan" : (billId) => `/bills/${billId}/thanh_toan/`,
    "getrate" : (tourId) => `/tours/${tourId}/get_rate/`,
    
}

export default axios.create({
    baseURL: "http://127.0.0.1:8000/"
})