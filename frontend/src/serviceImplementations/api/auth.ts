import { User, UserName, Password } from "../../entities/user"
import {LOGIN_ENDPOINT} from "./api"
import { AuthenticationServiceInterface } from "../../serviceInterfaces/auth";


export type LogOutResponse = {
  result: string;
}


export const logIn = async (login: UserName, password: Password ): Promise<User> => {
  const data = {login: login, password: password};
  let response = await fetch(
    LOGIN_ENDPOINT,
    {
      method: "POST",
      body: JSON.stringify(data),
      headers: {
        "Content-Type": "application/json"
      },
      credentials: 'include',
    },
  )
  return response.json();
}

export const logOut = async (): Promise<LogOutResponse> => {
  return new Promise((res) => setTimeout(() => res({
    result: "logged out successfully"})
  , 450));
}

export const AuthenticationService: AuthenticationServiceInterface = {
  logIn,
  logOut
}