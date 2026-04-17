import React from 'react';

const OperatorDashboardWireframe = () => {
  return (
    <div className="dashboard-wireframe">
      <header className="dashboard-header">
        <h1>Operator Dashboard</h1>
      </header>
      <main className="dashboard-main">
        <section className="health-scores">
          <h2>Health Scores</h2>
          <div className="score-card">
            <p>Score: 85</p>
            <button>Drill Down</button>
          </div>
          <div className="score-card">
            <p>Score: 90</p>
            <button>Drill Down</button>
          </div>
        </section>
        <section className="details">
          <h2>Details</h2>
          <p>Select a score to view details.</p>
        </section>
      </main>
    </div>
  );
};

export default OperatorDashboardWireframe;
