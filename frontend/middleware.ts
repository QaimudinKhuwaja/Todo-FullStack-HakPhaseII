// // frontend/middleware.ts
// import { NextResponse } from 'next/server';
// import type { NextRequest } from 'next/server';
// import Cookies from 'js-cookie'; // js-cookie can be used on the server-side as well

// export function middleware(request: NextRequest) {
//   const token = request.cookies.get('authToken'); // Get token from cookies

//   const protectedPaths = ['/dashboard', '/tasks'];
//   const isProtectedPath = protectedPaths.some(path => request.nextUrl.pathname.startsWith(path));

//   if (isProtectedPath && !token) {
//     // Redirect to login if trying to access protected path without a token
//     const loginUrl = new URL('/auth/login', request.url);
//     loginUrl.searchParams.set('redirect', request.nextUrl.pathname);
//     return NextResponse.redirect(loginUrl);
//   }

//   if ((request.nextUrl.pathname.startsWith('/auth/login') || request.nextUrl.pathname.startsWith('/auth/register')) && token) {
//     // If authenticated, redirect from login/register pages to dashboard
//     return NextResponse.redirect(new URL('/dashboard', request.url));
//   }

//   return NextResponse.next();
// }

// export const config = {
//   matcher: ['/dashboard/:path*', '/tasks/:path*', '/auth/login', '/auth/register'],
// };







// middleware.ts
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
  // Cookie name backend ke mutabiq hai
  const token = request.cookies.get('access_token')?.value;

  // Protected routes (jo login ke baad dikhne chahiye)
  const protectedPaths = ['/dashboard', '/tasks'];
  const isProtectedPath = protectedPaths.some(path =>
    request.nextUrl.pathname.startsWith(path)
  );

  // Agar protected page pe hai aur token nahi → login pe bhejo
  if (isProtectedPath && !token) {
    const loginUrl = new URL('/login', request.url); // ← '/auth/login' nahi, sirf '/login'
    loginUrl.searchParams.set('redirect', request.nextUrl.pathname);
    return NextResponse.redirect(loginUrl);
  }

  // Agar login ya register page pe hai aur token HAI → dashboard pe bhejo
  const authPaths = ['/login', '/register'];
  const isAuthPath = authPaths.some(path =>
    request.nextUrl.pathname === path || request.nextUrl.pathname.startsWith(path + '/')
  );

  if (isAuthPath && token) {
    return NextResponse.redirect(new URL('/dashboard', request.url));
  }

  // Baaki sab cases mein normal flow
  return NextResponse.next();
}

export const config = {
  matcher: [
    '/dashboard/:path*',
    '/tasks/:path*',
    '/login',
    '/register',
  ],
};