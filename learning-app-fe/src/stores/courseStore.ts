import { create } from 'zustand';
import { Course, Chapter } from '@/types';
import { courseService } from '@/services/courseService';
import toast from 'react-hot-toast';

interface CourseState {
  courses: Course[];
  currentCourse: Course | null;
  chapters: Chapter[];
  currentChapter: Chapter | null;
  isLoading: boolean;
  
  // Actions
  fetchCourses: (params?: { skip?: number; limit?: number; owner?: string }) => Promise<void>;
  fetchCourse: (courseId: string) => Promise<void>;
  createCourse: (courseData: any) => Promise<Course>;
  createCourseFromPrompt: (topic: string, level: string) => Promise<Course>;
  updateCourse: (courseId: string, courseData: any) => Promise<void>;
  deleteCourse: (courseId: string) => Promise<void>;
  
  // Chapter actions
  fetchChapters: (courseId: string) => Promise<void>;
  fetchChapter: (courseId: string, chapterId: string) => Promise<void>;
  createChapter: (courseId: string, chapterData: any) => Promise<Chapter>;
  updateChapter: (courseId: string, chapterId: string, chapterData: any) => Promise<void>;
  deleteChapter: (courseId: string, chapterId: string) => Promise<void>;
  
  // AI actions
  generateOutline: (courseId: string, topic: string, level: string) => Promise<string>;
  chatWithCourse: (courseId: string, message: string, mode: 'strict' | 'hybrid') => Promise<string>;
}

export const useCourseStore = create<CourseState>((set, get) => ({
  courses: [],
  currentCourse: null,
  chapters: [],
  currentChapter: null,
  isLoading: false,

  fetchCourses: async (params) => {
    try {
      set({ isLoading: true });
      const courses = await courseService.getCourses(params);
      set({ courses });
    } catch (error) {
      console.error('Failed to fetch courses:', error);
    } finally {
      set({ isLoading: false });
    }
  },

  fetchCourse: async (courseId: string) => {
    try {
      set({ isLoading: true });
      const course = await courseService.getCourse(courseId);
      set({ currentCourse: course });
    } catch (error) {
      console.error('Failed to fetch course:', error);
    } finally {
      set({ isLoading: false });
    }
  },

  createCourse: async (courseData) => {
    try {
      const course = await courseService.createCourse(courseData);
      set(state => ({ courses: [course, ...state.courses] }));
      toast.success('Course created successfully!');
      return course;
    } catch (error) {
      throw error;
    }
  },

  createCourseFromPrompt: async (topic: string, level: string) => {
    try {
      const course = await courseService.createCourseFromPrompt({ topic, level });
      set(state => ({ courses: [course, ...state.courses] }));
      toast.success('AI course generated successfully!');
      return course;
    } catch (error) {
      throw error;
    }
  },

  updateCourse: async (courseId: string, courseData) => {
    try {
      const updatedCourse = await courseService.updateCourse(courseId, courseData);
      set(state => ({
        courses: state.courses.map(c => c.id === courseId ? updatedCourse : c),
        currentCourse: state.currentCourse?.id === courseId ? updatedCourse : state.currentCourse
      }));
      toast.success('Course updated successfully!');
    } catch (error) {
      throw error;
    }
  },

  deleteCourse: async (courseId: string) => {
    try {
      await courseService.deleteCourse(courseId);
      set(state => ({
        courses: state.courses.filter(c => c.id !== courseId),
        currentCourse: state.currentCourse?.id === courseId ? null : state.currentCourse
      }));
      toast.success('Course deleted successfully!');
    } catch (error) {
      throw error;
    }
  },

  fetchChapters: async (courseId: string) => {
    try {
      const chapters = await courseService.getChapters(courseId);
      set({ chapters });
    } catch (error) {
      console.error('Failed to fetch chapters:', error);
    }
  },

  fetchChapter: async (courseId: string, chapterId: string) => {
    try {
      const chapter = await courseService.getChapter(courseId, chapterId);
      set({ currentChapter: chapter });
    } catch (error) {
      console.error('Failed to fetch chapter:', error);
    }
  },

  createChapter: async (courseId: string, chapterData) => {
    try {
      const chapter = await courseService.createChapter(courseId, chapterData);
      set(state => ({ chapters: [...state.chapters, chapter] }));
      toast.success('Chapter created successfully!');
      return chapter;
    } catch (error) {
      throw error;
    }
  },

  updateChapter: async (courseId: string, chapterId: string, chapterData) => {
    try {
      const updatedChapter = await courseService.updateChapter(courseId, chapterId, chapterData);
      set(state => ({
        chapters: state.chapters.map(c => c.id === chapterId ? updatedChapter : c),
        currentChapter: state.currentChapter?.id === chapterId ? updatedChapter : state.currentChapter
      }));
      toast.success('Chapter updated successfully!');
    } catch (error) {
      throw error;
    }
  },

  deleteChapter: async (courseId: string, chapterId: string) => {
    try {
      await courseService.deleteChapter(courseId, chapterId);
      set(state => ({
        chapters: state.chapters.filter(c => c.id !== chapterId),
        currentChapter: state.currentChapter?.id === chapterId ? null : state.currentChapter
      }));
      toast.success('Chapter deleted successfully!');
    } catch (error) {
      throw error;
    }
  },

  generateOutline: async (courseId: string, topic: string, level: string) => {
    try {
      const result = await courseService.generateOutline(courseId, { topic, level });
      return result.outline;
    } catch (error) {
      throw error;
    }
  },

  chatWithCourse: async (courseId: string, message: string, mode: 'strict' | 'hybrid') => {
    try {
      const result = await courseService.chatWithCourse(courseId, { message, mode });
      return result.answer;
    } catch (error) {
      throw error;
    }
  },
}));
