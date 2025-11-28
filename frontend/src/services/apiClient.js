import axios from "axios";

const API_URL = "http://127.0.0.1:8000/api/services/health";

export const getServicesStatus = async () => {
  const res = await axios.get(API_URL);
  return res.data;
};
