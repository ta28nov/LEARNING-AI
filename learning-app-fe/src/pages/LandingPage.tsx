import React from 'react';
import { Link } from 'react-router-dom';
import { ArrowRight, Upload, MessageCircle, Brain, BookOpen } from 'lucide-react';
import { Button } from '@/components/ui/Button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/Card';

export function LandingPage() {
  const features = [
    {
      icon: Upload,
      title: 'Upload & Learn',
      description: 'Upload your documents and let AI transform them into interactive learning experiences.'
    },
    {
      icon: MessageCircle,
      title: 'Chat with Your AI Tutor',
      description: 'Get instant answers and explanations from your personal AI tutor, available 24/7.'
    },
    {
      icon: Brain,
      title: 'Interactive Quizzes',
      description: 'Test your knowledge with AI-generated quizzes tailored to your learning materials.'
    }
  ];

  return (
    <div className="min-h-screen bg-white">
      {/* Navigation */}
      <nav className="bg-white shadow-sm">
        <div className="max-w-1440 mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center space-x-2">
              <BookOpen className="h-8 w-8 text-primary-600" />
              <span className="text-xl font-bold text-gray-900">AI Learning Platform</span>
            </div>
            <div className="flex items-center space-x-4">
              <Link to="/login">
                <Button variant="ghost">Sign In</Button>
              </Link>
              <Link to="/register">
                <Button>Get Started</Button>
              </Link>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="bg-gradient-to-br from-primary-50 to-secondary-50">
        <div className="max-w-1440 mx-auto px-4 sm:px-6 lg:px-8 py-24">
          <div className="grid grid-cols-12 gap-8 items-center">
            {/* Left Column - Content */}
            <div className="col-span-12 lg:col-span-6 space-y-8">
              <div className="space-y-4">
                <h1 className="text-4xl lg:text-6xl font-bold text-gray-900 leading-tight">
                  Unlock Your Potential with{' '}
                  <span className="text-primary-600">AI</span>
                </h1>
                <p className="text-xl text-gray-600 leading-relaxed">
                  Transform your learning experience with our AI-powered platform. 
                  Upload documents, chat with your AI tutor, and master any subject 
                  through personalized quizzes and interactive content.
                </p>
              </div>
              
              <div className="flex flex-col sm:flex-row gap-4">
                <Link to="/register">
                  <Button size="lg" className="w-full sm:w-auto">
                    Start Learning Now
                    <ArrowRight className="ml-2 h-5 w-5" />
                  </Button>
                </Link>
                <Link to="/login">
                  <Button variant="outline" size="lg" className="w-full sm:w-auto">
                    Sign In
                  </Button>
                </Link>
              </div>
            </div>

            {/* Right Column - Illustration */}
            <div className="col-span-12 lg:col-span-6">
              <div className="relative">
                {/* Abstract AI/Learning illustration */}
                <div className="bg-gradient-to-br from-primary-100 to-secondary-100 rounded-2xl p-12 shadow-lg">
                  <div className="grid grid-cols-3 gap-4">
                    <div className="space-y-4">
                      <div className="h-16 bg-primary-200 rounded-lg animate-pulse"></div>
                      <div className="h-12 bg-secondary-200 rounded-lg animate-pulse delay-75"></div>
                      <div className="h-20 bg-primary-300 rounded-lg animate-pulse delay-150"></div>
                    </div>
                    <div className="space-y-4 pt-8">
                      <div className="h-20 bg-secondary-300 rounded-lg animate-pulse delay-100"></div>
                      <div className="h-16 bg-primary-200 rounded-lg animate-pulse delay-200"></div>
                      <div className="h-12 bg-secondary-200 rounded-lg animate-pulse"></div>
                    </div>
                    <div className="space-y-4 pt-4">
                      <div className="h-12 bg-primary-300 rounded-lg animate-pulse delay-75"></div>
                      <div className="h-20 bg-secondary-200 rounded-lg animate-pulse delay-150"></div>
                      <div className="h-16 bg-primary-200 rounded-lg animate-pulse delay-100"></div>
                    </div>
                  </div>
                  
                  {/* Floating elements */}
                  <div className="absolute -top-4 -right-4 h-8 w-8 bg-primary-500 rounded-full animate-bounce"></div>
                  <div className="absolute -bottom-4 -left-4 h-6 w-6 bg-secondary-400 rounded-full animate-bounce delay-200"></div>
                  <div className="absolute top-1/2 -left-2 h-4 w-4 bg-primary-400 rounded-full animate-pulse"></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-24 bg-white">
        <div className="max-w-1440 mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl lg:text-4xl font-bold text-gray-900 mb-4">
              Powerful Features for Modern Learning
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Experience the future of education with AI-powered tools designed to enhance your learning journey.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {features.map((feature, index) => {
              const Icon = feature.icon;
              return (
                <Card key={index} className="text-center hover:shadow-lg transition-shadow duration-300">
                  <CardHeader>
                    <div className="mx-auto h-16 w-16 bg-primary-100 rounded-2xl flex items-center justify-center mb-4">
                      <Icon className="h-8 w-8 text-primary-600" />
                    </div>
                    <CardTitle className="text-xl font-semibold">
                      {feature.title}
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <CardDescription className="text-base">
                      {feature.description}
                    </CardDescription>
                  </CardContent>
                </Card>
              );
            })}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-24 bg-gradient-to-r from-primary-600 to-primary-700">
        <div className="max-w-1440 mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <div className="space-y-6">
            <h2 className="text-3xl lg:text-4xl font-bold text-white">
              Ready to Transform Your Learning?
            </h2>
            <p className="text-xl text-primary-100 max-w-2xl mx-auto">
              Join thousands of learners who are already using AI to accelerate their education.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link to="/register">
                <Button variant="secondary" size="lg" className="w-full sm:w-auto">
                  Get Started Free
                  <ArrowRight className="ml-2 h-5 w-5" />
                </Button>
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-12">
        <div className="max-w-1440 mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <div className="flex items-center space-x-2 mb-4 md:mb-0">
              <BookOpen className="h-6 w-6" />
              <span className="text-lg font-semibold">AI Learning Platform</span>
            </div>
            <div className="flex space-x-8">
              <a href="#" className="text-gray-400 hover:text-white transition-colors">
                Privacy Policy
              </a>
              <a href="#" className="text-gray-400 hover:text-white transition-colors">
                Terms of Service
              </a>
            </div>
          </div>
          <div className="mt-8 pt-8 border-t border-gray-800 text-center text-gray-400">
            <p>&copy; 2024 AI Learning Platform. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  );
}
