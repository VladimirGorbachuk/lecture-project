import React, { useState } from "react";
import { useContext } from "react";
import {User, UserNonAuthenticated, Contact} from "../entities/user";


interface Props {
  children: React.ReactNode;
}

interface CurrentState {
  user: User;
  setLoggedIn(userInfo: User): void;
  setLoggedOut(): void;
}


const StoreContext = React.createContext<CurrentState>(
  {user: {...UserNonAuthenticated }, setLoggedIn: (userInfo: User) => {}, setLoggedOut: ()=>{}}
);

export const useStore = (): CurrentState => useContext(StoreContext); // to get the context in any component inside provider

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
