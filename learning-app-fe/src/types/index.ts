// User types
export interface User {
  id: string;
  email: string;
  name: string;
  avatar?: string;
  role: 'student' | 'instructor' | 'admin';
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface AuthTokens {
  access_token: string;
  token_type: string;
}

// Course types
export interface Course {
  id: string;
  owner_id: string;
  title: string;
  description: string;
  outline?: string;
  source?: string;
  level: 'beginner' | 'intermediate' | 'advanced';
  tags: string[];
  visibility?: 'PUBLIC' | 'PRIVATE' | 'DRAFT';
  enrollment_count?: number;
  created_at: string;
  updated_at: string;
}

export interface Chapter {
  id: string;
  course_id: string;
  title: string;
  content: string;
  order: number;
  created_at: string;
  updated_at: string;
}

// Enrollment types
export type EnrollmentStatus = 'active' | 'completed' | 'dropped';

export interface CourseEnrollment {
  id: string;
  student_id: string;
  course_id: string;
  status: EnrollmentStatus;
  progress: number;
  enrolled_at: string;
  last_accessed?: string;
  completed_at?: string;
}

// Alias for backend response compatibility
export type CourseEnrollmentResponse = CourseEnrollment;

export interface EnrolledCourseInfo {
  course_id: string;
  title: string;
  description: string;
  level: 'beginner' | 'intermediate' | 'advanced';
  enrollment_status: EnrollmentStatus;
  progress: number;
  enrolled_at: string;
  last_accessed?: string;
}

export interface ChapterProgress {
  id: string;
  user_id: string;
  course_id: string;
  chapter_id: string;
  status: 'not_started' | 'in_progress' | 'completed';
  progress: number;
  time_spent: number;
  last_position?: number;
  created_at: string;
  updated_at: string;
}

export interface StudentDashboardResponse {
  total_enrolled_courses: number;
  completed_courses: number;
  in_progress_courses: number;
  total_time_spent: number;
  average_progress: number;
  recent_courses: EnrolledCourseInfo[];
}

export interface CourseAnalytics {
  course_id: string;
  title: string;
  total_enrollments: number;
  active_students: number;
  completed_students: number;
  average_progress: number;
  average_time_spent: number;
  completion_rate: number;
}

export interface InstructorDashboardResponse {
  total_courses: number;
  total_students: number;
  total_enrollments: number;
  average_course_rating: number;
  recent_analytics: CourseAnalytics[];
}

export interface StudentEnrollmentInfo {
  student_id: string;
  student_name: string;
  student_email: string;
  enrolled_at: string;
  progress: number;
  status: EnrollmentStatus;
  last_accessed?: string;
}

// Upload types
export interface Upload {
  id: string;
  user_id: string;
  filename: string;
  file_type: 'pdf' | 'docx' | 'txt' | 'video' | 'image';
  file_path: string;
  file_size: number;
  status: 'pending' | 'processing' | 'completed' | 'failed';
  extracted_text?: string;
  metadata?: Record<string, any>;
  created_at: string;
}

// Quiz types
export interface Quiz {
  id: string;
  course_id?: string;
  chapter_id?: string;
  title: string;
  prompt: string;
  created_at: string;
}

export interface QuizQuestion {
  id: string;
  quiz_id: string;
  question: string;
  options: string[];
  correct_answer: number;
  explanation?: string;
  order: number;
}

export interface QuizAnswer {
  question_id: string;
  answer: number;
}

export interface QuizHistory {
  id: string;
  quiz_id: string;
  user_id: string;
  score: number;
  total_questions: number;
  correct_answers: number;
  answers: Array<{
    question_id: string;
    question: string;
    user_answer: number;
    correct_answer: number;
    is_correct: boolean;
    explanation?: string;
  }>;
  taken_at: string;
}

// Chat types
export interface ChatSession {
  id: string;
  user_id: string;
  course_id?: string;
  upload_id?: string;
  title: string;
  mode: 'strict' | 'hybrid';
  status: 'active' | 'archived' | 'deleted';
  created_at: string;
  updated_at: string;
}

export interface ChatMessage {
  id: string;
  session_id: string;
  sender: 'user' | 'ai';
  message: string;
  answer?: string;
  metadata?: Record<string, any>;
  created_at: string;
}

// Dashboard types
export interface DashboardStats {
  total_courses: number;
  completed_courses: number;
  total_quizzes: number;
  total_time_spent: number;
  average_score: number;
  recent_activity: Array<{
    type: string;
    title: string;
    score?: number;
    date: string;
  }>;
  progress_by_course: Array<{
    course_id: string;
    course_title: string;
    progress: number;
  }>;
  weekly_progress: Array<{
    week: string;
    quizzes_taken: number;
    average_score: number;
  }>;
}

export interface Progress {
  id: string;
  user_id: string;
  course_id: string;
  chapter_id?: string;
  status: 'not_started' | 'in_progress' | 'completed';
  progress: number;
  time_spent: number;
  last_accessed: string;
  created_at: string;
  updated_at: string;
}

// API Response types
export interface ApiResponse<T> {
  data: T;
  message?: string;
}

export interface ApiError {
  detail: string;
  status_code: number;
}

// Form types
export interface LoginForm {
  email: string;
  password: string;
}

export interface RegisterForm {
  name: string;
  email: string;
  password: string;
}

export interface CourseForm {
  title: string;
  description: string;
  level: 'beginner' | 'intermediate' | 'advanced';
  tags: string[];
}

export interface ChapterForm {
  title: string;
  content: string;
  order: number;
}
