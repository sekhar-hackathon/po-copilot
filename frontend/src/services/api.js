import axios from 'axios';

export const fetchBearingHealthScores = async () => {
  const response = await axios.get('/api/bearing-health-scores');
  return response.data;
};
