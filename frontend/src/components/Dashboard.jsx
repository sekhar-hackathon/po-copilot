import React, { useState, useEffect } from 'react';
import { fetchBearingHealthScores } from '../services/api';

const Dashboard = () => {
  const [healthScores, setHealthScores] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadHealthScores = async () => {
      try {
        const scores = await fetchBearingHealthScores();
        setHealthScores(scores);
      } catch (error) {
        console.error('Failed to load health scores:', error);
      } finally {
        setLoading(false);
      }
    };

    loadHealthScores();
  }, []);

  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <div className="dashboard">
      <h1>Bearing Health Dashboard</h1>
      <ul>
        {healthScores.map((score, index) => (
          <li key={index}>
            <h2>Bearing {score.bearingId}</h2>
            <p>Health Score: {score.healthScore}</p>
            <button onClick={() => alert(`Details for Bearing ${score.bearingId}`)}>View Details</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Dashboard;
