import { User, UserName, Password } from "../entities/user"


export type LogOutResponse = {
  result: string;
}

type logInCallableInterface = (login: UserName, password: Password) => Promise<User>;

type logOutCallableInterface = () => Promise<LogOutResponse>;

export type AuthenticationServiceInterface = {
  logIn: logInCallableInterface,
  logOut: logOutCallableInterface,
}
