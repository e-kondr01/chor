import axios from "axios";

const apiURL = import.meta.env.VITE_APP_API_URL;

const http = axios.create({
    baseURL: apiURL,
});

http.interceptors.response.use(function (response) {
    return response;
  }, function (error) {
    return Promise.reject(error);
  });


export default http;
