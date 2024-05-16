import axios from "axios";

const apiURL = import.meta.env.VITE_APP_API_URL;

const http = axios.create({
    baseURL: apiURL,
});

export default http;
