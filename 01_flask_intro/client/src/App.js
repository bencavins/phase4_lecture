import './App.css';
import { Route, Routes, useNavigate } from 'react-router-dom';
import { useEffect, useState } from 'react';

import Home from './components/Home';
import Login from './components/Login';
import Logout from './components/Logout';
import Signup from './components/Signup';
import Pets from './components/Pets';

function App() {
  const [user, setUser] = useState({})
  const [pets, setPets] = useState([])

  const navigate = useNavigate();

  useEffect(() => {
    fetchUser()
    fetchPets()
  }, [])

  function fetchPets() {
    fetch('/api/pets')
    .then(resp => {
      if (resp.ok) {
        resp.json().then(data => setPets(data))
      } else {
        console.log(resp.status)
      }
    })
  }

  function fetchUser() {
    fetch('/authorized')
    .then(resp => resp.json())
    .then(data => setUser(data))
  }

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

  function handleSignupSubmit(event) {
    // Prevent page refresh
    event.preventDefault()

    // Get data from form
    const data = {
      username: event.target.username.value,
      password: event.target.password.value,
      email: event.target.email.value
    }

    // Send data to flask
    fetch('/signup', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    })
    .then(resp => resp.json())
    .then(() => navigate('/login'))
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
        <Route exact path='/signup' element={
          <Signup 
            handleSubmit={handleSignupSubmit} />
        } />
        <Route exact path='/logout' element={
          <Logout />
        } />
        <Route exact path='/pets' element={
          <Pets pets={pets} />
        } />
      </Routes>
    </div>
  );
}

export default App;
