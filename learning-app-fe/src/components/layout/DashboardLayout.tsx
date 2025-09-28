import React, { useState } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { 
  BookOpen, 
  Upload, 
  MessageCircle, 
  Brain, 
  TrendingUp, 
  User, 
  Settings, 
  LogOut,
  Menu,
  X,
  Shield
} from 'lucide-react';
import { useAuthStore } from '@/stores/authStore';
import { Button } from '@/components/ui/Button';
import { ThemeToggle } from '@/components/ui/ThemeToggle';
import { LanguageToggle } from '@/components/ui/LanguageToggle';

interface DashboardLayoutProps {
  children: React.ReactNode;
}

export function DashboardLayout({ children }: DashboardLayoutProps) {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const location = useLocation();
  const navigate = useNavigate();
  const { user, logout } = useAuthStore();
  const { t } = useTranslation();

  const navigation = [
    { name: t('navigation.dashboard'), href: '/dashboard', icon: TrendingUp },
    { name: t('navigation.courses'), href: '/courses', icon: BookOpen },
    { name: t('navigation.uploads'), href: '/uploads', icon: Upload },
    { name: t('navigation.chat'), href: '/chat', icon: MessageCircle },
    { name: t('navigation.quiz'), href: '/quiz', icon: Brain },
    { name: t('navigation.progress'), href: '/progress', icon: TrendingUp },
  ];

  // Add admin link for admin users
  if (user?.role === 'admin') {
    navigation.push({ name: t('navigation.admin'), href: '/admin', icon: Shield });
  }

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  const isActive = (href: string) => {
    return location.pathname === href || location.pathname.startsWith(href + '/');
  };

  return (
    <div className="flex h-screen bg-gray-50">
      {/* Mobile sidebar overlay */}
      {sidebarOpen && (
        <div 
          className="fixed inset-0 z-40 bg-gray-600 bg-opacity-75 lg:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      {/* Sidebar */}
      <div className={`
        fixed inset-y-0 left-0 z-50 w-64 bg-white/80 dark:bg-slate-800/80 backdrop-blur-xl shadow-2xl border-r border-white/20 dark:border-white/10 transform transition-transform duration-300 ease-in-out lg:translate-x-0 lg:static lg:inset-0
        ${sidebarOpen ? 'translate-x-0' : '-translate-x-full'}
      `}>
        <div className="flex flex-col h-full">
          {/* Logo */}
          <div className="flex items-center justify-between h-16 px-6 border-b border-slate-200/50 dark:border-slate-700/50">
            <Link to="/dashboard" className="flex items-center space-x-3 group">
              <div className="relative">
                <div className="absolute inset-0 bg-gradient-to-r from-primary-600 to-secondary-600 rounded-lg blur-sm opacity-75 group-hover:opacity-100 transition-opacity"></div>
                <Brain className="relative h-8 w-8 text-white" />
              </div>
              <span className="text-xl font-bold gradient-text">AI Learning</span>
            </Link>
            <button
              onClick={() => setSidebarOpen(false)}
              className="lg:hidden rounded-md p-2 text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 hover:text-gray-600 dark:hover:text-gray-300"
            >
              <X className="h-5 w-5" />
            </button>
          </div>

          {/* Navigation */}
          <nav className="flex-1 px-4 py-6 space-y-2">
            {navigation.map((item) => {
              const Icon = item.icon;
              const active = isActive(item.href);
              
              return (
                <Link
                  key={item.name}
                  to={item.href}
                    className={`
                      group flex items-center px-3 py-3 rounded-xl text-sm font-medium transition-all duration-200 relative
                      ${active 
                        ? 'bg-gradient-to-r from-primary-50 to-primary-100 dark:from-primary-900/20 dark:to-primary-800/20 text-primary-700 dark:text-primary-300 shadow-lg border border-primary-200 dark:border-primary-700' 
                        : 'text-slate-700 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-700 hover:text-slate-900 dark:hover:text-white hover:shadow-md'
                      }
                    `}
                  onClick={() => setSidebarOpen(false)}
                >
                  {active && (
                    <div className="absolute left-0 top-1/2 -translate-y-1/2 w-1 h-8 bg-gradient-to-b from-primary-500 to-secondary-500 rounded-r-full"></div>
                  )}
                  <Icon className={`mr-3 h-5 w-5 transition-transform group-hover:scale-110 ${active ? 'text-primary-600 dark:text-primary-400' : ''}`} />
                  {item.name}
                </Link>
              );
            })}
          </nav>

          {/* User menu */}
          <div className="border-t border-gray-200 dark:border-gray-700 p-4">
            <div className="flex items-center space-x-3 mb-4">
              <div className="h-10 w-10 rounded-full bg-primary-100 dark:bg-primary-900/20 flex items-center justify-center">
                <User className="h-6 w-6 text-primary-600 dark:text-primary-400" />
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium text-gray-900 dark:text-white truncate">
                  {user?.name}
                </p>
                <p className="text-xs text-gray-500 dark:text-gray-400 capitalize">
                  {user?.role}
                </p>
              </div>
            </div>
            
            {/* Theme and Language toggles */}
            <div className="mb-4 space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Theme</span>
                <ThemeToggle />
              </div>
              <div className="flex items-center justify-between">
                <span className="text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Language</span>
                <LanguageToggle />
              </div>
            </div>
            
            <div className="space-y-2">
              <Link
                to="/profile"
                className="flex items-center w-full px-3 py-2 text-sm text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700"
                onClick={() => setSidebarOpen(false)}
              >
                <Settings className="mr-3 h-4 w-4" />
                {t('navigation.settings')}
              </Link>
              <button
                onClick={handleLogout}
                className="flex items-center w-full px-3 py-2 text-sm text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700"
              >
                <LogOut className="mr-3 h-4 w-4" />
                {t('auth.logout')}
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Main content */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Top bar */}
        <header className="bg-white dark:bg-gray-800 shadow-sm border-b border-gray-200 dark:border-gray-700 lg:hidden">
          <div className="flex items-center justify-between h-16 px-4">
            <button
              onClick={() => setSidebarOpen(true)}
              className="rounded-md p-2 text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 hover:text-gray-600 dark:hover:text-gray-300"
            >
              <Menu className="h-6 w-6" />
            </button>
            
            <Link to="/dashboard" className="flex items-center space-x-2">
              <Brain className="h-6 w-6 text-primary-600" />
              <span className="text-lg font-bold text-gray-900 dark:text-white">AI Learning</span>
            </Link>
            
            <div className="w-10" /> {/* Spacer */}
          </div>
        </header>

        {/* Page content */}
        <main className="flex-1 overflow-y-auto bg-gray-50 dark:bg-gray-900">
          {children}
        </main>
      </div>
    </div>
  );
}
