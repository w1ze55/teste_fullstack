// API Configuration
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

export const API_ENDPOINTS = {
  // Auth endpoints
  LOGIN: `${API_BASE_URL}/auth/login`,
  REGISTER: `${API_BASE_URL}/auth/register`,
  VERIFY: `${API_BASE_URL}/auth/verify`,
  PROFILE: `${API_BASE_URL}/auth/profile`,
  PERMISSIONS: `${API_BASE_URL}/auth/permissions`,
  
  // Charging station endpoints
  STATIONS: `${API_BASE_URL}/api/cargas`,
  STATION_BY_ID: (id) => `${API_BASE_URL}/api/cargas/${id}`,
  STATIONS_STATS: `${API_BASE_URL}/api/cargas/stats`,
  STATIONS_BY_LOCATION: `${API_BASE_URL}/api/cargas/by-location`,
  STATIONS_BY_STATUS: (status) => `${API_BASE_URL}/api/cargas/by-status/${status}`,
  STATIONS_BY_TYPE: (type) => `${API_BASE_URL}/api/cargas/by-type/${type}`,
  
  // Health endpoints
  HEALTH: `${API_BASE_URL}/health/check`
};

export default API_BASE_URL;
