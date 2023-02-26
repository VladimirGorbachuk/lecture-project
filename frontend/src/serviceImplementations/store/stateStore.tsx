import React, { useState } from "react";
import { useContext } from "react";
import {User, UserNonAuthenticated, Contact} from "../../entities/user";
import { useUserAuthStoreInterface, UserAuthState } from "../../serviceInterfaces/userStore";


interface Props {
  children: React.ReactNode;
}



const StoreContext = React.createContext<UserAuthState>(
  {user: {...UserNonAuthenticated }, setLoggedIn: (userInfo: User) => {}, setLoggedOut: ()=>{}}
);

export const useUserAuthStore: useUserAuthStoreInterface = (): UserAuthState => useContext(StoreContext); // to get the context in any component inside provider

export const Provider: React.FC<Props> = ({ children }) => {
  const [user, setUser] = useState({...UserNonAuthenticated});

  const value = {
    user,
    setLoggedIn: (userInfo: User) => setUser({...userInfo}), // better separate this out
    setLoggedOut: () => setUser({...UserNonAuthenticated}),
  };

  return (
    <StoreContext.Provider value={value}>{children}</StoreContext.Provider>
  );
};
