export const API_ENDPOINT = process.env.REACT_APP_API_URL
export const AUTH_ENDPOINTS = API_ENDPOINT + "/auth"
export const LOGIN_ENDPOINT = AUTH_ENDPOINTS + "/login"
export const LOGOUT_ENDPOINT = AUTH_ENDPOINTS + "/logout"
console.log("a", API_ENDPOINT, "b", AUTH_ENDPOINTS, "c", LOGIN_ENDPOINT, "ENDPOINTS")