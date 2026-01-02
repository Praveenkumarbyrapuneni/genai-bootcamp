// src/components/Login.tsx

"use client";

import { supabase } from "@/lib/supabase";
import { useState } from "react";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [isSignUp, setIsSignUp] = useState(false);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");

  const handleEmailAuth = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setMessage("");

    try {
      if (isSignUp) {
        const { error } = await supabase.auth.signUp({ email, password });
        if (error) throw error;
        setMessage("Check your email for the confirmation link!");
      } else {
        const { error } = await supabase.auth.signInWithPassword({ email, password });
        if (error) throw error;
      }
    } catch (error: any) {
      setMessage(error.message);
    } finally {
      setLoading(false);
    }
  };

  const handleGitHubLogin = async () => {
    setLoading(true);
    const { error } = await supabase.auth.signInWithOAuth({
      provider: "github",
      options: {
        redirectTo: window.location.origin,
      },
    });
    if (error) setMessage(error.message);
    setLoading(false);
  };

  const handleGoogleLogin = async () => {
    setLoading(true);
    const { error } = await supabase.auth.signInWithOAuth({
      provider: "google",
      options: {
        redirectTo: window.location.origin,
      },
    });
    if (error) setMessage(error.message);
    setLoading(false);
  };

  // Custom Logo Component
  const Logo = () => (
    <svg width="56" height="56" viewBox="0 0 56 56" fill="none" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <linearGradient id="rocketGradient" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stopColor="#6366F1" />
          <stop offset="50%" stopColor="#8B5CF6" />
          <stop offset="100%" stopColor="#A855F7" />
        </linearGradient>
        <linearGradient id="flameGradient" x1="0%" y1="0%" x2="0%" y2="100%">
          <stop offset="0%" stopColor="#FBBF24" />
          <stop offset="50%" stopColor="#F97316" />
          <stop offset="100%" stopColor="#EF4444" />
        </linearGradient>
        <linearGradient id="windowGradient" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stopColor="#38BDF8" />
          <stop offset="100%" stopColor="#0EA5E9" />
        </linearGradient>
      </defs>
      
      <circle cx="28" cy="28" r="26" fill="url(#rocketGradient)" opacity="0.1"/>
      <path d="M28 8C28 8 38 18 38 30C38 38 34 44 28 46C22 44 18 38 18 30C18 18 28 8 28 8Z" 
            fill="url(#rocketGradient)" />
      <circle cx="28" cy="24" r="6" fill="url(#windowGradient)" />
      <circle cx="28" cy="24" r="4" fill="#1E293B" />
      <circle cx="26" cy="22" r="1.5" fill="#38BDF8" opacity="0.6" />
      <path d="M18 34L12 42L18 40V34Z" fill="url(#rocketGradient)" />
      <path d="M38 34L44 42L38 40V34Z" fill="url(#rocketGradient)" />
      <ellipse cx="28" cy="50" rx="6" ry="4" fill="url(#flameGradient)" />
      <ellipse cx="28" cy="49" rx="4" ry="3" fill="#FBBF24" />
      <ellipse cx="28" cy="48" rx="2" ry="2" fill="#FEF3C7" />
      <circle cx="10" cy="14" r="1" fill="#6366F1" />
      <circle cx="46" cy="18" r="1.5" fill="#8B5CF6" />
      <circle cx="8" cy="32" r="1" fill="#6366F1" />
      <circle cx="48" cy="36" r="1" fill="#8B5CF6" />
    </svg>
  );

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-50 via-white to-indigo-50 relative overflow-hidden">
      {/* Background Effects - Light Version */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute -top-40 -right-40 w-96 h-96 bg-purple-200 rounded-full mix-blend-multiply filter blur-3xl opacity-40 animate-pulse"></div>
        <div className="absolute -bottom-40 -left-40 w-96 h-96 bg-indigo-200 rounded-full mix-blend-multiply filter blur-3xl opacity-40 animate-pulse"></div>
        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-pink-100 rounded-full mix-blend-multiply filter blur-3xl opacity-30"></div>
      </div>

      {/* Login Card */}
      <div className="relative w-full max-w-md p-8 space-y-6 bg-white/80 backdrop-blur-xl rounded-3xl shadow-xl border border-gray-100">
        {/* Logo & Title */}
        <div className="text-center">
          <div className="flex items-center justify-center gap-3 mb-3">
            <Logo />
            <div className="text-left">
              <h1 className="text-3xl font-bold bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 bg-clip-text text-transparent">
                CareerPath AI
              </h1>
              <p className="text-sm text-gray-500">AI-Powered Career Strategist</p>
            </div>
          </div>
        </div>

        {/* OAuth Buttons */}
        <div className="space-y-3 pt-4">
          <button
            onClick={handleGitHubLogin}
            disabled={loading}
            className="w-full flex items-center justify-center gap-3 px-4 py-3.5 bg-gray-900 hover:bg-gray-800 text-white rounded-xl transition-all duration-300 font-medium disabled:opacity-50 hover:shadow-lg hover:shadow-gray-900/20"
          >
            <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
              <path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z" />
            </svg>
            Continue with GitHub
          </button>

          <button
            onClick={handleGoogleLogin}
            disabled={loading}
            className="w-full flex items-center justify-center gap-3 px-4 py-3.5 bg-white hover:bg-gray-50 text-gray-700 rounded-xl transition-all duration-300 font-medium disabled:opacity-50 border border-gray-200 hover:border-indigo-300 hover:shadow-lg hover:shadow-indigo-500/10"
          >
            <svg className="w-5 h-5" viewBox="0 0 24 24">
              <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" />
              <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" />
              <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" />
              <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" />
            </svg>
            Continue with Google
          </button>
        </div>

        {/* Divider */}
        <div className="relative py-2">
          <div className="absolute inset-0 flex items-center">
            <div className="w-full border-t border-gray-200"></div>
          </div>
          <div className="relative flex justify-center text-sm">
            <span className="px-4 bg-white text-gray-400">or continue with email</span>
          </div>
        </div>

        {/* Email Form */}
        <form onSubmit={handleEmailAuth} className="space-y-4">
          <div>
            <input
              type="email"
              placeholder="Email address"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              className="w-full px-4 py-3.5 bg-gray-50 border border-gray-200 rounded-xl text-gray-800 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent focus:bg-white transition-all"
            />
          </div>
          <div>
            <input
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              minLength={6}
              className="w-full px-4 py-3.5 bg-gray-50 border border-gray-200 rounded-xl text-gray-800 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent focus:bg-white transition-all"
            />
          </div>
          <button
            type="submit"
            disabled={loading}
            className="w-full py-3.5 bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 hover:from-indigo-500 hover:via-purple-500 hover:to-pink-500 text-white font-semibold rounded-xl transition-all duration-300 disabled:opacity-50 shadow-lg shadow-indigo-500/30 hover:shadow-indigo-500/50"
          >
            {loading ? (
              <span className="flex items-center justify-center gap-2">
                <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                </svg>
                Loading...
              </span>
            ) : isSignUp ? "Create Account" : "Sign In"}
          </button>
        </form>

        {/* Message */}
        {message && (
          <div className={`p-3 rounded-lg text-center text-sm ${message.includes("Check") ? "bg-green-50 text-green-600 border border-green-200" : "bg-red-50 text-red-600 border border-red-200"}`}>
            {message}
          </div>
        )}

        {/* Toggle Sign Up / Sign In */}
        <p className="text-center text-gray-500 text-sm pt-2">
          {isSignUp ? "Already have an account?" : "Don't have an account?"}{" "}
          <button
            onClick={() => setIsSignUp(!isSignUp)}
            className="text-indigo-600 hover:text-indigo-500 font-semibold transition-colors"
          >
            {isSignUp ? "Sign In" : "Sign Up"}
          </button>
        </p>

        {/* Footer */}
        <div className="pt-4 border-t border-gray-100">
          <p className="text-center text-gray-400 text-xs">
            🔒 Secured with Supabase Authentication
          </p>
        </div>
      </div>
    </div>
  );
}
