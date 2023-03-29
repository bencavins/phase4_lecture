import logo from './logo.svg';
import './App.css';
import { Route, Routes, useNavigate } from 'react-router-dom';
import { useState } from 'react';

import Home from './components/Home';
import Login from './components/Login';

function App() {
  const [user, setUser] = useState({})

  const navigate = useNavigate();

  function handleLoginSubmit(event) {
    // Prevent page refresh
    event.preventDefault()

    // Get data from form
    const data = {
      username: event.target.username.value,
      password: event.target.password.value
    }

    // Send data to flask
    fetch('/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    })
    .then(resp => resp.json())
    .then(data => setUser(data))
    .then(() => navigate('/'))
  }

  return (
    <div className="App">
      {/* <header className="App-header">
      </header> */}
      <Routes>
        <Route exact path='/' element={
          <Home user={user} />
        } />
        <Route exact path='/login' element={
          <Login 
            handleSubmit={handleLoginSubmit} />
        } />
        <Route exact path='/signup' />
        <Route exact path='/logout' />
        <Route exact path='/pets' />
      </Routes>
    </div>
  );
}

export default App;
