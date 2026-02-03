// frontend/src/app/page.tsx
import Link from 'next/link';
import React from 'react';

const HomePage: React.FC = () => {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100 p-4">
      <h1 className="text-6xl font-bold text-blue-600 mb-4 ">Welcome to TodoApp!</h1>
      <p className="text-lg text-gray-600 mb-8 text-center">
        Your personal task manager to keep track of everything you need to do.
      </p>
      <div className="flex space-x-4">
        <Link href="/register" className="px-6 py-3 bg-blue-600 text-white rounded-lg shadow-md hover:bg-blue-700 transition duration-300">
          Get Started
        </Link>
        <Link href="/login" className="px-6 py-3 bg-gray-300 text-gray-800 rounded-lg shadow-md hover:bg-gray-400 transition duration-300">
          Login
        </Link>
      </div>
    </div>
  );
};

export default HomePage;
