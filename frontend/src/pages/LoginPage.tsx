import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Shield, Sparkles, BookOpen, KeyRound, ArrowRight } from 'lucide-react';
import { useAuthStore } from '../stores/authStore';

export const LoginPage: React.FC = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [errorMsg, setErrorMsg] = useState('');
  const { login, isLoading } = useAuthStore();
  const navigate = useNavigate();

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrorMsg('');
    try {
      await login({ email: email.trim(), password });
      navigate('/dashboard');
    } catch (err: any) {
      setErrorMsg(err.message || 'Invalid email or password');
    }
  };

  const handleQuickLogin = async (uEmail: string, uPass: string) => {
    setEmail(uEmail);
    setPassword(uPass);
    setErrorMsg('');
    try {
      await login({ email: uEmail.trim(), password: uPass });
      navigate('/dashboard');
    } catch (err: any) {
      setErrorMsg(err.message || 'Login failed');
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 flex flex-col justify-center items-center p-4">
      {/* Background radial glow */}
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_top,_var(--tw-gradient-stops))] from-blue-900/20 via-slate-950 to-slate-950 pointer-events-none" />

      <div className="relative w-full max-w-md bg-slate-900/90 border border-slate-800 rounded-2xl shadow-2xl p-8 backdrop-blur-xl">
        {/* Header */}
        <div className="text-center mb-6">
          <div className="inline-flex items-center justify-center w-12 h-12 rounded-xl bg-blue-600/20 border border-blue-500/30 text-blue-400 mb-3">
            <BookOpen className="w-6 h-6" />
          </div>
          <h1 className="text-xl font-bold tracking-tight text-white uppercase">
            Curriculum Intelligence System
          </h1>
          <p className="text-xs text-slate-400 mt-1 max-w-sm mx-auto">
            Bridging Academic Learning and Industry Requirements Through Agentic Intelligence.
          </p>
        </div>

        {errorMsg && (
          <div className="mb-4 p-3 rounded-lg bg-rose-500/10 border border-rose-500/30 text-rose-400 text-xs">
            {errorMsg}
          </div>
        )}

        {/* Login Form */}
        <form onSubmit={handleLogin} className="space-y-4">
          <div>
            <label className="block text-xs font-medium text-slate-300 mb-1">University Email</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="e.g. faculty@university.edu"
              required
              className="w-full bg-slate-800/80 border border-slate-700 rounded-lg px-3 py-2 text-xs text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <div>
            <label className="block text-xs font-medium text-slate-300 mb-1">Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••••••"
              required
              className="w-full bg-slate-800/80 border border-slate-700 rounded-lg px-3 py-2 text-xs text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <button
            type="submit"
            disabled={isLoading}
            className="w-full mt-2 py-2.5 px-4 bg-blue-600 hover:bg-blue-500 text-white font-medium rounded-lg text-xs transition-colors flex items-center justify-center gap-2 disabled:opacity-50"
          >
            {isLoading ? (
              <span>Authenticating...</span>
            ) : (
              <>
                <span>Sign In to CIS</span>
                <ArrowRight className="w-4 h-4" />
              </>
            )}
          </button>
        </form>

        {/* Quick Role Fill Presets */}
        <div className="mt-6 pt-5 border-t border-slate-800">
          <p className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider mb-2.5 flex items-center gap-1.5">
            <KeyRound className="w-3.5 h-3.5 text-blue-400" />
            <span>Instant Role Access (University Sandbox)</span>
          </p>
          <div className="grid grid-cols-2 gap-2 text-left">
            <button
              onClick={() => handleQuickLogin('faculty@university.edu', 'Faculty@CIS2026!')}
              className="p-2 rounded-lg bg-slate-800/60 hover:bg-slate-800 border border-slate-700/60 text-left transition-colors"
            >
              <div className="text-[11px] font-semibold text-blue-400">Faculty Member</div>
              <div className="text-[9px] text-slate-400">Upload & Edit Curriculum</div>
            </button>
            <button
              onClick={() => handleQuickLogin('reviewer@university.edu', 'Reviewer@CIS2026!')}
              className="p-2 rounded-lg bg-slate-800/60 hover:bg-slate-800 border border-slate-700/60 text-left transition-colors"
            >
              <div className="text-[11px] font-semibold text-emerald-400">Curriculum Reviewer</div>
              <div className="text-[9px] text-slate-400">Benchmarking & Comments</div>
            </button>
            <button
              onClick={() => handleQuickLogin('management@university.edu', 'Dean@CIS2026!')}
              className="p-2 rounded-lg bg-slate-800/60 hover:bg-slate-800 border border-slate-700/60 text-left transition-colors"
            >
              <div className="text-[11px] font-semibold text-purple-400">Academic Dean</div>
              <div className="text-[9px] text-slate-400">Executive Reports & Signoff</div>
            </button>
            <button
              onClick={() => handleQuickLogin('admin@university.edu', 'Admin@CIS2026!')}
              className="p-2 rounded-lg bg-slate-800/60 hover:bg-slate-800 border border-slate-700/60 text-left transition-colors"
            >
              <div className="text-[11px] font-semibold text-amber-400">System Admin</div>
              <div className="text-[9px] text-slate-400">Full RBAC & Config</div>
            </button>
          </div>
        </div>

        {/* Security badge footer */}
        <div className="mt-4 text-center flex items-center justify-center gap-1.5 text-[10px] text-slate-400">
          <Shield className="w-3 h-3 text-emerald-400" />
          <span>Argon2id Password Hashing & JWT Token Architecture</span>
        </div>
      </div>
    </div>
  );
};
