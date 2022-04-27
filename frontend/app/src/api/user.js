import { instance } from '../Instance';


export const getAccessToken = async (data) => {
    const response = await instance.post('auth/access-token', data);
    return response.data.access_token;
}


export const setupUser = async (user) => {
    try {
        const response = await instance.get('users/me');
        user.set(response.data);
    } catch (error) {
        user.set(null);
    }
}