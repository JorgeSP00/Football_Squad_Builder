import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes, Link, useNavigate } from 'react-router-dom';
import Players from './pages/players'; 
import Nationalities from './pages/nationalities'; 
import Teams from './pages/teams';
import SquadBuilder from './pages/squad_builder';
import UserZone from './pages/user_zone';
import { getCompetitions, getFilteredPlayers, getNationalities, verifyUser, postNewUser  } from './services/api';
import './App.css';

function App() {
  const [showPopup, setShowPopup] = useState(false);
  const [showLoginPopup, setShowLoginPopup] = useState(false);
  const [showSignupPopup, setShowSignupPopup] = useState(false);
  const [competitions, setCompetitions] = useState([]);
  const [nationalities, setNationalities] = useState([]);
  const [selectedCompetition, setSelectedCompetition] = useState('');
  const [selectedNationality, setSelectedNationality] = useState('');
  const [budget, setBudget] = useState('');
  const [playersList, setPlayersList] = useState([]);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [userId, setUserId] = useState('');
  const [email, setEmail] = useState('');

  useEffect(() => {
    const fetchCompetitions = async () => {
      try {
        const competitionsResponse = await getCompetitions();
        setCompetitions(competitionsResponse.competitions);
      } catch (error) {
        console.error('Error fetching competitions:', error);
      }
    };
    fetchCompetitions();
  }, []);

  useEffect(() => {
    const fetchNationalities = async () => {
      try {
        const nationalitiesResponse = await getNationalities();
        setNationalities(nationalitiesResponse.nationalities);
      } catch (error) {
        console.error('Error fetching nationalities:', error);
      }
    };
    fetchNationalities();
  }, []);

  const closePopup = () => {
    setShowPopup(false);
  };

  const createSquad = async () => {
    try {
      const filteredPlayersData = await getFilteredPlayers(selectedCompetition, selectedNationality, budget);
      setPlayersList(filteredPlayersData);
    } catch (error) {
      console.error('Error fetching filtered players:', error);
    }

    closePopup();
  };

  return (
    <Router>
      <div className="App">
        <Routes>
          {/* Main Page */}
          <Route
            path="/"
            element={<HomePage 
              showPopup={showPopup} 
              setShowPopup={setShowPopup} 
              showLoginPopup={showLoginPopup}
              setShowLoginPopup={setShowLoginPopup}
              showSignupPopup={showSignupPopup}
              setShowSignupPopup={setShowSignupPopup}
              competitions={competitions}
              selectedCompetition={selectedCompetition}
              setSelectedCompetition={setSelectedCompetition}
              nationalities={nationalities}
              selectedNationality={selectedNationality}
              setSelectedNationality={setSelectedNationality}
              budget={budget}
              setBudget={setBudget}
              playersList={playersList}
              createSquad={createSquad}
              username={username}
              setUsername={setUsername}
              password={password}
              setPassword={setPassword}
              email={email}
              setEmail={setEmail}
              userId={userId}
              setUserId={setUserId}
            />}
          />

          {/* All routes */}

          <Route path="/players" element={<Players />} />

          <Route path="/nationalities" element={<Nationalities />} />

          <Route path="/teams" element={<Teams />} />

          <Route path="/squad_builder" element={
              <SquadBuilder
                playersList={playersList}
                selectedCompetition={selectedCompetition}
                selectedNationality={selectedNationality}
                budget={budget}
              />
            }
          />

          <Route path="/user_zone" element={
              <UserZone 
                user_id={userId}
              />
            }
          />
        </Routes>
      </div>
    </Router>
  );
}

