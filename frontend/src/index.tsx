import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';

import { Provider } from './service/stateStore';

const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);
root.render(
  <Provider>  
    <React.StrictMode>
      <App />
    </React.StrictMode>
  </Provider>
);
