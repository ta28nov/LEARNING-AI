import React, { useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Brain, Clock, Award, Play } from 'lucide-react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { LoadingSpinner } from '@/components/ui/LoadingSpinner';
import { useQuizStore } from '@/stores/quizStore';
import { formatRelativeTime } from '@/lib/utils';

export function QuizPage() {
  const { quizHistory, fetchQuizHistory } = useQuizStore();

  useEffect(() => {
    fetchQuizHistory();
  }, [fetchQuizHistory]);

  return (
    <div className="p-6 space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Quizzes</h1>
        <p className="text-gray-600">Test your knowledge and track your progress</p>
      </div>

      {/* Quick Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Quizzes</CardTitle>
            <Brain className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{quizHistory.length}</div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Average Score</CardTitle>
            <Award className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {quizHistory.length > 0 
                ? Math.round(quizHistory.reduce((acc, quiz) => acc + quiz.score, 0) / quizHistory.length)
                : 0
              }%
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Best Score</CardTitle>
            <Award className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {quizHistory.length > 0 ? Math.max(...quizHistory.map(q => q.score)) : 0}%
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Quiz History */}
      <Card>
        <CardHeader>
          <CardTitle>Quiz History</CardTitle>
          <CardDescription>Your recent quiz attempts</CardDescription>
        </CardHeader>
        <CardContent>
          {quizHistory.length > 0 ? (
            <div className="space-y-4">
              {quizHistory.map((quiz) => (
                <div key={quiz.id} className="flex items-center justify-between p-4 border rounded-lg">
                  <div className="flex items-center gap-4">
                    <div className={`
                      h-12 w-12 rounded-full flex items-center justify-center
                      ${quiz.score >= 80 ? 'bg-green-100 text-green-600' :
                        quiz.score >= 60 ? 'bg-yellow-100 text-yellow-600' :
                        'bg-red-100 text-red-600'
                      }
                    `}>
                      <span className="font-bold">{Math.round(quiz.score)}%</span>
                    </div>
                    
                    <div>
                      <h3 className="font-medium text-gray-900">Quiz Results</h3>
                      <div className="flex items-center gap-4 text-sm text-gray-600">
                        <span>{quiz.correct_answers}/{quiz.total_questions} correct</span>
                        <span className="flex items-center gap-1">
                          <Clock className="h-3 w-3" />
                          {formatRelativeTime(quiz.taken_at)}
                        </span>
                      </div>
                    </div>
                  </div>
                  
                  <Link to={`/quiz/results/${quiz.id}`}>
                    <Button variant="outline" size="sm">
                      View Details
                    </Button>
                  </Link>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center py-12">
              <Brain className="h-16 w-16 text-gray-400 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-gray-900 mb-2">No quizzes taken yet</h3>
              <p className="text-gray-600">Start learning and take your first quiz</p>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
