export interface ILoginData {
    username: string;
    password: string;
}

export interface ITokenApi {
    access_token: string
    refresh_token: string;
    token_type: string
}

export interface IRegisterData {
    email: string,
    password: string,
    re_password: string
}