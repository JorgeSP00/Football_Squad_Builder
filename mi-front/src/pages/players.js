import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { getPlayers, getNationalities, getTeams } from '../services/api';
import '../App.css';

const Players = () => {
  const [players, setPlayers] = useState([]);
  const [filteredPlayers, setFilteredPlayers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [sortConfig, setSortConfig] = useState({ key: '', direction: '' });
  const [filterName, setFilterName] = useState('');
  const [filterPosition, setFilterPosition] = useState('');
  const [filterNationality, setFilterNationality] = useState('');
  const [filterTeam, setFilterTeam] = useState('');
  const positions = ['GK', 'LB', 'CB', 'RB', 'CDM', 'CM', 'CAM', 'RM', 'LM', 'RW', 'LW', 'ST'];

  useEffect(() => {
    const fetchData = async () => {
      try {
        const playersResponse = await getPlayers();
        const nationalitiesResponse = await getNationalities();
        const teamsResponse = await getTeams();

        const playersData = playersResponse.players;
        const nationalitiesData = nationalitiesResponse.nationalities;
        const teamsData = teamsResponse.teams;

        if (Array.isArray(playersData) && Array.isArray(nationalitiesData)) {
          const nationalitiesMap = {};
          nationalitiesData.forEach(nat => {
            nationalitiesMap[nat.id] = nat.name;
          });

          const teamsMap = {};
          teamsData.forEach(team => {
            teamsMap[team.id] = team.name;
          });

          const playersWithNationality = playersData.map(player => ({
            ...player,
            nationality: nationalitiesMap[player.nationality_id] || 'Unknown',
            team: teamsMap[player.team_id] || 'Unknown',
          }));

          setPlayers(playersWithNationality);
          setFilteredPlayers(playersWithNationality); // Initialize players.
        } else {
          console.error('Incorrect formatted data of players or nationalities:', playersData, nationalitiesData);
          throw new Error('Incorrect data.');
        }

        setLoading(false);
      } catch (err) {
        console.error('Error loading data:', err);
        setError(err);
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  // Sort players
  const handleSort = (key) => {
    let direction = 'asc';
    if (sortConfig.key === key && sortConfig.direction === 'asc') {
      direction = 'desc';
    }
    setSortConfig({ key, direction });

    const sortedPlayers = [...filteredPlayers].sort((a, b) => {
      if (a[key] < b[key]) return direction === 'asc' ? -1 : 1;
      if (a[key] > b[key]) return direction === 'asc' ? 1 : -1;
      return 0;
    });

    setFilteredPlayers(sortedPlayers);
  };

  // Apply any filter
  const applyFilters = () => {
    const filtered = players.filter(player => {
      return (
        player.name.toLowerCase().includes(filterName.toLowerCase()) &&
        (filterPosition === '' || player.position === filterPosition) &&
        player.nationality.toLowerCase().includes(filterNationality.toLowerCase()) &&
        player.team.toLowerCase().includes(filterTeam.toLowerCase())
      );
    });
    setFilteredPlayers(filtered);
  };

  // Changing filter
  const handleFilterChange = (setter) => (e) => {
    setter(e.target.value);
  };

  useEffect(() => {
    applyFilters();
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [filterName, filterPosition, filterNationality, filterTeam]);

  if (loading) return <p>Loading data...</p>;
  if (error) return <p>Error loading data: {error.message}</p>;

  return (
    <div className="container">
      <div className="filters">
        <h3>Filtros de búsqueda</h3>
        <input
          type="text"
          placeholder="Name:"
          value={filterName}
          onChange={handleFilterChange(setFilterName)}
          style={{ marginBottom: '10px', width: '70%'  }}
        />
        
        <select
          value={filterPosition}
          onChange={handleFilterChange(setFilterPosition)}
          style={{ marginBottom: '10px', width: '70%' }}
        >
          <option value="">All positions</option>
          {positions.map((pos) => (
            <option key={pos} value={pos}>
              {pos}
            </option>
          ))}
        </select>

        <input
          type="text"
          placeholder="Nationality"
          value={filterNationality}
          onChange={handleFilterChange(setFilterNationality)}
          style={{ marginBottom: '10px', width: '70%'  }}
        />
        <input
          type="text"
          placeholder="Team"
          value={filterTeam}
          onChange={handleFilterChange(setFilterTeam)}
          style={{ marginBottom: '10px', width: '70%'  }}
        />
      </div>
      
      <div className="table-container">
        <div className="overlay">
            <h1>Players Data</h1>
        </div>
        <table border="1">
          <thead>
            <tr>
              <th onClick={() => handleSort('name')}>Name</th>
              <th onClick={() => handleSort('position')}>Position</th>
              <th onClick={() => handleSort('nationality')}>
                <Link to="/nationalities">Nationality</Link>
              </th>
              <th onClick={() => handleSort('team')}>
                <Link to="/teams">Team</Link>
              </th>
              <th onClick={() => handleSort('market_value')}>Market Value</th>
            </tr>
          </thead>
          <tbody>
            {filteredPlayers.map((player, index) => (
              <tr key={index}>
                <td>{player.name}</td>
                <td>{player.position}</td>
                <td>{player.nationality}</td>
                <td>{player.team}</td>
                <td>{player.market_value}M. €</td>
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
      </div>
    </div>
  );
};

export default Players;
