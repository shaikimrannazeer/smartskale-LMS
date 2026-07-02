/**
 * Frontend types
 */
export interface User {
  id: string;
  email: string;
  name: string;
  role: string;
}

export interface ApiResponse<T> {
  success: boolean;
  message: string;
  data?: T;
  error_code?: string;
  details?: Record<string, unknown>;
}
