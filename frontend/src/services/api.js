import axios from 'axios';

export const fetchBearingHealthScores = async () => {
  try {
    const response = await axios.get('/api/bearing-health-scores');
    return response.data;
  } catch (error) {
    console.error('Error fetching bearing health scores:', error);
    throw error;
  }
};
