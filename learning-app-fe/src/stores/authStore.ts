import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { User } from '@/types';
import { authService } from '@/services/authService';
import toast from 'react-hot-toast';

interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  
  // Actions
  login: (email: string, password: string) => Promise<void>;
  register: (name: string, email: string, password: string) => Promise<void>;
  logout: () => void;
  refreshToken: () => Promise<void>;
  getCurrentUser: () => Promise<void>;
  updateProfile: (userData: Partial<User>) => Promise<void>;
  changePassword: (currentPassword: string, newPassword: string) => Promise<void>;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      user: null,
      token: null,
      isAuthenticated: false,
      isLoading: false,

      login: async (email: string, password: string) => {
        try {
          set({ isLoading: true });
          const tokenData = await authService.login({ email, password });
          set({ 
            token: tokenData.access_token, 
            isAuthenticated: true 
          });
          
          // Get user data after successful login
          await get().getCurrentUser();
          toast.success('Logged in successfully!');
        } catch (error) {
          set({ user: null, token: null, isAuthenticated: false });
          throw error;
        } finally {
          set({ isLoading: false });
        }
      },

      register: async (name: string, email: string, password: string) => {
        try {
          set({ isLoading: true });
          const user = await authService.register({ name, email, password });
          
          // Auto login after registration
          await get().login(email, password);
          toast.success('Account created successfully!');
        } catch (error) {
          throw error;
        } finally {
          set({ isLoading: false });
        }
      },

      logout: () => {
        set({ 
          user: null, 
          token: null, 
          isAuthenticated: false 
        });
        toast.success('Logged out successfully!');
      },

      refreshToken: async () => {
        try {
          const tokenData = await authService.refreshToken();
          set({ token: tokenData.access_token });
        } catch (error) {
          get().logout();
          throw error;
        }
      },

      getCurrentUser: async () => {
        try {
          const user = await authService.getCurrentUser();
          set({ user });
        } catch (error) {
          get().logout();
          throw error;
        }
      },

      updateProfile: async (userData: Partial<User>) => {
        try {
          const updatedUser = await authService.updateProfile(userData);
          set({ user: updatedUser });
          toast.success('Profile updated successfully!');
        } catch (error) {
          throw error;
        }
      },

      changePassword: async (currentPassword: string, newPassword: string) => {
        try {
          await authService.changePassword({
            current_password: currentPassword,
            new_password: newPassword,
          });
          toast.success('Password changed successfully!');
        } catch (error) {
          throw error;
        }
      },
    }),
    {
      name: 'auth-storage',
      partialize: (state) => ({
        user: state.user,
        token: state.token,
        isAuthenticated: state.isAuthenticated,
      }),
    }
  )
);
