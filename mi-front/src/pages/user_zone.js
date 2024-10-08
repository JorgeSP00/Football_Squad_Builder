import React, { useState, useEffect } from 'react';
import { Routes, Route, Link, useNavigate } from 'react-router-dom';
import { getUserSquads, getFilteredPlayers, getSquadPlayers, getCompetitions, getNationalities } from '../services/api';
import SquadBuilder from './squad_builder';

const UserZone = ({ user_id }) => {
  const [userId, setUserId] = useState(user_id);
  const [userSquads, setUserSquad] = useState([]);
  const [selectedSquad, setSelectedSquad] = useState(null);
  const [competitions, setCompetitions] = useState([]);
  const [nationalities, setNationalities] = useState([]);

  const navigate = useNavigate();
  
  const [showPopup, setShowPopup] = useState(false);
  const [selectedCompetition, setSelectedCompetition] = useState('');
  const [selectedNationality, setSelectedNationality] = useState('');
  const [budget, setBudget] = useState('');

  // Go to main page if there is not userId
  useEffect(() => {
    if (!userId) {
      navigate('/');
    }
  }, [userId, navigate]);

  useEffect(() => {
    setUserId(user_id);
  }, [user_id, userId]);

  useEffect(() => {
    const fetchUserSquads = async () => {
      try {
        const response = await getUserSquads(userId);
        setUserSquad(response);
      } catch (err) {
        console.error('Error loading personal squads:', err);
      }
    };

    fetchUserSquads();
  }, [userId]);

  const createSquad = async () => {
    try {
      const playersList = await getFilteredPlayers(selectedCompetition, selectedNationality, budget);
      const user_id = userId;
      setSelectedSquad({
        selectedCompetition,
        playersList,
        selectedNationality,
        budget,
        user_id,
      });

    } catch (error) {
      console.error('Error fetching filtered players:', error);
    }

    setShowPopup(false);
  };
  
  const handleSelectSquad = async (squad_id, competition_id, budget, nationality_id) => {
    try {
      const playersList = await getFilteredPlayers(competition_id, nationality_id, budget);
      const players_in_squad = await getSquadPlayers(squad_id);
      setSelectedSquad({
        selectedCompetition: competition_id,
        playersList,
        selectedNationality: nationality_id,
        budget,
        user_id: userId,
        players_in_squad,
        squad_id,
      });
    } catch (error) {
      console.error('Error while getting information of squad.', error);
    }
  };

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

  return (
    <div className="overlay">
      <h1>Welcome to the user zone!</h1>

      {!selectedSquad ? (
        <div>
          <table border="1">
            <thead>
              <tr>
                <th>Nombre</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              {userSquads.map((userSquad, index) => (
                <tr key={index}>
                  <td>{userSquad.name}</td>
                  <td>
                    <button
                      onClick={() =>
                        handleSelectSquad(
                          userSquad.id,
                          userSquad.competition_id,
                          userSquad.budget,
                          userSquad.nationality_id
                        )
                      }
                    >
                      Select
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>

          <br/>
          <br/>
          <br/>

          <footer className="footer">
            <Link to="/">
              <button>Home</button>
            </Link>
          </footer>
          <button onClick={() => setShowPopup(true)}>New Squad</button>
          
          {showPopup && (
            <div className="popup">
              <div className="popup-content">
                <h2>Create New Squad</h2>

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

                <label>Maximum Budget (M. €):</label>
                <input
                  type="number"
                  placeholder="Enter budget"
                  value={budget}
                  onChange={(e) => setBudget(e.target.value)}
                  style={{ marginBottom: '10px', width: '100%' }}
                />

                {/* Botones para cerrar el pop-up o crear el squad */}
                <button onClick={createSquad}>
                  Create Squad
                </button>
                <button onClick={() => setShowPopup(false)} style={{ marginRight: '10px' }}>
                  Cancel
                </button>
              </div>
            </div>
          )}
        </div>
      ) : (
        <>
          <Link to="/squad_builder"></Link>
          <Routes>
            <Route
              path="*"
              element={<SquadBuilder
                playersList={selectedSquad.playersList}
                selectedCompetition={selectedSquad.selectedCompetition}
                selectedNationality={selectedSquad.selectedNationality}
                budget={selectedSquad.budget}
                user_id={selectedSquad.user_id}
                players_in_squad={selectedSquad.players_in_squad}
                squad_id={selectedSquad.squad_id} />}
            />
          </Routes>
        </>
      )}
    </div>
  );
};

export default UserZone;