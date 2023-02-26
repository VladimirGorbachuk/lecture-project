import './App.css';
import { useAuthenticateInjectedCallableType } from './useCases/authenticate'
import { Auth } from './ui/Auth';
import { DefaultReactElement } from './ui/Default/DefaultReactElement'
import {PropsWithUseAuthenticate} from './di/propTypes'

function App(props: PropsWithUseAuthenticate) {
  const authenticationManager = props.useAuthenticate()
  if(!authenticationManager.user.isAuthenticated){
    console.log(authenticationManager.user, "current state")
    return (
      <Auth
      useAuthenticate={props.useAuthenticate}/>
    )
  }
  return <DefaultReactElement/>
}

export default App;
