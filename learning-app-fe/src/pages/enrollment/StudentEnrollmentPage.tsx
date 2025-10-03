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
  CheckCircle2, 
  Clock, 
  TrendingUp, 
  ArrowRight,
  Award,
  Target
} from 'lucide-react';

export const StudentEnrollmentPage: React.FC = () => {
  const { t } = useTranslation();
  const { user } = useAuthStore();
  const { studentDashboard, fetchStudentDashboard, isLoading } = useEnrollmentStore();

  useEffect(() => {
    if (user?.role === 'student') {
      fetchStudentDashboard();
    }
  }, [user, fetchStudentDashboard]);

  if (!user || user.role !== 'student') {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
            {t('common.accessDenied')}
          </h2>
          <p className="text-gray-600 dark:text-gray-400">
            This page is only accessible to students.
          </p>
        </div>
      </div>
    );
  }

  const stats = [
    {
      label: t('enrollment.totalEnrolled'),
      value: studentDashboard?.total_enrolled_courses || 0,
      icon: BookOpen,
      color: 'text-primary-600 dark:text-primary-400',
      bgColor: 'bg-primary-100 dark:bg-primary-900/30'
    },
    {
      label: t('enrollment.completed'),
      value: studentDashboard?.completed_courses || 0,
      icon: CheckCircle2,
      color: 'text-success-600 dark:text-success-400',
      bgColor: 'bg-success-100 dark:bg-success-900/30'
    },
    {
      label: t('enrollment.inProgress'),
      value: studentDashboard?.in_progress_courses || 0,
      icon: Target,
      color: 'text-warning-600 dark:text-warning-400',
      bgColor: 'bg-warning-100 dark:bg-warning-900/30'
    },
    {
      label: t('enrollment.averageProgress'),
      value: `${studentDashboard?.average_progress?.toFixed(1) || 0}%`,
      icon: TrendingUp,
      color: 'text-accent-600 dark:text-accent-400',
      bgColor: 'bg-accent-100 dark:bg-accent-900/30'
    },
    {
      label: t('enrollment.timeSpent'),
      value: `${Math.floor((studentDashboard?.total_time_spent || 0) / 60)}h`,
      icon: Clock,
      color: 'text-secondary-600 dark:text-secondary-400',
      bgColor: 'bg-secondary-100 dark:bg-secondary-900/30'
    }
  ];

  return (
    <div className="container mx-auto px-4 py-8">
      <FadeIn>
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
            {t('enrollment.myLearning')}
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            {t('enrollment.trackProgress')}
          </p>
        </div>
      </FadeIn>

      {/* Stats Grid */}
      <StaggerContainer className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-5 gap-6 mb-8">
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

      {/* Recent Courses */}
      <FadeIn direction="up" delay={0.2}>
        <div className="glass p-6 rounded-xl">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
              {t('enrollment.recentCourses')}
            </h2>
            <Link to="/my-courses">
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
          ) : studentDashboard?.recent_courses && studentDashboard.recent_courses.length > 0 ? (
            <div className="space-y-4">
              {studentDashboard.recent_courses.map((course) => (
                <div
                  key={course.course_id}
                  className="flex items-center justify-between p-4 rounded-lg border border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors"
                >
                  <div className="flex-1">
                    <h3 className="font-semibold text-gray-900 dark:text-white mb-1">
                      {course.title}
                    </h3>
                    <div className="flex items-center gap-4 text-sm text-gray-600 dark:text-gray-400">
                      <span className="capitalize">{course.level}</span>
                      <span>•</span>
                      <span>{course.progress.toFixed(0)}% {t('common.complete')}</span>
                    </div>
                    {/* Progress bar */}
                    <div className="mt-2 w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                      <div
                        className="bg-gradient-to-r from-primary-600 to-primary-500 h-2 rounded-full transition-all duration-300"
                        style={{ width: `${course.progress}%` }}
                      />
                    </div>
                  </div>
                  <Link to={`/courses/${course.course_id}`}>
                    <Button variant="ghost" size="sm">
                      {t('courses.viewCourse')}
                      <ArrowRight className="ml-2 h-4 w-4" />
                    </Button>
                  </Link>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center py-12">
              <BookOpen className="mx-auto h-12 w-12 text-gray-400 dark:text-gray-600 mb-4" />
              <p className="text-gray-600 dark:text-gray-400 mb-4">
                {t('enrollment.noEnrolledCourses')}
              </p>
              <Link to="/courses">
                <Button>
                  {t('dashboard.browseCourses')}
                </Button>
              </Link>
            </div>
          )}
        </div>
      </FadeIn>

      {/* Achievement placeholder */}
      {studentDashboard && studentDashboard.completed_courses > 0 && (
        <FadeIn direction="up" delay={0.3}>
          <div className="glass p-6 rounded-xl mt-6 bg-gradient-to-r from-accent-50 to-primary-50 dark:from-accent-900/20 dark:to-primary-900/20">
            <div className="flex items-center gap-4">
              <div className="w-16 h-16 bg-gradient-to-br from-accent-500 to-primary-600 rounded-full flex items-center justify-center">
                <Award className="h-8 w-8 text-white" />
              </div>
              <div>
                <h3 className="text-lg font-bold text-gray-900 dark:text-white mb-1">
                  {t('enrollment.achievement')}
                </h3>
                <p className="text-gray-600 dark:text-gray-400">
                  {t('enrollment.completedCourseCount', { 
                    count: studentDashboard.completed_courses 
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
