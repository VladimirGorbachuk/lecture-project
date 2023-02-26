import { User, UserName, Password } from "../entities/user";
import {useUserAuthStoreInterface} from "../serviceInterfaces/userStore"
import {AuthenticationServiceInterface} from "../serviceInterfaces/auth"


export interface UserAuthenticator {
  user: User;
  authenticate(login: UserName, password: Password): Promise<void>;
  logout(): Promise<void>;
}

export type useAuthenticateCallableType = (
  useAuthStore: useUserAuthStoreInterface,
  authService: AuthenticationServiceInterface,
) => UserAuthenticator;

export type useAuthenticateInjectedCallableType = (
) => UserAuthenticator;

export const useAuthenticate: useAuthenticateCallableType = (
  useAuthStore: useUserAuthStoreInterface,
  authService: AuthenticationServiceInterface,
): UserAuthenticator => {

  const storage = useAuthStore();

  async function authenticate(login: UserName, password: Password): Promise<void> {
    const user = await authService.logIn(login, password)
    storage.setLoggedIn(user);
  }

  async function logout(): Promise<void> {
    await authService.logOut()
    storage.setLoggedOut();
  }

  return {
    user: storage.user,
    authenticate,
    logout,
  };
}
