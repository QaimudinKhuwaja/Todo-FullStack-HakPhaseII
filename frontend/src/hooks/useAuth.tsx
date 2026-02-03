"use client"

import { createContext, useContext, useState, useEffect, ReactNode, useCallback } from 'react';
import { useRouter } from 'next/navigation';
import { AuthEndpoints } from '../lib/api/endpoints';
import { User, LoginCredentials, RegisterCredentials } from '../types/auth';
import { ApiError } from '../lib/api/client';
import { setAuthToken, getAuthToken, removeAuthToken } from '../lib/auth/token';

// -------------------- Context Type --------------------
export interface AuthContextType {
  user: User | null;
  isLoggedIn: boolean;
  login: (credentials: LoginCredentials) => Promise<void>;
  register: (credentials: RegisterCredentials) => Promise<void>;
  logout: () => Promise<void>;
  isLoading: boolean;
  error: string | null;
}

// -------------------- Context --------------------
export const AuthContext = createContext<AuthContextType | undefined>(undefined);

// -------------------- Provider --------------------
export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();

  const fetchUser = useCallback(async () => {
    // If no token, skip fetching user
    const token = getAuthToken();
    if (!token) {
      setUser(null);
      setIsLoading(false);
      return;
    }

    try {
      const userData = await AuthEndpoints.me();
      setUser(userData);
    } catch (err: any) {
      // Treat unauthorized or not found as "not logged in"
      if (err instanceof ApiError && (err.status === 401 || err.status === 404)) {
        setUser(null);
        removeAuthToken();
      } else {
        console.error('Failed to fetch user:', err);
        setError('Failed to fetch user data.');
      }
    } finally {
      setIsLoading(false);
    }
  }, []); // Remove router from dependency - not needed

  // -------------------- Fetch User on Mount --------------------
  useEffect(() => {
    fetchUser();
  }, [fetchUser]);

  // -------------------- Login --------------------
  const login = async (credentials: LoginCredentials) => {
    setIsLoading(true);
    setError(null);
    try {
   // Line 67-72 ko isse replace karo:
const resp = await AuthEndpoints.login(credentials);
// Store token if present
const token = (resp as any)?.access_token || (resp as any)?.token || (resp as any)?.access;
if (token) {
  setAuthToken(token);
}
      await fetchUser(); // Fetch user data after login
      router.push('/dashboard');
    } catch (err: any) {
      setError(err?.message || 'Login failed');
      throw err;
    } finally {
      setIsLoading(false);
    }
  };

  // -------------------- Register --------------------
  const register = async (credentials: RegisterCredentials) => {
    setIsLoading(true);
    setError(null);
    try {
      await AuthEndpoints.register(credentials);
      router.push('/login');
    } catch (err: any) {
      setError(err?.message || 'Registration failed');
      throw err;
    } finally {
      setIsLoading(false);
    }
  };

  // -------------------- Logout --------------------
  const logout = async () => {
    setIsLoading(true);
    setError(null);
    try {
      await AuthEndpoints.logout();
    } catch (err: any) {
      // Ignore server errors for logout, still clear client state
      console.warn('Logout request failed:', err);
    } finally {
      removeAuthToken();
      setUser(null);
      setIsLoading(false);
      router.push('/login');
    }
  };

  // -------------------- Derived --------------------
  const isLoggedIn = !!user;

  return (
    <AuthContext.Provider
      value={{ user, isLoggedIn, login, register, logout, isLoading, error }}
    >
      {children}
    </AuthContext.Provider>
  );
};

// -------------------- Hook --------------------
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};