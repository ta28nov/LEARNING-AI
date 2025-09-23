import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { ArrowLeft, CheckCircle, XCircle, Clock } from 'lucide-react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { Progress } from '@/components/ui/Progress';
import { LoadingSpinner } from '@/components/ui/LoadingSpinner';
import { useQuizStore } from '@/stores/quizStore';

export function QuizDetailPage() {
  const { quizId } = useParams<{ quizId: string }>();
  const navigate = useNavigate();
  const { 
    currentQuiz, 
    questions, 
    currentQuestionIndex, 
    userAnswers, 
    currentResult,
    startQuiz, 
    nextQuestion, 
    previousQuestion, 
    setAnswer, 
    submitQuiz,
    resetQuiz,
    isLoading,
    isSubmitting
  } = useQuizStore();

  const [quizStarted, setQuizStarted] = useState(false);
  const [selectedAnswer, setSelectedAnswer] = useState<number | null>(null);

  useEffect(() => {
    if (quizId) {
      startQuiz(quizId);
    }
    
    return () => {
      resetQuiz();
    };
  }, [quizId, startQuiz, resetQuiz]);

  useEffect(() => {
    if (questions.length > 0) {
      const currentQuestion = questions[currentQuestionIndex];
      const existingAnswer = userAnswers.find(a => a.question_id === currentQuestion?.id);
      setSelectedAnswer(existingAnswer?.answer ?? null);
    }
  }, [currentQuestionIndex, questions, userAnswers]);

  const handleStartQuiz = () => {
    setQuizStarted(true);
  };

  const handleAnswerSelect = (answerIndex: number) => {
    if (!questions[currentQuestionIndex]) return;
    
    setSelectedAnswer(answerIndex);
    setAnswer(questions[currentQuestionIndex].id, answerIndex);
  };

  const handleNext = () => {
    if (currentQuestionIndex < questions.length - 1) {
      nextQuestion();
    }
  };

  const handlePrevious = () => {
    if (currentQuestionIndex > 0) {
      previousQuestion();
    }
  };

  const handleSubmit = async () => {
    try {
      await submitQuiz();
    } catch (error) {
      console.error('Failed to submit quiz:', error);
    }
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <LoadingSpinner size="lg" />
      </div>
    );
  }

  if (!currentQuiz || questions.length === 0) {
    return (
      <div className="p-6">
        <div className="text-center py-12">
          <h3 className="text-lg font-medium text-gray-900 mb-2">Quiz not found</h3>
          <p className="text-gray-600 mb-6">The quiz you're looking for doesn't exist.</p>
          <Button onClick={() => navigate('/quiz')}>
            Back to Quizzes
          </Button>
        </div>
      </div>
    );
  }

  // Show results if quiz is completed
  if (currentResult) {
    return (
      <div className="p-6 space-y-6">
        <div className="flex items-center gap-4">
          <Button variant="outline" size="icon" onClick={() => navigate('/quiz')}>
            <ArrowLeft className="h-4 w-4" />
          </Button>
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Quiz Results</h1>
            <p className="text-gray-600">{currentQuiz.title}</p>
          </div>
        </div>

        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-3">
              <div className={`
                h-16 w-16 rounded-full flex items-center justify-center text-2xl font-bold
                ${currentResult.score >= 80 ? 'bg-green-100 text-green-600' :
                  currentResult.score >= 60 ? 'bg-yellow-100 text-yellow-600' :
                  'bg-red-100 text-red-600'
                }
              `}>
                {Math.round(currentResult.score)}%
              </div>
              <div>
                <div className="text-2xl font-bold">
                  {currentResult.correct_answers} / {currentResult.total_questions}
                </div>
                <div className="text-sm text-gray-600">Correct Answers</div>
              </div>
            </CardTitle>
          </CardHeader>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Answer Review</CardTitle>
            <CardDescription>Review your answers and explanations</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-6">
              {currentResult.answers.map((answer, index) => (
                <div key={answer.question_id} className="border rounded-lg p-4">
                  <div className="flex items-start gap-3 mb-3">
                    {answer.is_correct ? (
                      <CheckCircle className="h-5 w-5 text-green-600 mt-1" />
                    ) : (
                      <XCircle className="h-5 w-5 text-red-600 mt-1" />
                    )}
                    <div className="flex-1">
                      <h4 className="font-medium text-gray-900 mb-2">
                        Question {index + 1}: {answer.question}
                      </h4>
                      
                      <div className="space-y-2">
                        <div className={`
                          p-2 rounded text-sm
                          ${answer.is_correct ? 'bg-green-50 text-green-700' : 'bg-red-50 text-red-700'}
                        `}>
                          Your answer: {questions.find(q => q.id === answer.question_id)?.options[answer.user_answer]}
                        </div>
                        
                        {!answer.is_correct && (
                          <div className="p-2 rounded text-sm bg-green-50 text-green-700">
                            Correct answer: {questions.find(q => q.id === answer.question_id)?.options[answer.correct_answer]}
                          </div>
                        )}
                      </div>
                      
                      {answer.explanation && (
                        <div className="mt-3 p-3 bg-blue-50 rounded text-sm text-blue-700">
                          <strong>Explanation:</strong> {answer.explanation}
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    );
  }

  // Show quiz start screen
  if (!quizStarted) {
    return (
      <div className="p-6 space-y-6">
        <div className="flex items-center gap-4">
          <Button variant="outline" size="icon" onClick={() => navigate('/quiz')}>
            <ArrowLeft className="h-4 w-4" />
          </Button>
          <div>
            <h1 className="text-3xl font-bold text-gray-900">{currentQuiz.title}</h1>
            <p className="text-gray-600">Ready to test your knowledge?</p>
          </div>
        </div>

        <Card>
          <CardHeader>
            <CardTitle>Quiz Information</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-6">
              <div>
                <div className="text-sm text-gray-600">Questions</div>
                <div className="font-medium">{questions.length}</div>
              </div>
              <div>
                <div className="text-sm text-gray-600">Time Limit</div>
                <div className="font-medium">No limit</div>
              </div>
              <div>
                <div className="text-sm text-gray-600">Attempts</div>
                <div className="font-medium">Unlimited</div>
              </div>
            </div>
            
            <Button onClick={handleStartQuiz} size="lg">
              Start Quiz
            </Button>
          </CardContent>
        </Card>
      </div>
    );
  }

  const currentQuestion = questions[currentQuestionIndex];
  const progress = ((currentQuestionIndex + 1) / questions.length) * 100;

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <Button variant="outline" size="icon" onClick={() => navigate('/quiz')}>
            <ArrowLeft className="h-4 w-4" />
          </Button>
          <div>
            <h1 className="text-2xl font-bold text-gray-900">
              Question {currentQuestionIndex + 1} of {questions.length}
            </h1>
            <p className="text-gray-600">{currentQuiz.title}</p>
          </div>
        </div>
        
        <Progress value={progress} className="w-32" />
      </div>

      {/* Question */}
      <Card>
        <CardHeader>
          <CardTitle className="text-xl">{currentQuestion.question}</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            {currentQuestion.options.map((option, index) => (
              <button
                key={index}
                onClick={() => handleAnswerSelect(index)}
                className={`
                  w-full text-left p-4 rounded-lg border transition-colors
                  ${selectedAnswer === index
                    ? 'border-primary-500 bg-primary-50'
                    : 'border-gray-200 hover:bg-gray-50'
                  }
                `}
              >
                <div className="flex items-center gap-3">
                  <div className={`
                    h-5 w-5 rounded-full border-2 flex items-center justify-center
                    ${selectedAnswer === index
                      ? 'border-primary-500 bg-primary-500'
                      : 'border-gray-300'
                    }
                  `}>
                    {selectedAnswer === index && (
                      <div className="h-2 w-2 bg-white rounded-full" />
                    )}
                  </div>
                  <span>{option}</span>
                </div>
              </button>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Navigation */}
      <div className="flex items-center justify-between">
        <Button
          variant="outline"
          onClick={handlePrevious}
          disabled={currentQuestionIndex === 0}
        >
          Previous
        </Button>
        
        <div className="flex gap-3">
          {currentQuestionIndex < questions.length - 1 ? (
            <Button onClick={handleNext}>
              Next
            </Button>
          ) : (
            <Button 
              onClick={handleSubmit}
              isLoading={isSubmitting}
              disabled={userAnswers.length !== questions.length}
            >
              Submit Quiz
            </Button>
          )}
        </div>
      </div>
    </div>
  );
}
