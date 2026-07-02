/**
 * Updated types
 */
export interface User {
  id: string;
  email: string;
  name: string;
  role: string;
}

export interface CurrentUserResponse {
  user_id: string;
  full_name: string;
  email: string;
  role: 'admin' | 'trainer' | 'student';
  is_active: boolean;
}

export interface ApiResponse<T> {
  success: boolean;
  message: string;
  data?: T;
  error_code?: string;
  details?: Record<string, unknown>;
}

export interface TokenResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  user: CurrentUserResponse;
}
