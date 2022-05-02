import axios from "axios";

export const url = `localhost:8000`

export const instance = axios.create({
	baseURL: `http://${url}/api/`,
});

instance.interceptors.request.use((config) => {
	const token = localStorage.getItem('access_token');
	config.headers.Authorization = token ? `Bearer ${token}` : '';
	return config;
});
