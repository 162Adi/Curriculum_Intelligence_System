import { create } from 'zustand';
import { User, Role } from '../types';
import { api } from '../services/api';

interface AuthState {
  user: User | null;
  token: string | null;
  isLoading: boolean;
  error: string | null;
  login: (credentials: { email?: string; username?: string; password?: string } | FormData) => Promise<void>;
  logout: () => void;
  loadUser: () => Promise<void>;
  hasRole: (roles: Role[]) => boolean;
}

export const useAuthStore = create<AuthState>((set, get) => ({
  user: JSON.parse(localStorage.getItem('cis_user') || 'null'),
  token: localStorage.getItem('cis_access_token'),
  isLoading: false,
  error: null,

  login: async (credentials: any) => {
    set({ isLoading: true, error: null });
    try {
      const data = await api.login(credentials);
      localStorage.setItem('cis_access_token', data.access_token);
      let currentUser = data.user;
      if (!currentUser) {
        currentUser = await api.getMe();
      }
      localStorage.setItem('cis_user', JSON.stringify(currentUser));
      set({ user: currentUser, token: data.access_token, isLoading: false });
    } catch (err: any) {
      set({ error: err.message || 'Login failed', isLoading: false });
      throw err;
    }
  },

  logout: () => {
    localStorage.removeItem('cis_access_token');
    localStorage.removeItem('cis_user');
    set({ user: null, token: null });
    window.location.href = '/login';
  },

  loadUser: async () => {
    const token = localStorage.getItem('cis_access_token');
    if (!token) return;
    try {
      const user = await api.getMe();
      localStorage.setItem('cis_user', JSON.stringify(user));
      set({ user });
    } catch {
      get().logout();
    }
  },

  hasRole: (roles: Role[]) => {
    const user = get().user;
    if (!user) return false;
    return roles.includes(user.role);
  },
}));
