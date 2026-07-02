/**
 * Authentication service
 */
import api from './api';
import { CurrentUserResponse, TokenResponse } from '../types';

export interface RegisterData {
  full_name: string;
  email: string;
  password: string;
  role: 'admin' | 'trainer' | 'student';
}

export interface LoginData {
  email: string;
  password: string;
}

export const authService = {
  register: async (data: RegisterData): Promise<CurrentUserResponse> => {
    const response = await api.post<CurrentUserResponse>('/auth/register', data);
    return response.data;
  },

  login: async (data: LoginData): Promise<TokenResponse> => {
    const response = await api.post<TokenResponse>('/auth/login', data);
    return response.data;
  },

  logout: async (): Promise<void> => {
    await api.post('/auth/logout');
  },

  refreshToken: async (refreshToken: string): Promise<{ access_token: string }> => {
    const response = await api.post<{ access_token: string }>('/auth/refresh', {
      refresh_token: refreshToken,
    });
    return response.data;
  },

  getCurrentUser: async (): Promise<CurrentUserResponse> => {
    const response = await api.get<CurrentUserResponse>('/auth/me');
    return response.data;
  },
};
