export interface UserSignInRequest {
    first_name: string;
    last_name: string;
    email_address: string;
    password: string;
}

export interface UserLogInRequest {
    username: string;
    password: string;
}

export interface ChangePasswordRequest {
    email_address: string;
    new_password: string;
}

export interface AuthenticationResponse {
    access_token: string | null;
    token_type: string;
}