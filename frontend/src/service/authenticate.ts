import { useStore } from "./stateStore";
import { UserName, Password } from "../entities/user";
import { logIn, logOut } from "../api/auth";

export function useAuthenticate() {
  // Usually, we access services through Dependency Injection.
  // Here we can use hooks as a crooked “DI-container”.

  // The use case function doesn't call third-party services directly,
  // instead, it relies on the interfaces we declared earlier.
  const storage = useStore();

  // Ideally, we would pass a command as an argument,
  // which would encapsulate all input data.
  async function authenticate(login: UserName, password: Password): Promise<void> {
    const user = await logIn(login, password)
    storage.setLoggedIn(user);
  }

  async function logout(): Promise<void> {
    await logOut()
    storage.setLoggedOut();
  }

  return {
    user: storage.user,
    authenticate,
    logout,
  };
}
