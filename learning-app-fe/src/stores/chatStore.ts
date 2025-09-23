import { create } from 'zustand';
import { ChatSession, ChatMessage } from '@/types';
import { chatService } from '@/services/chatService';
import toast from 'react-hot-toast';

interface ChatState {
  sessions: ChatSession[];
  currentSession: ChatSession | null;
  messages: ChatMessage[];
  isLoading: boolean;
  isSendingMessage: boolean;
  
  // Actions
  fetchSessions: () => Promise<void>;
  createSession: (data: { course_id?: string; upload_id?: string; title: string; mode: 'strict' | 'hybrid' }) => Promise<ChatSession>;
  selectSession: (sessionId: string) => Promise<void>;
  deleteSession: (sessionId: string) => Promise<void>;
  
  // Message actions
  fetchMessages: (sessionId: string) => Promise<void>;
  sendMessage: (sessionId: string, message: string) => Promise<void>;
  freestyleChat: (message: string, mode: 'strict' | 'hybrid') => Promise<string>;
  
  // Utility actions
  saveSessionAsCourse: (sessionId: string, title: string, description: string) => Promise<string>;
  clearCurrentSession: () => void;
}

export const useChatStore = create<ChatState>((set, get) => ({
  sessions: [],
  currentSession: null,
  messages: [],
  isLoading: false,
  isSendingMessage: false,

  fetchSessions: async () => {
    try {
      set({ isLoading: true });
      const sessions = await chatService.getSessions();
      set({ sessions });
    } catch (error) {
      console.error('Failed to fetch chat sessions:', error);
    } finally {
      set({ isLoading: false });
    }
  },

  createSession: async (data) => {
    try {
      const session = await chatService.createSession(data);
      set(state => ({ 
        sessions: [session, ...state.sessions],
        currentSession: session,
        messages: []
      }));
      toast.success('Chat session created!');
      return session;
    } catch (error) {
      throw error;
    }
  },

  selectSession: async (sessionId: string) => {
    try {
      set({ isLoading: true });
      const session = await chatService.getSession(sessionId);
      const messages = await chatService.getMessages(sessionId);
      set({ 
        currentSession: session,
        messages: messages.reverse() // Show oldest first
      });
    } catch (error) {
      console.error('Failed to select session:', error);
    } finally {
      set({ isLoading: false });
    }
  },

  deleteSession: async (sessionId: string) => {
    try {
      await chatService.deleteSession(sessionId);
      set(state => ({
        sessions: state.sessions.filter(s => s.id !== sessionId),
        currentSession: state.currentSession?.id === sessionId ? null : state.currentSession,
        messages: state.currentSession?.id === sessionId ? [] : state.messages
      }));
      toast.success('Chat session deleted!');
    } catch (error) {
      throw error;
    }
  },

  fetchMessages: async (sessionId: string) => {
    try {
      const messages = await chatService.getMessages(sessionId);
      set({ messages: messages.reverse() });
    } catch (error) {
      console.error('Failed to fetch messages:', error);
    }
  },

  sendMessage: async (sessionId: string, message: string) => {
    try {
      set({ isSendingMessage: true });
      
      // Add user message immediately
      const userMessage: ChatMessage = {
        id: Date.now().toString(),
        session_id: sessionId,
        sender: 'user',
        message,
        created_at: new Date().toISOString()
      };
      
      set(state => ({ messages: [...state.messages, userMessage] }));
      
      // Send message and get AI response
      const response = await chatService.sendMessage(sessionId, message);
      
      // Add AI response
      const aiMessage: ChatMessage = {
        id: (Date.now() + 1).toString(),
        session_id: sessionId,
        sender: 'ai',
        message: response.answer,
        created_at: new Date().toISOString()
      };
      
      set(state => ({ messages: [...state.messages, aiMessage] }));
    } catch (error) {
      // Remove user message on error
      set(state => ({ 
        messages: state.messages.slice(0, -1)
      }));
      throw error;
    } finally {
      set({ isSendingMessage: false });
    }
  },

  freestyleChat: async (message: string, mode: 'strict' | 'hybrid') => {
    try {
      const response = await chatService.freestyleChat({ message, mode });
      return response.answer;
    } catch (error) {
      throw error;
    }
  },

  saveSessionAsCourse: async (sessionId: string, title: string, description: string) => {
    try {
      const result = await chatService.saveAsCourse(sessionId, { title, description });
      toast.success('Chat saved as course successfully!');
      return result.course_id;
    } catch (error) {
      throw error;
    }
  },

  clearCurrentSession: () => {
    set({ currentSession: null, messages: [] });
  },
}));
