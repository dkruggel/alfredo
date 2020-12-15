import React from 'react';
import './App.css';
import { useAuth0 } from '@auth0/auth0-react';
import { Loading } from './components/Loading';
import Dashboard from './pages/Dashboard';
import { Home } from './pages/Home';
import NavBar from './components/NavBar';

const App = () => {
  const { isLoading, isAuthenticated, user } = useAuth0();

  if (isLoading) {
    return <Loading />;
  }

  if (isAuthenticated) {
    return (
      <>
        <NavBar />
        <div className='container flex-grow-1'>
          <Dashboard user={user.name.toString().slice(0, user.name.toString().indexOf(' ')).toLowerCase()}/>
        </div>
      </>
    );
  } else {
    return (
      <>
        <NavBar />
        <div className='container flex-grow-1'>
          <Home />
        </div>
      </>
    );
  }
};

export default App;
