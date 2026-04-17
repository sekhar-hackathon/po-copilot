import React, { useState, useEffect } from 'react';
import { fetchBearingHealthScores } from '../services/api';
import BearingHealthCard from './BearingHealthCard';

const Dashboard = () => {
  const [bearingScores, setBearingScores] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadBearingScores = async () => {
      try {
        const scores = await fetchBearingHealthScores();
        setBearingScores(scores);
      } catch (error) {
        console.error('Failed to load bearing scores:', error);
      } finally {
        setLoading(false);
      }
    };

    loadBearingScores();
  }, []);

  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <div className="dashboard">
      <h1>Bearing Health Dashboard</h1>
      <div className="bearing-list">
        {bearingScores.map((score) => (
          <BearingHealthCard key={score.id} score={score} />
        ))}
      </div>
    </div>
  );
};

export default Dashboard;
