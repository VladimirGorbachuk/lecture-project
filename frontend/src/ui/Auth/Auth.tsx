import React, { useState } from "react";
import styles from "./Auth.module.css";
import {PropsWithUseAuthenticate} from '../../di/propTypes'


export function Auth(props: PropsWithUseAuthenticate ) {
  const [loading, setLoading] = useState(false);

  const { user, authenticate, logout } = props.useAuthenticate();

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
          type="password"
          name="password"
        />
      </label>

      <button type="submit" disabled={loading}>
        {loading ? "Trying to login..." : "Login"}
      </button>
    </form>
  );
}
