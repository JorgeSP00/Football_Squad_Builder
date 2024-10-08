import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { getTeams } from '../services/api';

const Teams = () => {
  const [teams, setTeams] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchNationalities = async () => {
      try {
        const response = await getTeams();
        setTeams(response.teams);
        setLoading(false);
      } catch (err) {
        console.error('Error al cargar teams:', err);
        setError(err);
        setLoading(false);
      }
    };

    fetchNationalities();
  }, []);

  if (loading) return <p>Loading teams...</p>;
  if (error) return <p>Error loading teams: {error.message}</p>;

  return (
    <div>
      <div className="overlay">
        <h2>Teams</h2>
      </div>
      <table border="1" align="center">
        <thead>
          <tr>
            <th>Name</th>
          </tr>
        </thead>
        <tbody>
          {teams.map((nationality, index) => (
            <tr key={index}>
              <td>{nationality.name}</td>
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
        <Link to="/players/">
          <button>Players</button>
        </Link>
      </footer>
    </div>
  );
};

export default Teams;
