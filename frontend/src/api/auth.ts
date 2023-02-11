import { User, UserName, Password } from "../entities/user"



export type LogOutResponse = {
  result: string;
}


export const logIn = async (login: UserName, password: Password ): Promise<User> => {
  return new Promise((res) => setTimeout(() => res({
    isAuthenticated: true,
    id: "123",
    login: "abc",
    email: "some@email.ru",
    cv: "123",
    contacts: [],
  }), 450));
}


export const logOut = async (): Promise<LogOutResponse> => {
  return new Promise((res) => setTimeout(() => res({
    result: "logged out successfully"})
  , 450));
}