import { AuthAPI } from './auth/auth';
import http from './config/http';

export const authAPI = new AuthAPI(http);
