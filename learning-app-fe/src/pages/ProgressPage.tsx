import React, { useEffect } from 'react';
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { TrendingUp, BookOpen, Brain, Clock } from 'lucide-react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/Card';
import { Progress } from '@/components/ui/Progress';
import { LoadingSpinner } from '@/components/ui/LoadingSpinner';
import { useDashboardStore } from '@/stores/dashboardStore';
import { formatRelativeTime } from '@/lib/utils';

export function ProgressPage() {
  const { stats, progress, fetchStats, fetchProgress, isLoading } = useDashboardStore();

  useEffect(() => {
    fetchStats();
    fetchProgress();
  }, [fetchStats, fetchProgress]);

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <LoadingSpinner size="lg" />
      </div>
    );
  }

  // Sample data for charts
  const weeklyProgressData = stats?.weekly_progress || [
    { week: 'Week 1', quizzes_taken: 3, average_score: 85 },
    { week: 'Week 2', quizzes_taken: 5, average_score: 78 },
    { week: 'Week 3', quizzes_taken: 4, average_score: 92 },
    { week: 'Week 4', quizzes_taken: 6, average_score: 88 },
  ];

  const courseProgressData = stats?.progress_by_course || [];

  return (
    <div className="p-6 space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Learning Progress</h1>
        <p className="text-gray-600">Track your learning journey and achievements</p>
      </div>

      {/* Overview Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Courses Completed</CardTitle>
            <BookOpen className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats?.completed_courses || 0}</div>
            <p className="text-xs text-muted-foreground">
              of {stats?.total_courses || 0} total courses
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Average Score</CardTitle>
            <Brain className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats?.average_score?.toFixed(1) || 0}%</div>
            <p className="text-xs text-muted-foreground">
              Across all quizzes
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Study Time</CardTitle>
            <Clock className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats?.total_time_spent || 0}h</div>
            <p className="text-xs text-muted-foreground">
              Total learning time
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Streak</CardTitle>
            <TrendingUp className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">7</div>
            <p className="text-xs text-muted-foreground">
              Days learning
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Learning Progress Over Time */}
        <Card>
          <CardHeader>
            <CardTitle>Learning Progress Over Time</CardTitle>
            <CardDescription>Your weekly quiz performance</CardDescription>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={weeklyProgressData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="week" />
                <YAxis />
                <Tooltip />
                <Line 
                  type="monotone" 
                  dataKey="average_score" 
                  stroke="#2563eb" 
                  strokeWidth={2}
                  name="Average Score (%)"
                />
              </LineChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        {/* Quiz Scores by Course */}
        <Card>
          <CardHeader>
            <CardTitle>Quiz Scores by Course</CardTitle>
            <CardDescription>Performance across different courses</CardDescription>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={courseProgressData.slice(0, 5)}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="course_title" />
                <YAxis />
                <Tooltip />
                <Bar 
                  dataKey="progress" 
                  fill="#facc15"
                  name="Progress (%)"
                />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </div>

      {/* Course Progress Details */}
      <Card>
        <CardHeader>
          <CardTitle>Course Progress Details</CardTitle>
          <CardDescription>Detailed breakdown of your course progress</CardDescription>
        </CardHeader>
        <CardContent>
          {courseProgressData.length > 0 ? (
            <div className="space-y-4">
              {courseProgressData.map((course) => (
                <div key={course.course_id} className="flex items-center justify-between p-4 border rounded-lg">
                  <div className="flex-1">
                    <h3 className="font-medium text-gray-900">{course.course_title}</h3>
                    <div className="mt-2">
                      <Progress 
                        value={course.progress} 
                        showLabel 
                        className="w-full"
                      />
                    </div>
                  </div>
                  <div className="ml-4 text-right">
                    <div className="text-sm font-medium text-gray-900">
                      {course.progress.toFixed(1)}%
                    </div>
                    <div className="text-xs text-gray-600">Complete</div>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center py-8">
              <TrendingUp className="h-12 w-12 text-gray-400 mx-auto mb-4" />
              <p className="text-gray-600">No course progress data available</p>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Recent Activity */}
      <Card>
        <CardHeader>
          <CardTitle>Recent Activity</CardTitle>
          <CardDescription>Your latest learning activities</CardDescription>
        </CardHeader>
        <CardContent>
          {stats?.recent_activity && stats.recent_activity.length > 0 ? (
            <div className="space-y-3">
              {stats.recent_activity.map((activity, index) => (
                <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                  <div className="flex items-center gap-3">
                    <div className={`
                      h-8 w-8 rounded-full flex items-center justify-center
                      ${activity.type === 'quiz' ? 'bg-blue-100 text-blue-600' : 'bg-green-100 text-green-600'}
                    `}>
                      {activity.type === 'quiz' ? <Brain className="h-4 w-4" /> : <BookOpen className="h-4 w-4" />}
                    </div>
                    <div>
                      <h4 className="font-medium text-gray-900">{activity.title}</h4>
                      <p className="text-sm text-gray-600">{formatRelativeTime(activity.date)}</p>
                    </div>
                  </div>
                  {activity.score && (
                    <div className="text-sm font-medium text-gray-900">
                      {activity.score}%
                    </div>
                  )}
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center py-8">
              <Clock className="h-12 w-12 text-gray-400 mx-auto mb-4" />
              <p className="text-gray-600">No recent activity</p>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
