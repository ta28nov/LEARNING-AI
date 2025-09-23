import { create } from 'zustand';
import { Quiz, QuizQuestion, QuizAnswer, QuizHistory } from '@/types';
import { quizService } from '@/services/quizService';
import toast from 'react-hot-toast';

interface QuizState {
  quizzes: Quiz[];
  currentQuiz: Quiz | null;
  questions: QuizQuestion[];
  currentQuestionIndex: number;
  userAnswers: QuizAnswer[];
  quizHistory: QuizHistory[];
  currentResult: QuizHistory | null;
  isLoading: boolean;
  isSubmitting: boolean;
  
  // Actions
  createQuiz: (data: { title: string; prompt: string; course_id?: string }) => Promise<Quiz>;
  generateQuiz: (data: { type: 'course' | 'upload'; id: string; title: string; num_questions: number }) => Promise<Quiz>;
  startQuiz: (quizId: string) => Promise<void>;
  
  // Question navigation
  nextQuestion: () => void;
  previousQuestion: () => void;
  goToQuestion: (index: number) => void;
  
  // Answer management
  setAnswer: (questionId: string, answer: number) => void;
  submitQuiz: () => Promise<QuizHistory>;
  
  // History
  fetchQuizHistory: () => Promise<void>;
  getQuizResult: (historyId: string) => Promise<void>;
  
  // Reset
  resetQuiz: () => void;
}

export const useQuizStore = create<QuizState>((set, get) => ({
  quizzes: [],
  currentQuiz: null,
  questions: [],
  currentQuestionIndex: 0,
  userAnswers: [],
  quizHistory: [],
  currentResult: null,
  isLoading: false,
  isSubmitting: false,

  createQuiz: async (data) => {
    try {
      const quiz = await quizService.createQuiz(data);
      set(state => ({ quizzes: [quiz, ...state.quizzes] }));
      toast.success('Quiz created successfully!');
      return quiz;
    } catch (error) {
      throw error;
    }
  },

  generateQuiz: async (data) => {
    try {
      set({ isLoading: true });
      const quiz = await quizService.generateQuiz(data);
      set(state => ({ quizzes: [quiz, ...state.quizzes] }));
      toast.success('Quiz generated successfully!');
      return quiz;
    } catch (error) {
      throw error;
    } finally {
      set({ isLoading: false });
    }
  },

  startQuiz: async (quizId: string) => {
    try {
      set({ isLoading: true });
      const [quiz, questions] = await Promise.all([
        quizService.getQuiz(quizId),
        quizService.getQuizQuestions(quizId)
      ]);
      
      set({
        currentQuiz: quiz,
        questions: questions.sort((a, b) => a.order - b.order),
        currentQuestionIndex: 0,
        userAnswers: [],
        currentResult: null
      });
    } catch (error) {
      console.error('Failed to start quiz:', error);
    } finally {
      set({ isLoading: false });
    }
  },

  nextQuestion: () => {
    set(state => ({
      currentQuestionIndex: Math.min(state.currentQuestionIndex + 1, state.questions.length - 1)
    }));
  },

  previousQuestion: () => {
    set(state => ({
      currentQuestionIndex: Math.max(state.currentQuestionIndex - 1, 0)
    }));
  },

  goToQuestion: (index: number) => {
    set(state => ({
      currentQuestionIndex: Math.max(0, Math.min(index, state.questions.length - 1))
    }));
  },

  setAnswer: (questionId: string, answer: number) => {
    set(state => {
      const existingAnswerIndex = state.userAnswers.findIndex(a => a.question_id === questionId);
      const newAnswer: QuizAnswer = { question_id: questionId, answer };
      
      if (existingAnswerIndex >= 0) {
        const updatedAnswers = [...state.userAnswers];
        updatedAnswers[existingAnswerIndex] = newAnswer;
        return { userAnswers: updatedAnswers };
      } else {
        return { userAnswers: [...state.userAnswers, newAnswer] };
      }
    });
  },

  submitQuiz: async () => {
    try {
      const { currentQuiz, userAnswers } = get();
      if (!currentQuiz) throw new Error('No quiz selected');
      
      set({ isSubmitting: true });
      const result = await quizService.submitQuiz(currentQuiz.id, userAnswers);
      
      set({ 
        currentResult: result,
        quizHistory: [result, ...get().quizHistory]
      });
      
      toast.success(`Quiz completed! Score: ${result.score}%`);
      return result;
    } catch (error) {
      throw error;
    } finally {
      set({ isSubmitting: false });
    }
  },

  fetchQuizHistory: async () => {
    try {
      const history = await quizService.getQuizHistory();
      set({ quizHistory: history });
    } catch (error) {
      console.error('Failed to fetch quiz history:', error);
    }
  },

  getQuizResult: async (historyId: string) => {
    try {
      const result = await quizService.getQuizHistoryDetail(historyId);
      set({ currentResult: result });
    } catch (error) {
      console.error('Failed to fetch quiz result:', error);
    }
  },

  resetQuiz: () => {
    set({
      currentQuiz: null,
      questions: [],
      currentQuestionIndex: 0,
      userAnswers: [],
      currentResult: null
    });
  },
}));
