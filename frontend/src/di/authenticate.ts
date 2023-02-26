import { useAuthenticate, useAuthenticateInjectedCallableType } from "../useCases/authenticate";
import {useUserAuthStore} from "../serviceImplementations/store/stateStore"
import {AuthenticationService} from "../serviceImplementations/api/auth"

export const useAuthenticateInjected: useAuthenticateInjectedCallableType = () => {
    return useAuthenticate(useUserAuthStore, AuthenticationService)
}