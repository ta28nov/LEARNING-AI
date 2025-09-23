import React, { useEffect } from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { useAuthStore } from '@/stores/authStore';

// Layout components
import { ProtectedRoute } from '@/components/layout/ProtectedRoute';
import { DashboardLayout } from '@/components/layout/DashboardLayout';

// Page components
import { LandingPage } from '@/pages/LandingPage';
import { LoginPage } from '@/pages/auth/LoginPage';
import { RegisterPage } from '@/pages/auth/RegisterPage';
import ForgotPasswordPage from '@/pages/auth/ForgotPasswordPage';
import ResetPasswordPage from '@/pages/auth/ResetPasswordPage';
import VerifyEmailPage from '@/pages/auth/VerifyEmailPage';
import { DashboardPage } from '@/pages/DashboardPage';
import { CoursesPage } from '@/pages/courses/CoursesPage';
import { CourseDetailPage } from '@/pages/courses/CourseDetailPage';
import { ChapterPage } from '@/pages/courses/ChapterPage';
import { UploadsPage } from '@/pages/UploadsPage';
import { ChatPage } from '@/pages/chat/ChatPage';
import { QuizPage } from '@/pages/quiz/QuizPage';
import { QuizDetailPage } from '@/pages/quiz/QuizDetailPage';
import { ProgressPage } from '@/pages/ProgressPage';
import { AdminPage } from '@/pages/admin/AdminPage';
import { ProfilePage } from '@/pages/ProfilePage';

function App() {
  const { isAuthenticated, token, getCurrentUser } = useAuthStore();

  // Initialize user data on app start if token exists
  useEffect(() => {
    if (token && !isAuthenticated) {
      getCurrentUser().catch(() => {
        // Token might be expired, user will be redirected to login
      });
    }
  }, [token, isAuthenticated, getCurrentUser]);

  return (
    <Routes>
      {/* Public routes */}
      <Route path="/" element={<LandingPage />} />
      <Route 
        path="/login" 
        element={isAuthenticated ? <Navigate to="/dashboard" replace /> : <LoginPage />} 
      />
      <Route 
        path="/register" 
        element={isAuthenticated ? <Navigate to="/dashboard" replace /> : <RegisterPage />} 
      />
      <Route 
        path="/auth/login" 
        element={isAuthenticated ? <Navigate to="/dashboard" replace /> : <LoginPage />} 
      />
      <Route 
        path="/auth/register" 
        element={isAuthenticated ? <Navigate to="/dashboard" replace /> : <RegisterPage />} 
      />
      <Route 
        path="/auth/forgot-password" 
        element={isAuthenticated ? <Navigate to="/dashboard" replace /> : <ForgotPasswordPage />} 
      />
      <Route 
        path="/auth/reset-password" 
        element={isAuthenticated ? <Navigate to="/dashboard" replace /> : <ResetPasswordPage />} 
      />
      <Route 
        path="/auth/verify-email" 
        element={isAuthenticated ? <Navigate to="/dashboard" replace /> : <VerifyEmailPage />} 
      />

      {/* Protected routes with dashboard layout */}
      <Route
        path="/dashboard"
        element={
          <ProtectedRoute>
            <DashboardLayout>
              <DashboardPage />
            </DashboardLayout>
          </ProtectedRoute>
        }
      />
      
      <Route
        path="/courses"
        element={
          <ProtectedRoute>
            <DashboardLayout>
              <CoursesPage />
            </DashboardLayout>
          </ProtectedRoute>
        }
      />
      
      <Route
        path="/courses/:courseId"
        element={
          <ProtectedRoute>
            <DashboardLayout>
              <CourseDetailPage />
            </DashboardLayout>
          </ProtectedRoute>
        }
      />
      
      <Route
        path="/courses/:courseId/chapters/:chapterId"
        element={
          <ProtectedRoute>
            <DashboardLayout>
              <ChapterPage />
            </DashboardLayout>
          </ProtectedRoute>
        }
      />
      
      <Route
        path="/uploads"
        element={
          <ProtectedRoute>
            <DashboardLayout>
              <UploadsPage />
            </DashboardLayout>
          </ProtectedRoute>
        }
      />
      
      <Route
        path="/chat"
        element={
          <ProtectedRoute>
            <DashboardLayout>
              <ChatPage />
            </DashboardLayout>
          </ProtectedRoute>
        }
      />
      
      <Route
        path="/quiz"
        element={
          <ProtectedRoute>
            <DashboardLayout>
              <QuizPage />
            </DashboardLayout>
          </ProtectedRoute>
        }
      />
      
      <Route
        path="/quiz/:quizId"
        element={
          <ProtectedRoute>
            <DashboardLayout>
              <QuizDetailPage />
            </DashboardLayout>
          </ProtectedRoute>
        }
      />
      
      <Route
        path="/progress"
        element={
          <ProtectedRoute>
            <DashboardLayout>
              <ProgressPage />
            </DashboardLayout>
          </ProtectedRoute>
        }
      />
      
      <Route
        path="/profile"
        element={
          <ProtectedRoute>
            <DashboardLayout>
              <ProfilePage />
            </DashboardLayout>
          </ProtectedRoute>
        }
      />
      
      <Route
        path="/admin/*"
        element={
          <ProtectedRoute requiredRole="admin">
            <DashboardLayout>
              <AdminPage />
            </DashboardLayout>
          </ProtectedRoute>
        }
      />

      {/* Catch all route */}
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}

export default App;
