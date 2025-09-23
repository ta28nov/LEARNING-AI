import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { Plus, BookOpen, Clock, Star, Filter, Search } from 'lucide-react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { Progress } from '@/components/ui/Progress';
import { LoadingSpinner } from '@/components/ui/LoadingSpinner';
import { Modal } from '@/components/ui/Modal';
import { useCourseStore } from '@/stores/courseStore';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { formatRelativeTime } from '@/lib/utils';

const createCourseSchema = z.object({
  title: z.string().min(1, 'Title is required'),
  description: z.string().min(1, 'Description is required'),
  level: z.enum(['beginner', 'intermediate', 'advanced']),
  tags: z.string(),
});

const aiCourseSchema = z.object({
  topic: z.string().min(1, 'Topic is required'),
  level: z.enum(['beginner', 'intermediate', 'advanced']),
});

type CreateCourseForm = z.infer<typeof createCourseSchema>;
type AiCourseForm = z.infer<typeof aiCourseSchema>;

export function CoursesPage() {
  const { courses, fetchCourses, createCourse, createCourseFromPrompt, isLoading } = useCourseStore();
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [showAiModal, setShowAiModal] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const [levelFilter, setLevelFilter] = useState<string>('all');

  const createForm = useForm<CreateCourseForm>({
    resolver: zodResolver(createCourseSchema),
    defaultValues: {
      level: 'beginner',
    },
  });

  const aiForm = useForm<AiCourseForm>({
    resolver: zodResolver(aiCourseSchema),
    defaultValues: {
      level: 'beginner',
    },
  });

  useEffect(() => {
    fetchCourses();
  }, [fetchCourses]);

  const onCreateCourse = async (data: CreateCourseForm) => {
    try {
      const tags = data.tags.split(',').map(tag => tag.trim()).filter(Boolean);
      await createCourse({ ...data, tags });
      setShowCreateModal(false);
      createForm.reset();
    } catch (error) {
      console.error('Failed to create course:', error);
    }
  };

  const onCreateAiCourse = async (data: AiCourseForm) => {
    try {
      await createCourseFromPrompt(data.topic, data.level);
      setShowAiModal(false);
      aiForm.reset();
    } catch (error) {
      console.error('Failed to create AI course:', error);
    }
  };

  const filteredCourses = courses.filter(course => {
    const matchesSearch = course.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         course.description.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesLevel = levelFilter === 'all' || course.level === levelFilter;
    return matchesSearch && matchesLevel;
  });

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Courses</h1>
          <p className="text-gray-600">Explore and manage your learning courses</p>
        </div>
        <div className="flex gap-3">
          <Button onClick={() => setShowAiModal(true)} variant="secondary">
            <Plus className="h-4 w-4 mr-2" />
            AI Generate
          </Button>
          <Button onClick={() => setShowCreateModal(true)}>
            <Plus className="h-4 w-4 mr-2" />
            Create Course
          </Button>
        </div>
      </div>

      {/* Filters */}
      <div className="flex flex-col sm:flex-row gap-4">
        <div className="flex-1">
          <Input
            placeholder="Search courses..."
            icon={<Search className="h-4 w-4" />}
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>
        <div className="flex gap-2">
          <select
            className="px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
            value={levelFilter}
            onChange={(e) => setLevelFilter(e.target.value)}
          >
            <option value="all">All Levels</option>
            <option value="beginner">Beginner</option>
            <option value="intermediate">Intermediate</option>
            <option value="advanced">Advanced</option>
          </select>
        </div>
      </div>

      {/* Courses Grid */}
      {isLoading ? (
        <div className="flex items-center justify-center h-64">
          <LoadingSpinner size="lg" />
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredCourses.map((course) => (
            <Card key={course.id} className="hover:shadow-lg transition-shadow duration-200">
              <CardHeader>
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <CardTitle className="line-clamp-2">{course.title}</CardTitle>
                    <CardDescription className="line-clamp-3 mt-2">
                      {course.description}
                    </CardDescription>
                  </div>
                  <div className="ml-2">
                    <span className={`
                      inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium
                      ${course.level === 'beginner' ? 'bg-green-100 text-green-800' :
                        course.level === 'intermediate' ? 'bg-yellow-100 text-yellow-800' :
                        'bg-red-100 text-red-800'}
                    `}>
                      {course.level}
                    </span>
                  </div>
                </div>
              </CardHeader>
              
              <CardContent>
                <div className="space-y-4">
                  {/* Progress bar - placeholder for now */}
                  <div>
                    <div className="flex justify-between text-sm text-gray-600 mb-1">
                      <span>Progress</span>
                      <span>0%</span>
                    </div>
                    <Progress value={0} />
                  </div>

                  {/* Tags */}
                  {course.tags && course.tags.length > 0 && (
                    <div className="flex flex-wrap gap-1">
                      {course.tags.slice(0, 3).map((tag, index) => (
                        <span
                          key={index}
                          className="inline-flex items-center px-2 py-1 rounded-md text-xs font-medium bg-gray-100 text-gray-800"
                        >
                          {tag}
                        </span>
                      ))}
                      {course.tags.length > 3 && (
                        <span className="inline-flex items-center px-2 py-1 rounded-md text-xs font-medium bg-gray-100 text-gray-800">
                          +{course.tags.length - 3}
                        </span>
                      )}
                    </div>
                  )}

                  {/* Course info */}
                  <div className="flex items-center justify-between text-sm text-gray-600">
                    <div className="flex items-center">
                      <Clock className="h-4 w-4 mr-1" />
                      <span>{formatRelativeTime(course.created_at)}</span>
                    </div>
                    <div className="flex items-center">
                      <BookOpen className="h-4 w-4 mr-1" />
                      <span>{course.source || 'Manual'}</span>
                    </div>
                  </div>

                  {/* Actions */}
                  <div className="flex gap-2 pt-2">
                    <Link to={`/courses/${course.id}`} className="flex-1">
                      <Button variant="outline" className="w-full">
                        View Course
                      </Button>
                    </Link>
                    <Link to={`/courses/${course.id}/chapters/1`}>
                      <Button className="flex-1">
                        Start Learning
                      </Button>
                    </Link>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      )}

      {/* Empty state */}
      {!isLoading && filteredCourses.length === 0 && (
        <div className="text-center py-12">
          <BookOpen className="h-16 w-16 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">
            {searchTerm || levelFilter !== 'all' ? 'No courses found' : 'No courses yet'}
          </h3>
          <p className="text-gray-600 mb-6">
            {searchTerm || levelFilter !== 'all' 
              ? 'Try adjusting your search or filters'
              : 'Create your first course to get started with learning'
            }
          </p>
          {!searchTerm && levelFilter === 'all' && (
            <div className="flex justify-center gap-3">
              <Button onClick={() => setShowAiModal(true)} variant="secondary">
                Generate with AI
              </Button>
              <Button onClick={() => setShowCreateModal(true)}>
                Create Course
              </Button>
            </div>
          )}
        </div>
      )}

      {/* Create Course Modal */}
      <Modal
        isOpen={showCreateModal}
        onClose={() => setShowCreateModal(false)}
        title="Create New Course"
        size="lg"
      >
        <form onSubmit={createForm.handleSubmit(onCreateCourse)} className="space-y-4">
          <Input
            label="Course Title"
            error={createForm.formState.errors.title?.message}
            {...createForm.register('title')}
          />
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Description
            </label>
            <textarea
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
              rows={4}
              {...createForm.register('description')}
            />
            {createForm.formState.errors.description && (
              <p className="text-sm text-red-600 mt-1">
                {createForm.formState.errors.description.message}
              </p>
            )}
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Level
            </label>
            <select
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
              {...createForm.register('level')}
            >
              <option value="beginner">Beginner</option>
              <option value="intermediate">Intermediate</option>
              <option value="advanced">Advanced</option>
            </select>
          </div>

          <Input
            label="Tags (comma separated)"
            placeholder="e.g., programming, python, web development"
            {...createForm.register('tags')}
          />

          <div className="flex justify-end gap-3 pt-4">
            <Button type="button" variant="outline" onClick={() => setShowCreateModal(false)}>
              Cancel
            </Button>
            <Button type="submit" isLoading={createForm.formState.isSubmitting}>
              Create Course
            </Button>
          </div>
        </form>
      </Modal>

      {/* AI Generate Course Modal */}
      <Modal
        isOpen={showAiModal}
        onClose={() => setShowAiModal(false)}
        title="Generate Course with AI"
        size="lg"
      >
        <form onSubmit={aiForm.handleSubmit(onCreateAiCourse)} className="space-y-4">
          <Input
            label="Course Topic"
            placeholder="e.g., Introduction to Machine Learning"
            error={aiForm.formState.errors.topic?.message}
            {...aiForm.register('topic')}
          />

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Level
            </label>
            <select
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
              {...aiForm.register('level')}
            >
              <option value="beginner">Beginner</option>
              <option value="intermediate">Intermediate</option>
              <option value="advanced">Advanced</option>
            </select>
          </div>

          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
            <p className="text-sm text-blue-700">
              AI will generate a comprehensive course outline and content based on your topic and level.
              This may take a few moments.
            </p>
          </div>

          <div className="flex justify-end gap-3 pt-4">
            <Button type="button" variant="outline" onClick={() => setShowAiModal(false)}>
              Cancel
            </Button>
            <Button type="submit" isLoading={aiForm.formState.isSubmitting}>
              Generate Course
            </Button>
          </div>
        </form>
      </Modal>
    </div>
  );
}
