import axios from "axios";

const apiURL = import.meta.env.VITE_APP_API_URL;

const http = axios.create({
    baseURL: apiURL,
});

http.interceptors.request.use(
    (error) => {
        return Promise.reject(error);
    },
);


export default http;
