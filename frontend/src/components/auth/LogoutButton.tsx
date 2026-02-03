// frontend/src/components/auth/LogoutButton.tsx
'use client';

import React from 'react';
import { useAuth } from '@/hooks/useAuth';

const LogoutButton: React.FC = () => {
  const { logout, isLoading } = useAuth();

  return (
    <button
      onClick={logout}
      disabled={isLoading}
      className="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
    >
      Logout
    </button>
  );
};

export default LogoutButton;
