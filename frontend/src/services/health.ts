/**
 * Health check service
 */
import api from './api';

export interface HealthResponse {
  status: string;
  application: string;
  version: string;
}

export const healthService = {
  checkHealth: async (): Promise<HealthResponse> => {
    const response = await api.get<HealthResponse>('/health');
    return response.data;
  },
};
