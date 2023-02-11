import './App.css';
import {useStore} from './service/stateStore'
import { Auth } from './ui/Auth';
import { DefaultReactElement } from './ui/Default/DefaultReactElement'

function App() {
  const state = useStore()
  if(!state.user.isAuthenticated){
    console.log(state, "current state")
    return (
      <Auth/>
    )
  }
  return <DefaultReactElement/>
}

export default App;
