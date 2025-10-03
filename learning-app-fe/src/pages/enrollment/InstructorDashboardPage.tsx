import React, { useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { Link } from 'react-router-dom';
import { useEnrollmentStore } from '@/stores/enrollmentStore';
import { useAuthStore } from '@/stores/authStore';
import { FadeIn } from '@/components/ui/FadeIn';
import { StaggerContainer } from '@/components/ui/StaggerContainer';
import { Button } from '@/components/ui/Button';
import { 
  BookOpen, 
  Users, 
  TrendingUp, 
  Star,
  Award,
  ArrowRight,
  BarChart3
} from 'lucide-react';

export const InstructorDashboardPage: React.FC = () => {
  const { t } = useTranslation();
  const { user } = useAuthStore();
  const { instructorDashboard, fetchInstructorDashboard, isLoading } = useEnrollmentStore();

  useEffect(() => {
    if (user && (user.role === 'instructor' || user.role === 'admin')) {
      fetchInstructorDashboard();
    }
  }, [user, fetchInstructorDashboard]);

  if (!user || (user.role !== 'instructor' && user.role !== 'admin')) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
            {t('common.accessDenied')}
          </h2>
          <p className="text-gray-600 dark:text-gray-400">
            This page is only accessible to instructors and administrators.
          </p>
        </div>
      </div>
    );
  }

  const stats = [
    {
      label: t('enrollment.totalCourses'),
      value: instructorDashboard?.total_courses || 0,
      icon: BookOpen,
      color: 'text-primary-600 dark:text-primary-400',
      bgColor: 'bg-primary-100 dark:bg-primary-900/30'
    },
    {
      label: t('enrollment.totalStudents'),
      value: instructorDashboard?.total_students || 0,
      icon: Users,
      color: 'text-secondary-600 dark:text-secondary-400',
      bgColor: 'bg-secondary-100 dark:bg-secondary-900/30'
    },
    {
      label: t('enrollment.totalEnrollments'),
      value: instructorDashboard?.total_enrollments || 0,
      icon: TrendingUp,
      color: 'text-accent-600 dark:text-accent-400',
      bgColor: 'bg-accent-100 dark:bg-accent-900/30'
    },
    {
      label: t('enrollment.averageRating'),
      value: instructorDashboard?.average_course_rating?.toFixed(1) || '0.0',
      icon: Star,
      color: 'text-warning-600 dark:text-warning-400',
      bgColor: 'bg-warning-100 dark:bg-warning-900/30'
    }
  ];

  return (
    <div className="container mx-auto px-4 py-8">
      <FadeIn>
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
            {t('enrollment.instructorDashboard')}
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            {t('enrollment.manageCoursesStudents')}
          </p>
        </div>
      </FadeIn>

      {/* Stats Grid */}
      <StaggerContainer className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        {stats.map((stat) => (
          <FadeIn key={stat.label} direction="up">
            <div className="glass p-6 rounded-xl">
              <div className={`w-12 h-12 ${stat.bgColor} rounded-lg flex items-center justify-center mb-4`}>
                <stat.icon className={`h-6 w-6 ${stat.color}`} />
              </div>
              <div className="text-3xl font-bold text-gray-900 dark:text-white mb-1">
                {stat.value}
              </div>
              <div className="text-sm text-gray-600 dark:text-gray-400">
                {stat.label}
              </div>
            </div>
          </FadeIn>
        ))}
      </StaggerContainer>

      {/* Course Analytics */}
      <FadeIn direction="up" delay={0.2}>
        <div className="glass p-6 rounded-xl">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white flex items-center gap-2">
              <BarChart3 className="h-6 w-6" />
              {t('enrollment.courseAnalytics')}
            </h2>
            <Link to="/courses">
              <Button variant="ghost" size="sm">
                {t('common.viewAll')}
                <ArrowRight className="ml-2 h-4 w-4" />
              </Button>
            </Link>
          </div>

          {isLoading ? (
            <div className="flex items-center justify-center py-12">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
            </div>
          ) : instructorDashboard?.recent_analytics && instructorDashboard.recent_analytics.length > 0 ? (
            <div className="space-y-4">
              {instructorDashboard.recent_analytics.map((analytics) => (
                <div
                  key={analytics.course_id}
                  className="p-4 rounded-lg border border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors"
                >
                  <div className="flex items-center justify-between mb-3">
                    <h3 className="font-semibold text-gray-900 dark:text-white">
                      {analytics.title}
                    </h3>
                    <Link to={`/courses/${analytics.course_id}`}>
                      <Button variant="ghost" size="sm">
                        {t('common.view')}
                      </Button>
                    </Link>
                  </div>
                  
                  <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
                    <div className="text-center p-3 bg-gray-50 dark:bg-gray-800 rounded-lg">
                      <div className="text-2xl font-bold text-primary-600 dark:text-primary-400">
                        {analytics.total_enrollments}
                      </div>
                      <div className="text-xs text-gray-600 dark:text-gray-400 mt-1">
                        {t('enrollment.enrollments')}
                      </div>
                    </div>
                    
                    <div className="text-center p-3 bg-gray-50 dark:bg-gray-800 rounded-lg">
                      <div className="text-2xl font-bold text-success-600 dark:text-success-400">
                        {analytics.active_students}
                      </div>
                      <div className="text-xs text-gray-600 dark:text-gray-400 mt-1">
                        {t('enrollment.activeStudents')}
                      </div>
                    </div>
                    
                    <div className="text-center p-3 bg-gray-50 dark:bg-gray-800 rounded-lg">
                      <div className="text-2xl font-bold text-accent-600 dark:text-accent-400">
                        {analytics.completed_students}
                      </div>
                      <div className="text-xs text-gray-600 dark:text-gray-400 mt-1">
                        {t('enrollment.completedStudents')}
                      </div>
                    </div>
                    
                    <div className="text-center p-3 bg-gray-50 dark:bg-gray-800 rounded-lg">
                      <div className="text-2xl font-bold text-warning-600 dark:text-warning-400">
                        {analytics.average_progress.toFixed(0)}%
                      </div>
                      <div className="text-xs text-gray-600 dark:text-gray-400 mt-1">
                        {t('enrollment.avgProgress')}
                      </div>
                    </div>
                    
                    <div className="text-center p-3 bg-gray-50 dark:bg-gray-800 rounded-lg">
                      <div className="text-2xl font-bold text-secondary-600 dark:text-secondary-400">
                        {analytics.completion_rate.toFixed(0)}%
                      </div>
                      <div className="text-xs text-gray-600 dark:text-gray-400 mt-1">
                        {t('enrollment.completionRate')}
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center py-12">
              <BookOpen className="mx-auto h-12 w-12 text-gray-400 dark:text-gray-600 mb-4" />
              <p className="text-gray-600 dark:text-gray-400 mb-4">
                {t('enrollment.noCoursesYet')}
              </p>
              <Link to="/courses">
                <Button>
                  {t('courses.createCourse')}
                </Button>
              </Link>
            </div>
          )}
        </div>
      </FadeIn>

      {/* Achievement Section */}
      {instructorDashboard && instructorDashboard.total_students > 0 && (
        <FadeIn direction="up" delay={0.3}>
          <div className="glass p-6 rounded-xl mt-6 bg-gradient-to-r from-accent-50 to-secondary-50 dark:from-accent-900/20 dark:to-secondary-900/20">
            <div className="flex items-center gap-4">
              <div className="w-16 h-16 bg-gradient-to-br from-accent-500 to-secondary-600 rounded-full flex items-center justify-center">
                <Award className="h-8 w-8 text-white" />
              </div>
              <div>
                <h3 className="text-lg font-bold text-gray-900 dark:text-white mb-1">
                  {t('enrollment.instructorAchievement')}
                </h3>
                <p className="text-gray-600 dark:text-gray-400">
                  {t('enrollment.taughtStudentsCount', { 
                    count: instructorDashboard.total_students 
                  })}
                </p>
              </div>
            </div>
          </div>
        </FadeIn>
      )}
    </div>
  );
};
