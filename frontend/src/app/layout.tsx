// // frontend/src/app/layout.tsx
// import './globals.css';
// import { Inter } from 'next/font/google';
// import Navbar from '@/components/common/Navbar';
// import { AuthProvider } from '@/hooks/useAuth';

// const inter = Inter({ subsets: ['latin'] });

// export const metadata = {
//   title: 'Todo App',
//   description: 'A simple todo application',
// };

// export default function RootLayout({ children }: { children: React.ReactNode }) {
//   return (
//     <html lang="en">
//       <body className={inter.className}>
//         <AuthProvider>
//           <Navbar />
//           <main className="container mx-auto p-4">{children}</main>
//         </AuthProvider>
//       </body>
//     </html>
//   );
// }


import './globals.css';
import { Inter } from 'next/font/google';
import Navbar from '@/components/common/Navbar';
import { AuthProvider } from '@/hooks/useAuth';

const inter = Inter({ subsets: ['latin'] });

export const metadata = {
  title: 'Todo App',
  description: 'Todo application',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <AuthProvider>
          <Navbar />
          <main className="container mx-auto p-4">{children}</main>
        </AuthProvider>
      </body>
    </html>
  );
}