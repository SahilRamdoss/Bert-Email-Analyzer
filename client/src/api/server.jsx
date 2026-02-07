import axios from "axios";

const serverAPI = axios.create({
    baseURL: "http://127.0.0.1:8000",
    timeout: 600000,
})

export default serverAPI;