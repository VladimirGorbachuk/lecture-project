import React, { useState } from "react";

import {UserAuth, User}  from "../../entities/user"
import { useAuthenticate } from "../../service/authenticate";

import styles from "./Auth.module.css";


export interface AuthenticationService {
    auth(authInfo: UserAuth): Promise<User>;
  }


export function Auth() {
  const [loading, setLoading] = useState(false);

  const { user, authenticate, logout } = useAuthenticate();

  async function handleSubmit(e: React.FormEvent) {
    setLoading(true);
    e.preventDefault();
    const target = e.target as typeof e.target & {
      login: { value: string };
      password: { value: string };
    };
    const login = target.login.value;
    const password = target.password.value;
    await authenticate(login, password);
    setLoading(false);
  }

  return (
    <form className={styles.form} onSubmit={handleSubmit}>
      <label>
        <span>Login</span>
        <input
          type="text"
          name="login"
          autoFocus
        />
      </label>
      <label>
        <span>Password</span>
        <input
          type="text"
          name="password"
        />
      </label>

      <button type="submit" disabled={loading}>
        {loading ? "Trying to login..." : "Login"}
      </button>
    </form>
  );
}
