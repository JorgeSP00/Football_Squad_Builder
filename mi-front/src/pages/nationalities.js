import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { getNationalities } from '../services/api';

const Nationalities = () => {
  const [nationalities, setNationalities] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchNationalities = async () => {
      try {
        const response = await getNationalities();
        setNationalities(response.nationalities);
        setLoading(false);
      } catch (err) {
        console.error('Error loading nationalities:', err);
        setError(err);
        setLoading(false);
      }
    };

    fetchNationalities();
  }, []);

  if (loading) return <p>Loading nationalities...</p>;
  if (error) return <p>Error loading nationalities: {error.message}</p>;

  return (
    <div>
      <div className="overlay">
        <h2>Nationalities</h2>
      </div>
      <table border="1">
        <thead>
          <tr>
            <th>Name</th>
          </tr>
        </thead>
        <tbody>
          {nationalities.map((nationality, index) => (
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

export default Nationalities;
