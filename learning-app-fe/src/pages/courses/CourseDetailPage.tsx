import React, { useEffect, useState } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { ArrowLeft, BookOpen, Clock, Star, Play, MessageCircle, Brain, Edit, Plus } from 'lucide-react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { Progress } from '@/components/ui/Progress';
import { LoadingSpinner } from '@/components/ui/LoadingSpinner';
import { Modal } from '@/components/ui/Modal';
import { Input } from '@/components/ui/Input';
import { useCourseStore } from '@/stores/courseStore';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { formatRelativeTime } from '@/lib/utils';

const chapterSchema = z.object({
  title: z.string().min(1, 'Title is required'),
  content: z.string().min(1, 'Content is required'),
  order: z.number().min(1, 'Order must be at least 1'),
});

type ChapterForm = z.infer<typeof chapterSchema>;

export function CourseDetailPage() {
  const { courseId } = useParams<{ courseId: string }>();
  const navigate = useNavigate();
  const { currentCourse, chapters, fetchCourse, fetchChapters, createChapter, isLoading } = useCourseStore();
  const [showAddChapter, setShowAddChapter] = useState(false);

  const chapterForm = useForm<ChapterForm>({
    resolver: zodResolver(chapterSchema),
    defaultValues: {
      order: 1,
    },
  });

  useEffect(() => {
    if (courseId) {
      fetchCourse(courseId);
      fetchChapters(courseId);
    }
  }, [courseId, fetchCourse, fetchChapters]);

  useEffect(() => {
    if (chapters.length > 0) {
      chapterForm.setValue('order', chapters.length + 1);
    }
  }, [chapters, chapterForm]);

  const onAddChapter = async (data: ChapterForm) => {
    if (!courseId) return;
    
    try {
      await createChapter(courseId, data);
      setShowAddChapter(false);
      chapterForm.reset();
      chapterForm.setValue('order', chapters.length + 2);
    } catch (error) {
      console.error('Failed to create chapter:', error);
    }
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <LoadingSpinner size="lg" />
      </div>
    );
  }

  if (!currentCourse) {
    return (
      <div className="p-6">
        <div className="text-center py-12">
          <h3 className="text-lg font-medium text-gray-900 mb-2">Course not found</h3>
          <p className="text-gray-600 mb-6">The course you're looking for doesn't exist.</p>
          <Link to="/courses">
            <Button>Back to Courses</Button>
          </Link>
        </div>
      </div>
    );
  }

  const sortedChapters = chapters.sort((a, b) => a.order - b.order);

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div className="flex items-center gap-4">
        <Button variant="outline" size="icon" onClick={() => navigate('/courses')}>
          <ArrowLeft className="h-4 w-4" />
        </Button>
        <div className="flex-1">
          <div className="flex items-center gap-2 text-sm text-gray-600 mb-1">
            <BookOpen className="h-4 w-4" />
            <span>Course</span>
          </div>
          <h1 className="text-3xl font-bold text-gray-900">{currentCourse.title}</h1>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Main Content */}
        <div className="lg:col-span-2 space-y-6">
          {/* Course Info */}
          <Card>
            <CardHeader>
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <CardTitle>Course Overview</CardTitle>
                  <CardDescription className="mt-2">
                    {currentCourse.description}
                  </CardDescription>
                </div>
                <span className={`
                  inline-flex items-center px-3 py-1 rounded-full text-sm font-medium
                  ${currentCourse.level === 'beginner' ? 'bg-green-100 text-green-800' :
                    currentCourse.level === 'intermediate' ? 'bg-yellow-100 text-yellow-800' :
                    'bg-red-100 text-red-800'}
                `}>
                  {currentCourse.level}
                </span>
              </div>
            </CardHeader>
            
            <CardContent>
              <div className="space-y-4">
                {/* Progress */}
                <div>
                  <div className="flex justify-between text-sm text-gray-600 mb-2">
                    <span>Course Progress</span>
                    <span>0% Complete</span>
                  </div>
                  <Progress value={0} />
                </div>

                {/* Tags */}
                {currentCourse.tags && currentCourse.tags.length > 0 && (
                  <div>
                    <h4 className="text-sm font-medium text-gray-900 mb-2">Tags</h4>
                    <div className="flex flex-wrap gap-2">
                      {currentCourse.tags.map((tag, index) => (
                        <span
                          key={index}
                          className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-primary-100 text-primary-800"
                        >
                          {tag}
                        </span>
                      ))}
                    </div>
                  </div>
                )}

                {/* Course Outline */}
                {currentCourse.outline && (
                  <div>
                    <h4 className="text-sm font-medium text-gray-900 mb-2">Course Outline</h4>
                    <div className="bg-gray-50 rounded-lg p-4">
                      <pre className="text-sm text-gray-700 whitespace-pre-wrap font-sans">
                        {currentCourse.outline}
                      </pre>
                    </div>
                  </div>
                )}

                {/* Actions */}
                <div className="flex flex-wrap gap-3 pt-4">
                  {sortedChapters.length > 0 && (
                    <Link to={`/courses/${courseId}/chapters/${sortedChapters[0].id}`}>
                      <Button>
                        <Play className="h-4 w-4 mr-2" />
                        Start Learning
                      </Button>
                    </Link>
                  )}
                  <Link to={`/chat?courseId=${courseId}`}>
                    <Button variant="outline">
                      <MessageCircle className="h-4 w-4 mr-2" />
                      Chat about Course
                    </Button>
                  </Link>
                  <Link to={`/quiz?courseId=${courseId}`}>
                    <Button variant="outline">
                      <Brain className="h-4 w-4 mr-2" />
                      Take Quiz
                    </Button>
                  </Link>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Course Info */}
          <Card>
            <CardHeader>
              <CardTitle>Course Information</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                <div>
                  <div className="text-sm text-gray-600">Created</div>
                  <div className="font-medium">{formatRelativeTime(currentCourse.created_at)}</div>
                </div>
                <div>
                  <div className="text-sm text-gray-600">Source</div>
                  <div className="font-medium">{currentCourse.source || 'Manual'}</div>
                </div>
                <div>
                  <div className="text-sm text-gray-600">Chapters</div>
                  <div className="font-medium">{chapters.length}</div>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Sidebar - Chapters */}
        <div>
          <Card>
            <CardHeader>
              <div className="flex items-center justify-between">
                <CardTitle>Chapters</CardTitle>
                <Button size="sm" onClick={() => setShowAddChapter(true)}>
                  <Plus className="h-4 w-4 mr-1" />
                  Add
                </Button>
              </div>
              <CardDescription>
                {chapters.length} chapter{chapters.length !== 1 ? 's' : ''}
              </CardDescription>
            </CardHeader>
            
            <CardContent>
              {sortedChapters.length > 0 ? (
                <div className="space-y-3">
                  {sortedChapters.map((chapter, index) => (
                    <Link
                      key={chapter.id}
                      to={`/courses/${courseId}/chapters/${chapter.id}`}
                      className="block"
                    >
                      <div className="flex items-center p-3 rounded-lg border hover:bg-gray-50 transition-colors">
                        <div className="flex-1">
                          <div className="flex items-center gap-2 mb-1">
                            <span className="text-xs font-medium text-gray-500">
                              Chapter {chapter.order}
                            </span>
                          </div>
                          <h4 className="font-medium text-gray-900 line-clamp-2">
                            {chapter.title}
                          </h4>
                        </div>
                        <div className="ml-3">
                          <div className="h-2 w-2 bg-gray-300 rounded-full"></div>
                        </div>
                      </div>
                    </Link>
                  ))}
                </div>
              ) : (
                <div className="text-center py-8">
                  <BookOpen className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                  <p className="text-gray-600 mb-4">No chapters yet</p>
                  <Button size="sm" onClick={() => setShowAddChapter(true)}>
                    Add First Chapter
                  </Button>
                </div>
              )}
            </CardContent>
          </Card>
        </div>
      </div>

      {/* Add Chapter Modal */}
      <Modal
        isOpen={showAddChapter}
        onClose={() => setShowAddChapter(false)}
        title="Add New Chapter"
        size="lg"
      >
        <form onSubmit={chapterForm.handleSubmit(onAddChapter)} className="space-y-4">
          <Input
            label="Chapter Title"
            error={chapterForm.formState.errors.title?.message}
            {...chapterForm.register('title')}
          />
          
          <Input
            label="Order"
            type="number"
            min="1"
            error={chapterForm.formState.errors.order?.message}
            {...chapterForm.register('order', { valueAsNumber: true })}
          />

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Content
            </label>
            <textarea
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
              rows={8}
              {...chapterForm.register('content')}
            />
            {chapterForm.formState.errors.content && (
              <p className="text-sm text-red-600 mt-1">
                {chapterForm.formState.errors.content.message}
              </p>
            )}
          </div>

          <div className="flex justify-end gap-3 pt-4">
            <Button type="button" variant="outline" onClick={() => setShowAddChapter(false)}>
              Cancel
            </Button>
            <Button type="submit" isLoading={chapterForm.formState.isSubmitting}>
              Add Chapter
            </Button>
          </div>
        </form>
      </Modal>
    </div>
  );
}
