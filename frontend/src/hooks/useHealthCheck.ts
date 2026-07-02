/**
 * Custom hook for health check
 */
import { useQuery } from '@tanstack/react-query';
import { healthService } from '../services/health';

export const useHealthCheck = () => {
  return useQuery({
    queryKey: ['health'],
    queryFn: () => healthService.checkHealth(),
    refetchInterval: 30000, // Refetch every 30 seconds
  });
};
