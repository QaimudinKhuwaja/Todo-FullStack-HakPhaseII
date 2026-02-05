// // "use client"

// // import { createContext, useContext, useState, useEffect, ReactNode, useCallback } from 'react';
// // import { useRouter } from 'next/navigation';
// // import { AuthEndpoints } from '../lib/api/endpoints';
// // import { User, LoginCredentials, RegisterCredentials } from '../types/auth';
// // import { ApiError } from '../lib/api/client';
// // import { setAuthToken, getAuthToken, removeAuthToken } from '../lib/auth/token';

// // // -------------------- Context Type --------------------
// // export interface AuthContextType {
// //   user: User | null;
// //   isLoggedIn: boolean;
// //   login: (credentials: LoginCredentials) => Promise<void>;
// //   register: (credentials: RegisterCredentials) => Promise<void>;
// //   logout: () => Promise<void>;
// //   isLoading: boolean;
// //   error: string | null;
// // }

// // // -------------------- Context --------------------
// // export const AuthContext = createContext<AuthContextType | undefined>(undefined);

// // // -------------------- Provider --------------------
// // export const AuthProvider = ({ children }: { children: ReactNode }) => {
// //   const [user, setUser] = useState<User | null>(null);
// //   const [isLoading, setIsLoading] = useState(true);
// //   const [error, setError] = useState<string | null>(null);
// //   const router = useRouter();

// //   const fetchUser = useCallback(async () => {
// //     // If no token, skip fetching user
// //     const token = getAuthToken();
// //     if (!token) {
// //       setUser(null);
// //       setIsLoading(false);
// //       return;
// //     }

// //     try {
// //       const userData = await AuthEndpoints.me();
// //       setUser(userData);
// //     } catch (err: any) {
// //       // Treat unauthorized or not found as "not logged in"
// //       if (err instanceof ApiError && (err.status === 401 || err.status === 404)) {
// //         setUser(null);
// //         removeAuthToken();
// //       } else {
// //         console.error('Failed to fetch user:', err);
// //         setError('Failed to fetch user data.');
// //       }
// //     } finally {
// //       setIsLoading(false);
// //     }
// //   }, []); // Remove router from dependency - not needed

// //   // -------------------- Fetch User on Mount --------------------
// //   useEffect(() => {
// //     fetchUser();
// //   }, [fetchUser]);

// //   // -------------------- Login --------------------
// //   const login = async (credentials: LoginCredentials) => {
// //     setIsLoading(true);
// //     setError(null);
// //     try {
// //    // Line 67-72 ko isse replace karo:
// // const resp = await AuthEndpoints.login(credentials);
// // // Store token if present
// // const token = (resp as any)?.access_token || (resp as any)?.token || (resp as any)?.access;
// // if (token) {
// //   setAuthToken(token);
// // }
// //       await fetchUser(); // Fetch user data after login
// //       router.push('/dashboard');
// //     } catch (err: any) {
// //       setError(err?.message || 'Login failed');
// //       throw err;
// //     } finally {
// //       setIsLoading(false);
// //     }
// //   };

// //   // -------------------- Register --------------------
// //   const register = async (credentials: RegisterCredentials) => {
// //     setIsLoading(true);
// //     setError(null);
// //     try {
// //       await AuthEndpoints.register(credentials);
// //       router.push('/login');
// //     } catch (err: any) {
// //       setError(err?.message || 'Registration failed');
// //       throw err;
// //     } finally {
// //       setIsLoading(false);
// //     }
// //   };

// //   // -------------------- Logout --------------------
// //   const logout = async () => {
// //     setIsLoading(true);
// //     setError(null);
// //     try {
// //       await AuthEndpoints.logout();
// //     } catch (err: any) {
// //       // Ignore server errors for logout, still clear client state
// //       console.warn('Logout request failed:', err);
// //     } finally {
// //       removeAuthToken();
// //       setUser(null);
// //       setIsLoading(false);
// //       router.push('/login');
// //     }
// //   };

// //   // -------------------- Derived --------------------
// //   const isLoggedIn = !!user;

// //   return (
// //     <AuthContext.Provider
// //       value={{ user, isLoggedIn, login, register, logout, isLoading, error }}
// //     >
// //       {children}
// //     </AuthContext.Provider>
// //   );
// // };

// // // -------------------- Hook --------------------
// // export const useAuth = () => {
// //   const context = useContext(AuthContext);
// //   if (!context) {
// //     throw new Error('useAuth must be used within an AuthProvider');
// //   }
// //   return context;
// // };




// "use client"

// import { createContext, useContext, useState, useEffect, ReactNode, useCallback } from 'react';
// import { useRouter } from 'next/navigation';
// import { AuthEndpoints } from '../lib/api/endpoints';
// import { User, LoginCredentials, RegisterCredentials } from '../types/auth';
// import { ApiError } from '../lib/api/client';
// import { setAuthToken, getAuthToken, removeAuthToken } from '../lib/auth/token';

