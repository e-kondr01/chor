import BaseAPI from "../config/baseAPI";
import { ILoginData, ITokenApi, IRegisterData } from "./auth-schema";

export class AuthAPI extends BaseAPI {
    login = async (data: ILoginData) => {
        return this.API<ITokenApi>({
            method: 'POST',
            url: '/jwt/login',
            data: data,
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
        });
    };

    register = async (data: IRegisterData) => {
        return this.API<void>({
            method: 'POST',
            url: '/register',
            data: data,
            headers: {
                'Content-Type': 'application/json',
            },
        });
    };
}
