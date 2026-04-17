import React from 'react';

const BearingHealthCard = ({ score }) => {
  const { id, healthScore, details } = score;

  return (
    <div className="bearing-card">
      <h2>Bearing ID: {id}</h2>
      <p>Health Score: {healthScore}</p>
      <button onClick={() => alert(details)}>View Details</button>
    </div>
  );
};

export default BearingHealthCard;
