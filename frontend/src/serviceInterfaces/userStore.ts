import {User, UserNonAuthenticated, Contact} from "../entities/user";

export interface UserAuthState {
    user: User;
    setLoggedIn(userInfo: User): void;
    setLoggedOut(): void;
  }
  

export type useUserAuthStoreInterface = () => UserAuthState;
