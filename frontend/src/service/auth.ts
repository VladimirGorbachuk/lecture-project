import {UserAuth, User, UserNonAuthenticated}  from "../entities/user"


export interface AuthenticationService {
    auth(authInfo: UserAuth): Promise<User>;
  }

export const authenticateUser = (userAuth: UserAuth): User => {
    return {
      isAuthenticated: true,
      id: "123",
      login: userAuth.login,
      email: userAuth.email,
      cv: undefined,
      contacts: undefined,
    }
}