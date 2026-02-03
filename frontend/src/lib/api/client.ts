// // frontend/src/lib/api/client.ts
// import { getAuthToken } from '@/lib/auth/token';


// const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL;

// interface RequestOptions extends RequestInit {
//   token?: string;
// }

// export async function apiRequest<T>(
//   method: string,
//   path: string,
//   data?: any,
//   options?: RequestOptions
// ): Promise<T> {
//   const token = options?.token || getAuthToken();
//   const headers: HeadersInit = {
//     'Content-Type': 'application/json',
//   };

//   if (token) {
//     headers['Authorization'] = `Bearer ${token}`;
//   }

//   const config: RequestInit = {
//     method,
//     headers,
//     ...options,
//   };

//   if (data) {
//     config.body = JSON.stringify(data);
//   }

//   const response = await fetch(`${API_BASE_URL}${path}`, config);

//   if (response.status === 401) {
//     // Handle unauthorized globally, e.g., redirect to login
//     window.location.href = '/login';
//     throw new Error('Unauthorized');
//   }

//   if (!response.ok) {
//     let errorData: any;
//     let errorMessage = 'Something went wrong';

//     try {
//       errorData = await response.json();
//       if (errorData) {
//         if (typeof errorData === 'string') {
//           errorMessage = errorData;
//         } else if (errorData.detail) {
//           errorMessage = errorData.detail;
//         } else if (errorData.message) {
//           errorMessage = errorData.message;
//         } else {
//           // If errorData is an object but doesn't have a 'detail' or 'message' field, stringify it
//           errorMessage = JSON.stringify(errorData);
//         }
//       }
//     } catch (e) {
//       // If response is not JSON, try to get text or fall back to generic message
//       try {
//         errorMessage = await response.text();
//         if (!errorMessage) {
//           errorMessage = `Server error: ${response.status} ${response.statusText}`;
//         }
//       } catch (textError) {
//         errorMessage = `Network error or server responded with status ${response.status}`;
//       }
//     }
//     throw new ApiError(errorMessage, response);
//   }

//   // Handle cases where response might be empty (e.g., 204 No Content)
//   if (response.status === 204) {
//     return null as T;
//   }

//   return response.json();
// }

// export class ApiError extends Error {
//   response?: Response;
//   status: number;
//   constructor(message: string, response?: Response) {
//     super(message);
//     this.response = response;
//     this.status = response ? response.status : 0;
//     Object.setPrototypeOf(this, ApiError.prototype);
//   }
// }

// export const api = {
//   get: <T>(path: string, options?: RequestOptions) => apiRequest<T>('GET', path, undefined, options),
//   post: <T>(path: string, data: any, options?: RequestOptions) =>
//     apiRequest<T>('POST', path, data, options),
//   patch: <T>(path: string, data: any, options?: RequestOptions) =>
//     apiRequest<T>('PATCH', path, data, options),
//   delete: <T>(path: string, options?: RequestOptions) =>
//     apiRequest<T>('DELETE', path, undefined, options),
// };





//lib/api/client.ts
const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL;

interface RequestOptions extends RequestInit {}

export async function apiRequest<T>(
  method: string,
  path: string,
  data?: any,
  options?: RequestOptions
): Promise<T> {
  const headers: HeadersInit = {
    'Content-Type': 'application/json',
  };

  const config: RequestInit = {
    method,
    headers,
    credentials: 'include', // ✅ important for cookie-based auth
    ...options,
  };

  if (data) {
    config.body = JSON.stringify(data);
  }

  const response = await fetch(`${API_BASE_URL}${path}`, config);

  // -----------------------
  // ✅ Handle Unauthorized
  // -----------------------
  if (response.status === 401) {
    // Only redirect if not already on login page
    if (window.location.pathname !== '/login') {
      window.location.href = '/login';
    }
    throw new Error('Unauthorized - please login again');
  }

  // -----------------------
  // Handle other errors
  // -----------------------
  if (!response.ok) {
    let errorMessage = 'Something went wrong';

    try {
      const errorData = await response.json();

      if (typeof errorData === 'string') {
        errorMessage = errorData;
      } else if (errorData?.detail) {
        errorMessage = errorData.detail;
      } else if (errorData?.message) {
        errorMessage = errorData.message;
      } else {
        errorMessage = JSON.stringify(errorData);
      }
    } catch {
      try {
        errorMessage = await response.text();
      } catch {
        errorMessage = `Server error: ${response.status}`;
      }
    }

    throw new ApiError(errorMessage, response);
  }

  if (response.status === 204) {
    return null as T;
  }

  return response.json();
}

export class ApiError extends Error {
  response?: Response;
  status: number;

  constructor(message: string, response?: Response) {
    super(message);
    this.response = response;
    this.status = response ? response.status : 0;
    Object.setPrototypeOf(this, ApiError.prototype);
  }
}

// -----------------------
// API helpers
// -----------------------
export const api = {
  get: <T>(path: string, options?: RequestOptions) =>
    apiRequest<T>('GET', path, undefined, options),

  post: <T>(path: string, data: any, options?: RequestOptions) =>
    apiRequest<T>('POST', path, data, options),

  patch: <T>(path: string, data: any, options?: RequestOptions) =>
    apiRequest<T>('PATCH', path, data, options),

  delete: <T>(path: string, options?: RequestOptions) =>
    apiRequest<T>('DELETE', path, undefined, options),
};
