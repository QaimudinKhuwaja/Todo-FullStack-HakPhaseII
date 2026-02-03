export interface User {
  id: number;
  username: string;
  email: string;
  is_active: boolean;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
}

// ✅ ADD THIS
export interface LoginCredentials {
  email: string;
  password: string;
}

// ✅ ADD THIS
export interface RegisterCredentials {
  username: string;
  email: string;
  password: string;
}
