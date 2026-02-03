// frontend/src/components/common/Navbar.tsx
'use client';

import React from 'react';
import Link from 'next/link';
import { useAuth } from '@/hooks/useAuth';
import LogoutButton from '@/components/auth/LogoutButton';

const Navbar: React.FC = () => {
  const { user, isLoading } = useAuth();

  return (
    <nav className="bg-gray-800 p-4">
      <div className="container mx-auto flex justify-between items-center">
        <Link href="/" className="text-white text-lg font-bold">
          TodoApp
        </Link>
        <div className="flex items-center">
          {!isLoading && user ? (
            <>
              <span className="text-gray-300 mr-4">Welcome, {user.username}!</span>
              <Link href="/dashboard" className="text-gray-300 hover:text-white mr-4">
                Dashboard
              </Link>
              <LogoutButton />
            </>
          ) : (
            <>
              <Link href="/login" className="text-gray-300 hover:text-white mr-4">
                Login
              </Link>
              <Link href="/register" className="text-gray-300 hover:text-white">
                Register
              </Link>
            </>
          )}
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
