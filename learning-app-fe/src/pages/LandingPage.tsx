import React from 'react';
import { Link } from 'react-router-dom';
import { ArrowRight, Upload, MessageCircle, Brain, BookOpen, Sparkles, Zap, Target } from 'lucide-react';
import { Button } from '@/components/ui/Button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/Card';

export function LandingPage() {
  const features = [
    {
      icon: Upload,
      title: 'Upload & Learn',
      description: 'Upload your documents and let AI transform them into interactive learning experiences.',
      gradient: 'from-blue-500 to-purple-600'
    },
    {
      icon: MessageCircle,
      title: 'Chat with Your AI Tutor',
      description: 'Get instant answers and explanations from your personal AI tutor, available 24/7.',
      gradient: 'from-purple-500 to-pink-600'
    },
    {
      icon: Brain,
      title: 'Interactive Quizzes',
      description: 'Test your knowledge with AI-generated quizzes tailored to your learning materials.',
      gradient: 'from-green-500 to-teal-600'
    }
  ];

  const stats = [
    { label: 'Active Learners', value: '10K+', icon: Target },
    { label: 'AI Interactions', value: '1M+', icon: Zap },
    { label: 'Success Rate', value: '95%', icon: Sparkles }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-blue-50 dark:from-slate-900 dark:via-slate-800 dark:to-slate-900">
      {/* Navigation */}
      <nav className="glass border-b border-white/20 dark:border-white/10 sticky top-0 z-50 backdrop-blur-md">
        <div className="max-w-1440 mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center space-x-3">
              <div className="relative">
                <div className="absolute inset-0 bg-gradient-to-r from-primary-600 to-secondary-600 rounded-lg blur-sm opacity-75"></div>
                <BookOpen className="relative h-8 w-8 text-white" />
              </div>
              <span className="text-xl font-bold gradient-text">AI Learning Platform</span>
            </div>
            <div className="flex items-center space-x-4">
              <Link to="/login">
                <Button variant="ghost">Sign In</Button>
              </Link>
              <Link to="/register">
                <Button variant="primary" size="lg">
                  Get Started
                  <ArrowRight className="ml-2 h-4 w-4" />
                </Button>
              </Link>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="relative overflow-hidden">
        {/* Background Elements */}
        <div className="absolute inset-0 bg-gradient-to-br from-primary-50/50 via-transparent to-secondary-50/50"></div>
        <div className="absolute top-0 left-1/4 w-96 h-96 bg-primary-200/20 rounded-full blur-3xl animate-pulse-slow"></div>
        <div className="absolute bottom-0 right-1/4 w-96 h-96 bg-secondary-200/20 rounded-full blur-3xl animate-pulse-slow delay-1000"></div>
        
        <div className="relative max-w-1440 mx-auto px-4 sm:px-6 lg:px-8 py-24">
          <div className="grid grid-cols-12 gap-8 items-center">
            {/* Left Column - Content */}
            <div className="col-span-12 lg:col-span-6 space-y-8 animate-fade-in">
              <div className="space-y-6">
                <div className="inline-flex items-center px-4 py-2 rounded-full bg-primary-100 dark:bg-primary-900/20 text-primary-700 dark:text-primary-300 text-sm font-medium">
                  <Sparkles className="h-4 w-4 mr-2" />
                  AI-Powered Learning Platform
                </div>
                <h1 className="text-5xl lg:text-7xl font-bold leading-tight">
                  Unlock Your Potential with{' '}
                  <span className="gradient-text-secondary">AI</span>
                </h1>
                <p className="text-xl text-slate-600 dark:text-slate-300 leading-relaxed max-w-2xl">
                  Transform your learning experience with our AI-powered platform. 
                  Upload documents, chat with your AI tutor, and master any subject 
                  through personalized quizzes and interactive content.
                </p>
              </div>
              
              <div className="flex flex-col sm:flex-row gap-4">
                <Link to="/register">
                  <Button variant="primary" size="xl" className="w-full sm:w-auto group">
                    Start Learning Now
                    <ArrowRight className="ml-2 h-5 w-5 group-hover:translate-x-1 transition-transform" />
                  </Button>
                </Link>
                <Link to="/login">
                  <Button variant="outline" size="xl" className="w-full sm:w-auto">
                    Sign In
                  </Button>
                </Link>
              </div>

              {/* Stats */}
              <div className="grid grid-cols-3 gap-6 pt-8">
                {stats.map((stat, index) => {
                  const Icon = stat.icon;
                  return (
                    <div key={index} className="text-center animate-scale-in" style={{ animationDelay: `${index * 100}ms` }}>
                      <div className="inline-flex items-center justify-center w-12 h-12 rounded-xl bg-gradient-to-r from-primary-500 to-secondary-500 text-white mb-2">
                        <Icon className="h-6 w-6" />
                      </div>
                      <div className="text-2xl font-bold text-slate-900 dark:text-slate-100">{stat.value}</div>
                      <div className="text-sm text-slate-600 dark:text-slate-400">{stat.label}</div>
                    </div>
                  );
                })}
              </div>
            </div>

            {/* Right Column - Illustration */}
            <div className="col-span-12 lg:col-span-6 animate-fade-in" style={{ animationDelay: '200ms' }}>
              <div className="relative">
                {/* Main Illustration */}
                <div className="relative bg-gradient-to-br from-white/80 to-slate-50/80 dark:from-slate-800/80 dark:to-slate-900/80 backdrop-blur-xl rounded-3xl p-8 shadow-2xl border border-white/20 dark:border-white/10">
                  <div className="grid grid-cols-3 gap-4">
                    <div className="space-y-4">
                      <div className="h-16 bg-gradient-to-r from-blue-400 to-purple-500 rounded-xl animate-float"></div>
                      <div className="h-12 bg-gradient-to-r from-purple-400 to-pink-500 rounded-xl animate-float" style={{ animationDelay: '1s' }}></div>
                      <div className="h-20 bg-gradient-to-r from-green-400 to-teal-500 rounded-xl animate-float" style={{ animationDelay: '2s' }}></div>
                    </div>
                    <div className="space-y-4 pt-8">
                      <div className="h-20 bg-gradient-to-r from-yellow-400 to-orange-500 rounded-xl animate-float" style={{ animationDelay: '0.5s' }}></div>
                      <div className="h-16 bg-gradient-to-r from-indigo-400 to-blue-500 rounded-xl animate-float" style={{ animationDelay: '1.5s' }}></div>
                      <div className="h-12 bg-gradient-to-r from-red-400 to-pink-500 rounded-xl animate-float" style={{ animationDelay: '2.5s' }}></div>
                    </div>
                    <div className="space-y-4 pt-4">
                      <div className="h-12 bg-gradient-to-r from-teal-400 to-green-500 rounded-xl animate-float" style={{ animationDelay: '0.8s' }}></div>
                      <div className="h-20 bg-gradient-to-r from-violet-400 to-purple-500 rounded-xl animate-float" style={{ animationDelay: '1.8s' }}></div>
                      <div className="h-16 bg-gradient-to-r from-emerald-400 to-teal-500 rounded-xl animate-float" style={{ animationDelay: '2.8s' }}></div>
                    </div>
                  </div>
                  
                  {/* Floating Elements */}
                  <div className="absolute -top-4 -right-4 w-12 h-12 bg-gradient-to-r from-primary-500 to-secondary-500 rounded-full animate-bounce shadow-lg"></div>
                  <div className="absolute -bottom-4 -left-4 w-8 h-8 bg-gradient-to-r from-accent-500 to-primary-500 rounded-full animate-bounce delay-200 shadow-lg"></div>
                  <div className="absolute top-1/2 -left-2 w-6 h-6 bg-gradient-to-r from-secondary-500 to-accent-500 rounded-full animate-pulse shadow-lg"></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-24 relative">
        <div className="max-w-1440 mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16 animate-fade-in">
            <div className="inline-flex items-center px-4 py-2 rounded-full bg-primary-100 dark:bg-primary-900/20 text-primary-700 dark:text-primary-300 text-sm font-medium mb-6">
              <Sparkles className="h-4 w-4 mr-2" />
              Powerful Features
            </div>
            <h2 className="text-4xl lg:text-5xl font-bold text-slate-900 dark:text-slate-100 mb-6">
              Modern Learning Experience
            </h2>
            <p className="text-xl text-slate-600 dark:text-slate-300 max-w-3xl mx-auto">
              Experience the future of education with AI-powered tools designed to enhance your learning journey.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {features.map((feature, index) => {
              const Icon = feature.icon;
              return (
                <Card 
                  key={index} 
                  variant="elevated" 
                  hover="lift"
                  className="text-center group animate-scale-in"
                  style={{ animationDelay: `${index * 200}ms` }}
                >
                  <CardHeader>
                    <div className={`mx-auto h-20 w-20 bg-gradient-to-r ${feature.gradient} rounded-2xl flex items-center justify-center mb-6 shadow-lg group-hover:scale-110 transition-transform duration-300`}>
                      <Icon className="h-10 w-10 text-white" />
                    </div>
                    <CardTitle className="text-2xl font-bold">
                      {feature.title}
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <CardDescription className="text-base leading-relaxed">
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
      <section className="py-24 relative overflow-hidden">
        {/* Background */}
        <div className="absolute inset-0 bg-gradient-to-r from-primary-600 via-primary-700 to-secondary-600"></div>
        <div className="absolute inset-0 bg-gradient-to-r from-primary-600/90 via-primary-700/90 to-secondary-600/90"></div>
        <div className="absolute top-0 left-1/4 w-96 h-96 bg-white/10 rounded-full blur-3xl animate-pulse-slow"></div>
        <div className="absolute bottom-0 right-1/4 w-96 h-96 bg-white/10 rounded-full blur-3xl animate-pulse-slow delay-1000"></div>
        
        <div className="relative max-w-1440 mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <div className="space-y-8 animate-fade-in">
            <h2 className="text-4xl lg:text-6xl font-bold text-white">
              Ready to Transform Your Learning?
            </h2>
            <p className="text-xl text-primary-100 max-w-3xl mx-auto leading-relaxed">
              Join thousands of learners who are already using AI to accelerate their education and achieve their goals faster than ever.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link to="/register">
                <Button variant="secondary" size="xl" className="w-full sm:w-auto group shadow-2xl">
                  Get Started Free
                  <ArrowRight className="ml-2 h-5 w-5 group-hover:translate-x-1 transition-transform" />
                </Button>
              </Link>
              <Link to="/login">
                <Button variant="glass" size="xl" className="w-full sm:w-auto text-white border-white/20 hover:bg-white/20">
                  Sign In
                </Button>
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gradient-to-r from-slate-900 via-slate-800 to-slate-900 text-white py-16">
        <div className="max-w-1440 mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            {/* Logo and Description */}
            <div className="col-span-1 md:col-span-2">
              <div className="flex items-center space-x-3 mb-4">
                <div className="relative">
                  <div className="absolute inset-0 bg-gradient-to-r from-primary-600 to-secondary-600 rounded-lg blur-sm opacity-75"></div>
                  <BookOpen className="relative h-8 w-8 text-white" />
                </div>
                <span className="text-2xl font-bold">AI Learning Platform</span>
              </div>
              <p className="text-slate-400 max-w-md leading-relaxed">
                Empowering learners worldwide with AI-driven education tools and personalized learning experiences.
              </p>
            </div>
            
            {/* Links */}
            <div className="space-y-4">
              <h3 className="text-lg font-semibold text-white">Product</h3>
              <div className="space-y-2">
                <a href="#" className="block text-slate-400 hover:text-white transition-colors">Features</a>
                <a href="#" className="block text-slate-400 hover:text-white transition-colors">Pricing</a>
                <a href="#" className="block text-slate-400 hover:text-white transition-colors">API</a>
              </div>
            </div>
            
            <div className="space-y-4">
              <h3 className="text-lg font-semibold text-white">Support</h3>
              <div className="space-y-2">
                <a href="#" className="block text-slate-400 hover:text-white transition-colors">Help Center</a>
                <a href="#" className="block text-slate-400 hover:text-white transition-colors">Contact Us</a>
                <a href="#" className="block text-slate-400 hover:text-white transition-colors">Privacy Policy</a>
                <a href="#" className="block text-slate-400 hover:text-white transition-colors">Terms of Service</a>
              </div>
            </div>
          </div>
          
          <div className="mt-12 pt-8 border-t border-slate-700 flex flex-col md:flex-row justify-between items-center">
            <p className="text-slate-400 text-center md:text-left">
              &copy; 2024 AI Learning Platform. All rights reserved.
            </p>
            <div className="flex space-x-6 mt-4 md:mt-0">
              <a href="#" className="text-slate-400 hover:text-white transition-colors">
                <span className="sr-only">Twitter</span>
                <svg className="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M6.29 18.251c7.547 0 11.675-6.253 11.675-11.675 0-.178 0-.355-.012-.53A8.348 8.348 0 0020 3.92a8.19 8.19 0 01-2.357.646 4.118 4.118 0 001.804-2.27 8.224 8.224 0 01-2.605.996 4.107 4.107 0 00-6.993 3.743 11.65 11.65 0 01-8.457-4.287 4.106 4.106 0 001.27 5.477A4.073 4.073 0 01.8 7.713v.052a4.105 4.105 0 003.292 4.022 4.095 4.095 0 01-1.853.07 4.108 4.108 0 003.834 2.85A8.233 8.233 0 010 16.407a11.616 11.616 0 006.29 1.84" />
                </svg>
              </a>
              <a href="#" className="text-slate-400 hover:text-white transition-colors">
                <span className="sr-only">GitHub</span>
                <svg className="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 0C4.477 0 0 4.484 0 10.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0110 4.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.203 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.942.359.31.678.921.678 1.856 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0020 10.017C20 4.484 15.522 0 10 0z" clipRule="evenodd" />
                </svg>
              </a>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}
