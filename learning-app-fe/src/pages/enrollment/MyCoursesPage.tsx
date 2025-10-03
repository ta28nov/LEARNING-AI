import React, { useEffect, useState } from 'react';
import { useTranslation } from 'react-i18next';
import { Link } from 'react-router-dom';
import { useEnrollmentStore } from '@/stores/enrollmentStore';
import { useAuthStore } from '@/stores/authStore';
import { FadeIn } from '@/components/ui/FadeIn';
import { StaggerContainer } from '@/components/ui/StaggerContainer';
import { Button } from '@/components/ui/Button';
import { 
  BookOpen, 
  Filter, 
  Search, 
  ArrowRight,
  CheckCircle,
  Clock,
  XCircle
} from 'lucide-react';
import type { EnrollmentStatus } from '@/types';

export const MyCoursesPage: React.FC = () => {
  const { t } = useTranslation();
  const { user } = useAuthStore();
  const { enrolledCourses, fetchEnrolledCourses, isLoading } = useEnrollmentStore();
  const [searchQuery, setSearchQuery] = useState('');
  const [statusFilter, setStatusFilter] = useState<EnrollmentStatus | 'all'>('all');

  useEffect(() => {
    if (user?.role === 'student') {
      fetchEnrolledCourses();
    }
  }, [user, fetchEnrolledCourses]);

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

  // Filter courses
  const filteredCourses = enrolledCourses.filter(course => {
    const matchesSearch = course.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         course.description?.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesStatus = statusFilter === 'all' || course.enrollment_status === statusFilter;
    return matchesSearch && matchesStatus;
  });

  const statusOptions: { value: EnrollmentStatus | 'all'; label: string; icon: typeof BookOpen; color: string }[] = [
    { value: 'all', label: t('enrollment.allCourses'), icon: BookOpen, color: 'text-gray-600' },
    { value: 'active', label: t('enrollment.activeCourses'), icon: Clock, color: 'text-primary-600' },
    { value: 'completed', label: t('enrollment.completedCourses'), icon: CheckCircle, color: 'text-success-600' },
    { value: 'dropped', label: t('enrollment.droppedCourses'), icon: XCircle, color: 'text-error-600' },
  ];

  return (
    <div className="container mx-auto px-4 py-8">
      <FadeIn>
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
            {t('enrollment.myCourses')}
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            {t('enrollment.myCoursesDescription')}
          </p>
        </div>
      </FadeIn>

      {/* Search and Filter */}
      <FadeIn direction="up" delay={0.1}>
        <div className="flex flex-col sm:flex-row gap-4 mb-6">
          {/* Search */}
          <div className="flex-1 relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
            <input
              type="text"
              placeholder={t('courses.searchCourses')}
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-10 pr-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            />
          </div>

          {/* Status Filter */}
          <div className="flex gap-2 overflow-x-auto">
            {statusOptions.map((option) => (
              <button
                key={option.value}
                onClick={() => setStatusFilter(option.value)}
                className={`
                  flex items-center gap-2 px-4 py-2 rounded-lg font-medium transition-all whitespace-nowrap
                  ${statusFilter === option.value
                    ? 'bg-primary-600 text-white shadow-lg'
                    : 'bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-300 border border-gray-300 dark:border-gray-600 hover:bg-gray-50 dark:hover:bg-gray-700'
                  }
                `}
              >
                <option.icon className="h-4 w-4" />
                {option.label}
              </button>
            ))}
          </div>
        </div>
      </FadeIn>

      {/* Courses Grid */}
      {isLoading ? (
        <div className="flex items-center justify-center py-12">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
        </div>
      ) : filteredCourses.length > 0 ? (
        <StaggerContainer className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredCourses.map((course, index) => (
            <FadeIn key={course.course_id} direction="up" delay={index * 0.1}>
              <div className="glass p-6 rounded-xl hover:shadow-xl transition-all duration-300 group">
                {/* Status Badge */}
                <div className="flex items-center justify-between mb-4">
                  <span className={`
                    inline-flex items-center px-3 py-1 rounded-full text-xs font-medium
                    ${course.enrollment_status === 'active' ? 'bg-primary-100 text-primary-800 dark:bg-primary-900/30 dark:text-primary-400' :
                      course.enrollment_status === 'completed' ? 'bg-success-100 text-success-800 dark:bg-success-900/30 dark:text-success-400' :
                      'bg-gray-100 text-gray-800 dark:bg-gray-900/30 dark:text-gray-400'}
                  `}>
                    {course.enrollment_status === 'active' ? t('enrollment.active') :
                     course.enrollment_status === 'completed' ? t('enrollment.completed') :
                     t('enrollment.dropped')}
                  </span>
                  <span className={`
                    inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium
                    ${course.level === 'beginner' ? 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400' :
                      course.level === 'intermediate' ? 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-400' :
                      'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400'}
                  `}>
                    {t(`courses.${course.level}`)}
                  </span>
                </div>

                {/* Course Info */}
                <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-2 group-hover:text-primary-600 dark:group-hover:text-primary-400 transition-colors">
                  {course.title}
                </h3>
                <p className="text-gray-600 dark:text-gray-400 mb-4 line-clamp-2">
                  {course.description}
                </p>

                {/* Progress */}
                <div className="mb-4">
                  <div className="flex justify-between text-sm text-gray-600 dark:text-gray-400 mb-2">
                    <span>{t('enrollment.progress')}</span>
                    <span className="font-semibold">{course.progress.toFixed(0)}%</span>
                  </div>
                  <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                    <div
                      className="bg-gradient-to-r from-primary-600 to-primary-500 h-2 rounded-full transition-all duration-300"
                      style={{ width: `${course.progress}%` }}
                    />
                  </div>
                </div>

                {/* Enrolled Date */}
                <div className="text-xs text-gray-500 dark:text-gray-500 mb-4">
                  {t('enrollment.enrolledOn')} {new Date(course.enrolled_at).toLocaleDateString()}
                </div>

                {/* Action Button */}
                <Link to={`/courses/${course.course_id}`}>
                  <Button variant="outline" size="sm" className="w-full group-hover:bg-primary-600 group-hover:text-white group-hover:border-primary-600">
                    {t('courses.viewCourse')}
                    <ArrowRight className="ml-2 h-4 w-4" />
                  </Button>
                </Link>
              </div>
            </FadeIn>
          ))}
        </StaggerContainer>
      ) : (
        <FadeIn direction="up">
          <div className="text-center py-12 glass rounded-xl">
            <BookOpen className="mx-auto h-16 w-16 text-gray-400 dark:text-gray-600 mb-4" />
            <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">
              {searchQuery || statusFilter !== 'all' 
                ? t('enrollment.noCoursesMatch')
                : t('enrollment.noEnrolledCourses')}
            </h3>
            <p className="text-gray-600 dark:text-gray-400 mb-6">
              {searchQuery || statusFilter !== 'all'
                ? t('enrollment.tryDifferentFilters')
                : t('enrollment.browseAndEnroll')}
            </p>
            {(!searchQuery && statusFilter === 'all') && (
              <Link to="/courses">
                <Button>
                  {t('dashboard.browseCourses')}
                </Button>
              </Link>
            )}
          </div>
        </FadeIn>
      )}
    </div>
  );
};
