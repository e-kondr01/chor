import { AxiosInstance } from 'axios';

class BaseAPI {
    protected API: AxiosInstance;
    constructor(instance: AxiosInstance) {
        this.API = instance;
    }
}

export default BaseAPI;