function HomePage({ 
  showPopup, setShowPopup, showLoginPopup, setShowLoginPopup,
  competitions, selectedCompetition, setSelectedCompetition,
  nationalities, selectedNationality, setSelectedNationality, 
  budget, setBudget, createSquad, username, setUsername, password, 
  setPassword, setUserId, showSignupPopup, setShowSignupPopup,
  email, setEmail
}) {
  const navigate = useNavigate();

  const handleLogin = async () => {
    try {
      const response = await verifyUser( username, password );
      setUserId(response);
      setShowLoginPopup(false);
      navigate(`/user_zone`);
      setPassword('');
      setUsername('');
    } catch (error) {
      console.error('Error logging in:', error);
      alert('Login failed. Please check your credentials.');
    }
  };

  const handleSignup = async () => {
    try {
      await postNewUser(username, email, password);
      alert('User registered successfully');
      setShowSignupPopup(false);
      setUsername('');
      setEmail('');
      setPassword('');
    } catch (error) {
      console.error('Error signing up:', error);
      alert('Signup failed. Please try again.');
    }
  };

  return (
    <div className="overlay">
      <h1>Welcome to Football Players App</h1>

      <button onClick={() => setShowPopup(true)}>New Squad</button>

      <Link to="/players" align="center">
        <button>See Players</button>
      </Link>

      <button onClick={() => setShowLoginPopup(true)}>Login</button>

      <button onClick={() => setShowSignupPopup(true)}>Signup</button>

      {showPopup && (
        <div className="popup">
          <div className="popup-content">
            <h2>Limitations</h2>

            <label>Competition:</label>
            <select
              value={selectedCompetition}
              onChange={(e) => setSelectedCompetition(e.target.value)}
              style={{ marginBottom: '10px', width: '100%' }}
            >
              <option value="">Select Competition</option>
              {competitions.map((comp) => (
                <option key={comp.id} value={comp.id}>
                  {comp.name}
                </option>
              ))}
            </select>

            <label>Nationality:</label>
            <select
              value={selectedNationality}
              onChange={(e) => setSelectedNationality(e.target.value)}
              style={{ marginBottom: '10px', width: '100%' }}
            >
              <option value="">Select Nationality</option>
              {nationalities.map((comp) => (
                <option key={comp.id} value={comp.id}>
                  {comp.name}
                </option>
              ))}
            </select>

            <label>Budget (M. €):</label>
            <input
              type="number"
              placeholder="Enter budget"
              value={budget}
              onChange={(e) => setBudget(e.target.value)}
              style={{ marginBottom: '10px', width: '100%' }}
            />

            <button onClick={() => setShowPopup(false)} style={{ marginRight: '10px' }}>
              Cancel
            </button>
            <Link to="/squad_builder" align="center">
              <button onClick={createSquad}>
                Create Squad
              </button>
            </Link>
          </div>
        </div>
      )}

      {showLoginPopup && (
        <div className="popup">
          <div className="popup-content">
            <h2>Login</h2>
            <label>Username:</label>
            <input
              type="text"
              placeholder="Enter username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              style={{ marginBottom: '10px', width: '100%' }}
            />
            <label>Password:</label>
            <input
              type="password"
              placeholder="Enter password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              style={{ marginBottom: '10px', width: '100%' }}
            />
            <button onClick={handleLogin} style={{ marginRight: '10px' }}>
              Login
            </button>
            <button onClick={() => setShowLoginPopup(false)}>Cancel</button>
          </div>
        </div>
      )}

      {showSignupPopup && (
        <div className="popup">
          <div className="popup-content">
            <h2>Sign Up</h2>
            <label>Username:</label>
            <input
              type="text"
              placeholder="Enter username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              style={{ marginBottom: '10px', width: '100%' }}
            />
            <label>Email:</label>
            <input
              type="email"
              placeholder="Enter email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              style={{ marginBottom: '10px', width: '100%' }}
            />
            <label>Password:</label>
            <input
              type="password"
              placeholder="Enter password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              style={{ marginBottom: '10px', width: '100%' }}
            />
            <button onClick={handleSignup} style={{ marginRight: '10px' }}>
              Sign Up
            </button>
            <button onClick={() => setShowSignupPopup(false)}>Cancel</button>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
