import React, { useState, useEffect, useMemo } from 'react';
import '../App.css';
import { Link } from 'react-router-dom';
import { postSquad, postSquadPlayers, putSquadPlayers, deleteSquadPlayers } from '../services/api';

const SquadBuilder = ({ selectedCompetition, playersList, selectedNationality, budget, user_id, players_in_squad, squad_id }) => {
  const [players, setPlayers] = useState(playersList);
  const [selectedCompetitionLimit, setSelectedCompetition] = useState(selectedCompetition);
  const [selectedNationalityLimit, setSelectedNationality] = useState(selectedNationality);
  const [budgetLimit, setBudget] = useState(budget);
  const [filteredPlayers, setFilteredPlayers] = useState([]);
  const [squad, setSquad] = useState(players_in_squad || []);
  const [savedPlayers, setSavedPlayers] = useState([]);
  const [filterName, setFilterName] = useState('');
  const [selectedPlayer, setSelectedPlayer] = useState(null);
  const [selectedPosition, setSelectedPosition] = useState('');
  const [showPopup, setShowPopup] = useState(false);
  const [filterPosition, setFilterPosition] = useState('');
  const [maxMarketValue, setMaxMarketValue] = useState('');
  const [sortConfig, setSortConfig] = useState({ key: null, direction: 'ascending' });
  const [squadSortConfig, setSquadSortConfig] = useState({ key: 'position', direction: 'ascending' });
  const [squadId, setSquadId] = useState(squad_id);
  const [userId, setUserId] = useState(user_id);
  const [squadName, setSquadName] = useState('');

  const positions = useMemo(() => ['GK', 'LB', 'CB', 'RB', 'CDM', 'CM', 'CAM', 'RM', 'LM', 'RW', 'LW', 'ST'], []);

  useEffect(() => {
    if (userId !== user_id) {
      setUserId(user_id);
    }
  }, [user_id, userId]);

  useEffect(() => {
    if (players !== playersList) {
      setPlayers(playersList);
    }
  }, [playersList, players]);

  useEffect(() => {
    if (selectedCompetitionLimit !== selectedCompetition) {
      setSelectedCompetition(selectedCompetition);
    }
  }, [selectedCompetition, selectedCompetitionLimit]);

  useEffect(() => {
    if (selectedNationalityLimit !== selectedNationality) {
      setSelectedNationality(selectedNationality);
    }
  }, [selectedNationality, selectedNationalityLimit]);

  useEffect(() => {
    if (budgetLimit !== budget) {
      setBudget(budget);
    }
  }, [budget, budgetLimit]);

  // Filter players
  useEffect(() => {
    let filtered = players.filter((player) => {
      const matchesName = player.name.toLowerCase().includes(filterName.toLowerCase());
      const matchesPosition = filterPosition ? player.position === filterPosition : true;
      const matchesMarketValue = maxMarketValue ? player.market_value <= parseFloat(maxMarketValue) : true;
      const notInSquad = !squad.some((p) => p.id === player.id);
      return matchesName && matchesPosition && matchesMarketValue && notInSquad;
    });

    // Sort the players
    if (sortConfig.key) {
      filtered = filtered.sort((a, b) => {
        const orderMultiplier = sortConfig.direction === 'ascending' ? 1 : -1;
        if (sortConfig.key === 'position') {
          const posA = positions.indexOf(a.position);
          const posB = positions.indexOf(b.position);
          return (posA - posB) * orderMultiplier;
        } else {
          if (a[sortConfig.key] < b[sortConfig.key]) return -1 * orderMultiplier;
          if (a[sortConfig.key] > b[sortConfig.key]) return 1 * orderMultiplier;
          return 0;
        }
      });
    }

    setFilteredPlayers(filtered);
  }, [filterName, filterPosition, maxMarketValue, players, squad, sortConfig, positions]);


  useEffect(() => {
    if (players_in_squad) {
      // Map players
      const mappedSquad = players_in_squad.map((squadPlayer) => {
        const fullPlayer = playersList.find((player) => player.id === squadPlayer.player_id);
        return fullPlayer ? { ...fullPlayer, position: squadPlayer.position, id: squadPlayer.id, player_id: squadPlayer.player_id } : null;
      }).filter(player => player !== null);
      
      setSquad(mappedSquad);
      setSavedPlayers(mappedSquad);
    }
  }, [players_in_squad, playersList]);

  // Sort players
  const requestSort = (key) => {
    let direction = 'ascending';
    if (sortConfig.key === key && sortConfig.direction === 'ascending') {
      direction = 'descending';
    }
    setSortConfig({ key, direction });
  };

  // Sort squad
  const requestSquadSort = (key) => {
    let direction = 'ascending';
    if (squadSortConfig.key === key && squadSortConfig.direction === 'ascending') {
      direction = 'descending';
    }
    setSquadSortConfig({ key, direction });
  };

  // Add to squad
  const addToSquad = () => {
    if (squad.length >= 11) {
      alert('The squad is full! You can just add 11 players.');
    } else if (selectedPlayer && selectedPosition) {
      const newPlayer = { ...selectedPlayer, position: selectedPosition, player_id: selectedPlayer.id };
      setSquad([...squad, newPlayer]);
      setSelectedPlayer(null);
      setSelectedPosition('');
      setFilterName('');
      setShowPopup(false);
    } else {
      alert('Selecciona un jugador y una posición antes de añadir');
    }
  };

  // Delete from squad
  const removeFromSquad = (player) => {
    const updatedSquad = squad.filter((p) => p.player_id !== player.player_id);
    setSquad(updatedSquad);
  };

  // Save squad
  const saveSquad = async () => {
    try {
      // Not having squadId means that we have never saved the squad
      if (!squadId) {
        // If the squad has never been saved, we ask for the name
        const name = window.prompt('Squad Name:', squadName || '');
        if (name) {
          setSquadName(name);
        }
        const response = await postSquad(selectedCompetitionLimit, selectedNationalityLimit, budgetLimit, userId, name);
        await saveSquadPlayers(response.data.id);
        setSquadId(response.data.id);
      } else {
        await saveSquadPlayers(squadId);
      }
    } catch (error) {
      console.error('Error saving squad:', error);
      alert('Error saving squad.');
    }
  };

  const saveSquadPlayers = async (squadId) => {
    try {
      // Get which players of the squad are new, which one has not been changed, which one were changed of position and which ones where deleted.
      const newPlayers = squad.filter(
        (player) => !savedPlayers.some((sp) => sp.player_id === player.player_id)
      );

      const modifiedPlayers = savedPlayers
        .filter((savedPlayer) =>
          squad.some(
            (player) =>
              player.player_id === savedPlayer.player_id &&
              player.position !== savedPlayer.position
          )
        )
        .map((savedPlayer) => {
          const matchingPlayer = squad.find(
            (player) => player.player_id === savedPlayer.player_id
          );

          return {
            ...savedPlayer,
            position: matchingPlayer.position
          };
        });


      const removedPlayers = savedPlayers.filter(
        (savedPlayer) =>
          !squad.some((player) => player.player_id === savedPlayer.player_id)
      );

      // POST new players
      if (newPlayers.length > 0) {
        try {
          const postResponses = await Promise.all(
            newPlayers.map((player) => postSquadPlayers([player], squadId))
          );

          const newSavedPlayers = postResponses.flatMap((responseArray) => {
            if (Array.isArray(responseArray) && responseArray.length > 0) {
              const response = responseArray[0];
              if (response && response.data) {
                return response.data;
              }
            }
            console.warn('Unexpected response structure:', responseArray);
            return null;
          }).filter((item) => item !== null);

          setSavedPlayers((prev) => [...prev, ...newSavedPlayers]);
        } catch (error) {
          console.error('Error en postSquadPlayers:', error);
        }
      }

      // PUT changed players
      if (modifiedPlayers.length > 0) {
        await putSquadPlayers(modifiedPlayers, squadId);

        setSavedPlayers((prev) => {
          const unmodifiedPlayers = prev.filter(
            (savedPlayer) =>
              !modifiedPlayers.some(
                (modifiedPlayer) =>
                  modifiedPlayer.player_id === savedPlayer.player_id
              )
          );

          const updatedPlayers = modifiedPlayers.map((modifiedPlayer) => {
            const updatedSquadPlayer = squad.find(
              (player) => player.player_id === modifiedPlayer.player_id
            );

            return {
              ...modifiedPlayer,
              position: updatedSquadPlayer.position,
            };
          });

          return [...unmodifiedPlayers, ...updatedPlayers];
        });
      }

      // DELETE deleted players
      if (removedPlayers.length > 0) {
        await deleteSquadPlayers(
          removedPlayers.map((player) => player.id),
          squadId
        );

        setSavedPlayers((prev) =>
          prev.filter(
            (savedPlayer) =>
              !removedPlayers.some((rp) => rp.id === savedPlayer.id)
          )
        );
      }

      alert('Squad saved successfully!');
    } catch (error) {
      console.error('Error saving squad players:', error);
      alert('Error saving squad players.');
    }
  };

  return (
    <div style={{ display: 'flex', justifyContent: 'space-between' }}>
      <div>
        <div className="overlay">
          <h2>Búsqueda de Jugadores</h2>
          <input
            type="text"
            placeholder="Name"
            value={filterName}
            onChange={(e) => setFilterName(e.target.value)}
            style={{ marginBottom: '10px', width: '100%' }}
          />
          <select
            value={filterPosition}
            onChange={(e) => setFilterPosition(e.target.value)}
            style={{ marginBottom: '10px', width: '100%' }}
          >
            <option value="">Filtrar por posición</option>
            {positions.map((pos) => (
              <option key={pos} value={pos}>
                {pos}
              </option>
            ))}
          </select>
          <input
            type="number"
            placeholder="Max. Market value (€)"
            value={maxMarketValue}
            onChange={(e) => setMaxMarketValue(e.target.value)}
            style={{ marginBottom: '10px', width: '100%' }}
          />

          {filteredPlayers.length === 0 ? (
            <p>No data found</p>
          ) : (
            <><table border="1" style={{ width: '100%' }}>
                <thead>
                  <tr>
                    <th onClick={() => requestSort('name')} style={{ cursor: 'pointer' }}>
                      NAME {sortConfig.key === 'name' && (sortConfig.direction === 'ascending' ? '▲' : '▼')}
                    </th>
                    <th onClick={() => requestSort('position')} style={{ cursor: 'pointer' }}>
                      POS {sortConfig.key === 'position' && (sortConfig.direction === 'ascending' ? '▲' : '▼')}
                    </th>
                    <th onClick={() => requestSort('market_value')} style={{ cursor: 'pointer' }}>
                      MARKET VALUE {sortConfig.key === 'market_value' && (sortConfig.direction === 'ascending' ? '▲' : '▼')}
                    </th>
                    <th>SELECT</th>
                  </tr>
                </thead>
                <tbody>
                  {filteredPlayers.map((player, index) => (
                    <tr key={index}>
                      <td>{player.name}</td>
                      <td>{player.position}</td>
                      <td>{player.market_value}M. €</td>
                      <td>
                        <button
                          onClick={() => {
                            setSelectedPlayer(player);
                            setSelectedPosition(player.position);
                            setShowPopup(true);
                          } }
                        >
                          Select Player
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table><br /><br /><br /></>
          )}
        </div>
      </div>

      {/* Columna derecha: Squad */}
      <div className="overlay" style={{ flex: 1, marginLeft: '20px', justifyContent: 'start' }}>
        <h2>Squad</h2>

        {squad.length === 0 ? (
          <p>Any player has been added to the squad. Start selecting players!</p>
        ) : (
          <>
            <table border="1" style={{ width: '100%' }}>
              <thead>
                <tr>
                  <th onClick={() => requestSquadSort('name')} style={{ cursor: 'pointer' }}>
                    NAME {squadSortConfig.key === 'name' && (squadSortConfig.direction === 'ascending' ? '▲' : '▼')}
                  </th>
                  <th onClick={() => requestSquadSort('position')} style={{ cursor: 'pointer' }}>
                    POS {squadSortConfig.key === 'position' && (squadSortConfig.direction === 'ascending' ? '▲' : '▼')}
                  </th>
                  <th onClick={() => requestSquadSort('market_value')} style={{ cursor: 'pointer' }}>
                    MARKET VALUE {squadSortConfig.key === 'market_value' && (squadSortConfig.direction === 'ascending' ? '▲' : '▼')}
                  </th>
                  <th>DELETE</th>
                </tr>
              </thead>
              <tbody>
                {squad.map((player, index) => (
                  <tr key={index}>
                    <td>{player.name}</td>
                    <td>
                      <select
                        value={player.position}
                        onChange={(e) => {
                          const updatedSquad = squad.map((p) =>
                            p.id === player.id ? { ...p, position: e.target.value } : p
                          );
                          setSquad(updatedSquad);
                        }}
                      >
                        {positions.map((pos) => (
                          <option key={pos} value={pos}>
                            {pos}
                          </option>
                        ))}
                      </select>
                    </td>
                    <td>{player.market_value}M. €</td>
                    <td>
                      <button onClick={() => removeFromSquad(player)}>Eliminar</button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
            

            <br/>
            <br/>
            <br/>
            {userId && (
              <div>
                <button onClick={saveSquad}>Save Squad</button>
              </div>
            )}
          </>
        )}
        <footer className="footer">
          <Link to="/">
            <button>Home</button>
          </Link>
        </footer>
      </div>

      {/* Pop-up for choosing football player position */}
      {showPopup && selectedPlayer && (
        <div className="popup">
          <div className="popup-content">
            <h4>Selected player: {selectedPlayer.name}</h4>
            <select
              value={selectedPosition}
              onChange={(e) => setSelectedPosition(e.target.value)}
              style={{ marginBottom: '10px', width: '100%', marginTop: '10px' }}
            >
              {positions.map((pos) => (
                <option key={pos} value={pos}>
                  {pos}
                </option>
              ))}
            </select>
            <button onClick={addToSquad}>Add to the squad</button>
            <button onClick={() => setShowPopup(false)}>Cancel</button>
          </div>
        </div>
      )}
    </div>
  );
};

export default SquadBuilder;