// // -------------------- Context Type --------------------
// export interface AuthContextType {
//   user: User | null;
//   isLoggedIn: boolean;
//   login: (credentials: LoginCredentials) => Promise<void>;
//   register: (credentials: RegisterCredentials) => Promise<void>;
//   logout: () => Promise<void>;
//   isLoading: boolean;
//   error: string | null;
// }

// // -------------------- Context --------------------
// export const AuthContext = createContext<AuthContextType | undefined>(undefined);

// // -------------------- Provider --------------------
// export const AuthProvider = ({ children }: { children: ReactNode }) => {
//   const [user, setUser] = useState<User | null>(null);
//   const [isLoading, setIsLoading] = useState(true);
//   const [error, setError] = useState<string | null>(null);
//   const router = useRouter();

//   const fetchUser = useCallback(async () => {
//     const token = getAuthToken();
//     if (!token) {
//       setUser(null);
//       setIsLoading(false);
//       return;
//     }

//     try {
//       const userData = await AuthEndpoints.me();
//       setUser(userData);
//     } catch (err: any) {
//       if (err instanceof ApiError && (err.status === 401 || err.status === 404)) {
//         setUser(null);
//         removeAuthToken();
//       } else {
//         console.error('Failed to fetch user:', err);
//         setError('Failed to fetch user data.');
//       }
//     } finally {
//       setIsLoading(false);
//     }
//   }, []);

//   useEffect(() => {
//     fetchUser();
//   }, [fetchUser]);

//   // -------------------- Login --------------------
//   const login = async (credentials: LoginCredentials) => {
//     setIsLoading(true);
//     setError(null);
//     try {
//       const resp = await AuthEndpoints.login(credentials);

//       // Agar backend body mein token return kar raha hai (optional)
//       const tokenFromBody = (resp as any)?.access_token || (resp as any)?.token || (resp as any)?.access;
//       if (tokenFromBody) {
//         setAuthToken(tokenFromBody);
//       }

//       // Small delay taake browser cookie set kar le (Set-Cookie header process hone ke liye)
//       await new Promise(resolve => setTimeout(resolve, 500));

//       await fetchUser(); // User data fetch karo

//       // Redirect to dashboard
//       router.push('/dashboard');
//       router.refresh(); // Force re-render + cache clear
//     } catch (err: any) {
//       setError(err?.message || 'Login failed');
//       console.error('Login error:', err);
//       throw err;
//     } finally {
//       setIsLoading(false);
//     }
//   };

//   // -------------------- Register --------------------
//   const register = async (credentials: RegisterCredentials) => {
//     setIsLoading(true);
//     setError(null);
//     try {
//       await AuthEndpoints.register(credentials);
//       router.push('/login');
//     } catch (err: any) {
//       setError(err?.message || 'Registration failed');
//       throw err;
//     } finally {
//       setIsLoading(false);
//     }
//   };

//   // -------------------- Logout --------------------
//   const logout = async () => {
//     setIsLoading(true);
//     setError(null);
//     try {
//       await AuthEndpoints.logout();
//     } catch (err: any) {
//       console.warn('Logout request failed:', err);
//     } finally {
//       removeAuthToken();
//       setUser(null);
//       setIsLoading(false);
//       router.push('/login');
//     }
//   };

//   const isLoggedIn = !!user;

//   return (
//     <AuthContext.Provider
//       value={{ user, isLoggedIn, login, register, logout, isLoading, error }}
//     >
//       {children}
//     </AuthContext.Provider>
//   );
// };

// // -------------------- Hook --------------------
// export const useAuth = () => {
//   const context = useContext(AuthContext);
//   if (!context) {
//     throw new Error('useAuth must be used within an AuthProvider');
//   }
//   return context;
// };



"use client"

import { createContext, useContext, useState, useEffect, ReactNode, useCallback } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
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
  const searchParams = useSearchParams();  // Added to get redirect param

  const fetchUser = useCallback(async () => {
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
  }, []);

  useEffect(() => {
    fetchUser();
  }, [fetchUser]);

  // -------------------- Login --------------------
  const login = async (credentials: LoginCredentials) => {
    setIsLoading(true);
    setError(null);
    try {
      const resp = await AuthEndpoints.login(credentials);

      const tokenFromBody = (resp as any)?.access_token || (resp as any)?.token || (resp as any)?.access;
      if (tokenFromBody) {
        setAuthToken(tokenFromBody);
      }

      // Delay for cookie to set
      await new Promise(resolve => setTimeout(resolve, 500));

      await fetchUser();

      // Get redirect param from URL (e.g., ?redirect=%2Fdashboard)
      const redirectPath = searchParams.get('redirect') || '/dashboard';

      router.push(redirectPath);
      router.refresh();
    } catch (err: any) {
      setError(err?.message || 'Login failed');
      console.error('Login error:', err);
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
      console.warn('Logout request failed:', err);
    } finally {
      removeAuthToken();
      setUser(null);
      setIsLoading(false);
      router.push('/login');
    }
  };

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