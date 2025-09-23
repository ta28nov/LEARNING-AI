import React, { useEffect, useState } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { ArrowLeft, ArrowRight, MessageCircle, Brain, BookOpen, ChevronLeft, ChevronRight } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { Progress } from '@/components/ui/Progress';
import { LoadingSpinner } from '@/components/ui/LoadingSpinner';
import { useCourseStore } from '@/stores/courseStore';
import { useDashboardStore } from '@/stores/dashboardStore';
import { formatRelativeTime } from '@/lib/utils';

export function ChapterPage() {
  const { courseId, chapterId } = useParams<{ courseId: string; chapterId: string }>();
  const navigate = useNavigate();
  const { 
    currentCourse, 
    chapters, 
    currentChapter, 
    fetchCourse, 
    fetchChapters, 
    fetchChapter 
  } = useCourseStore();
  const { updateProgress } = useDashboardStore();
  
  const [startTime] = useState(Date.now());
  const [isCompleted, setIsCompleted] = useState(false);

  useEffect(() => {
    if (courseId && chapterId) {
      fetchCourse(courseId);
      fetchChapters(courseId);
      fetchChapter(courseId, chapterId);
    }
  }, [courseId, chapterId, fetchCourse, fetchChapters, fetchChapter]);

  const sortedChapters = chapters.sort((a, b) => a.order - b.order);
  const currentIndex = sortedChapters.findIndex(c => c.id === chapterId);
  const previousChapter = currentIndex > 0 ? sortedChapters[currentIndex - 1] : null;
  const nextChapter = currentIndex < sortedChapters.length - 1 ? sortedChapters[currentIndex + 1] : null;

  const handleMarkComplete = async () => {
    if (!courseId || !chapterId) return;
    
    const timeSpent = Math.floor((Date.now() - startTime) / 60000); // minutes
    
    try {
      await updateProgress({
        course_id: courseId,
        chapter_id: chapterId,
        status: 'completed',
        progress: 100,
        time_spent: timeSpent,
      });
      setIsCompleted(true);
    } catch (error) {
      console.error('Failed to update progress:', error);
    }
  };

  if (!currentChapter || !currentCourse) {
    return (
      <div className="flex items-center justify-center h-64">
        <LoadingSpinner size="lg" />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b border-gray-200 sticky top-0 z-10">
        <div className="max-w-4xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <Button variant="outline" size="icon" onClick={() => navigate(`/courses/${courseId}`)}>
                <ArrowLeft className="h-4 w-4" />
              </Button>
              <div>
                <div className="flex items-center gap-2 text-sm text-gray-600">
                  <BookOpen className="h-4 w-4" />
                  <Link to={`/courses/${courseId}`} className="hover:text-primary-600">
                    {currentCourse.title}
                  </Link>
                  <span>/</span>
                  <span>Chapter {currentChapter.order}</span>
                </div>
                <h1 className="text-xl font-semibold text-gray-900">{currentChapter.title}</h1>
              </div>
            </div>
            
            <div className="flex items-center gap-3">
              <div className="text-sm text-gray-600">
                {currentIndex + 1} of {sortedChapters.length}
              </div>
              <Progress 
                value={((currentIndex + 1) / sortedChapters.length) * 100} 
                className="w-24"
              />
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-4xl mx-auto px-6 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
          {/* Main Content */}
          <div className="lg:col-span-3">
            <Card>
              <CardHeader>
                <div className="flex items-start justify-between">
                  <div>
                    <CardTitle>Chapter {currentChapter.order}: {currentChapter.title}</CardTitle>
                    <p className="text-sm text-gray-600 mt-1">
                      Added {formatRelativeTime(currentChapter.created_at)}
                    </p>
                  </div>
                  {isCompleted && (
                    <div className="flex items-center gap-2 text-green-600 bg-green-50 px-3 py-1 rounded-full">
                      <div className="h-2 w-2 bg-green-600 rounded-full"></div>
                      <span className="text-sm font-medium">Completed</span>
                    </div>
                  )}
                </div>
              </CardHeader>
              
              <CardContent>
                <div className="prose max-w-none">
                  <div className="whitespace-pre-wrap text-gray-700 leading-relaxed">
                    {currentChapter.content}
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Navigation */}
            <div className="flex items-center justify-between mt-8">
              <div>
                {previousChapter ? (
                  <Link to={`/courses/${courseId}/chapters/${previousChapter.id}`}>
                    <Button variant="outline">
                      <ChevronLeft className="h-4 w-4 mr-2" />
                      Previous: {previousChapter.title}
                    </Button>
                  </Link>
                ) : (
                  <div></div>
                )}
              </div>
              
              <div className="flex gap-3">
                {!isCompleted && (
                  <Button onClick={handleMarkComplete}>
                    Mark as Complete
                  </Button>
                )}
                
                {nextChapter ? (
                  <Link to={`/courses/${courseId}/chapters/${nextChapter.id}`}>
                    <Button>
                      Next: {nextChapter.title}
                      <ChevronRight className="h-4 w-4 ml-2" />
                    </Button>
                  </Link>
                ) : (
                  <Link to={`/courses/${courseId}`}>
                    <Button>
                      Course Complete
                      <ChevronRight className="h-4 w-4 ml-2" />
                    </Button>
                  </Link>
                )}
              </div>
            </div>
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* Quick Actions */}
            <Card>
              <CardHeader>
                <CardTitle className="text-lg">Quick Actions</CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                <Link to={`/quiz?courseId=${courseId}&chapterId=${chapterId}`}>
                  <Button variant="outline" className="w-full justify-start">
                    <Brain className="h-4 w-4 mr-2" />
                    Take Chapter Quiz
                  </Button>
                </Link>
                
                <Link to={`/chat?courseId=${courseId}&chapterId=${chapterId}`}>
                  <Button variant="ghost" className="w-full justify-start">
                    <MessageCircle className="h-4 w-4 mr-2" />
                    Chat about this Topic
                  </Button>
                </Link>
              </CardContent>
            </Card>

            {/* Chapter Navigation */}
            <Card>
              <CardHeader>
                <CardTitle className="text-lg">All Chapters</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  {sortedChapters.map((chapter, index) => (
                    <Link
                      key={chapter.id}
                      to={`/courses/${courseId}/chapters/${chapter.id}`}
                      className={`
                        block p-3 rounded-lg text-sm transition-colors
                        ${chapter.id === chapterId 
                          ? 'bg-primary-50 text-primary-700 border border-primary-200' 
                          : 'hover:bg-gray-50 text-gray-700'
                        }
                      `}
                    >
                      <div className="flex items-center gap-3">
                        <div className={`
                          h-6 w-6 rounded-full flex items-center justify-center text-xs font-medium
                          ${chapter.id === chapterId 
                            ? 'bg-primary-600 text-white' 
                            : 'bg-gray-200 text-gray-600'
                          }
                        `}>
                          {chapter.order}
                        </div>
                        <span className="font-medium line-clamp-2">{chapter.title}</span>
                      </div>
                    </Link>
                  ))}
                </div>
              </CardContent>
            </Card>

            {/* Course Progress */}
            <Card>
              <CardHeader>
                <CardTitle className="text-lg">Course Progress</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  <Progress value={((currentIndex + 1) / sortedChapters.length) * 100} showLabel />
                  <div className="text-sm text-gray-600">
                    {currentIndex + 1} of {sortedChapters.length} chapters completed
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
}
