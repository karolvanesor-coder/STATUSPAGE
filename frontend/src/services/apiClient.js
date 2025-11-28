import axios from "axios";

const API_URL = "http://127.0.0.1:8000/health-today";

export const getServicesToday = async () => {
  const res = await axios.get(API_URL);
  return res.data;
};
