import React from 'react';
import { cn } from '@/lib/utils';

interface ModernLoaderProps {
  size?: 'sm' | 'md' | 'lg' | 'xl';
  variant?: 'spinner' | 'dots' | 'pulse' | 'bars' | 'grid';
  className?: string;
}

const sizeClasses = {
  sm: 'h-4 w-4',
  md: 'h-6 w-6',
  lg: 'h-8 w-8',
  xl: 'h-12 w-12',
};

export function ModernLoader({ size = 'md', variant = 'spinner', className }: ModernLoaderProps) {
  const baseClasses = sizeClasses[size];

  if (variant === 'spinner') {
    return (
      <div className={cn('relative', className)}>
        <div className={cn(
          'animate-spin rounded-full border-2 border-transparent',
          'border-t-primary-600 border-r-primary-600',
          baseClasses
        )} />
      </div>
    );
  }

  if (variant === 'dots') {
    return (
      <div className={cn('flex space-x-1', className)}>
        {[0, 1, 2].map((i) => (
          <div
            key={i}
            className={cn(
              'rounded-full bg-primary-600 animate-pulse',
              size === 'sm' ? 'h-1 w-1' : size === 'md' ? 'h-2 w-2' : size === 'lg' ? 'h-3 w-3' : 'h-4 w-4'
            )}
            style={{
              animationDelay: `${i * 0.2}s`,
              animationDuration: '1s',
            }}
          />
        ))}
      </div>
    );
  }

  if (variant === 'pulse') {
    return (
      <div className={cn(
        'rounded-full bg-gradient-to-r from-primary-500 to-secondary-500 animate-pulse',
        baseClasses,
        className
      )} />
    );
  }

  if (variant === 'bars') {
    return (
      <div className={cn('flex space-x-1 items-end', className)}>
        {[0, 1, 2, 3].map((i) => (
          <div
            key={i}
            className={cn(
              'bg-gradient-to-t from-primary-600 to-secondary-500 rounded-sm animate-pulse',
              size === 'sm' ? 'h-3 w-1' : size === 'md' ? 'h-4 w-1' : size === 'lg' ? 'h-6 w-1' : 'h-8 w-2'
            )}
            style={{
              animationDelay: `${i * 0.1}s`,
              animationDuration: '0.8s',
            }}
          />
        ))}
      </div>
    );
  }

  if (variant === 'grid') {
    return (
      <div className={cn('grid grid-cols-3 gap-1', className)}>
        {[0, 1, 2, 3, 4, 5, 6, 7, 8].map((i) => (
          <div
            key={i}
            className={cn(
              'bg-gradient-to-r from-primary-500 to-secondary-500 rounded-sm animate-pulse',
              size === 'sm' ? 'h-1 w-1' : size === 'md' ? 'h-2 w-2' : size === 'lg' ? 'h-3 w-3' : 'h-4 w-4'
            )}
            style={{
              animationDelay: `${i * 0.1}s`,
              animationDuration: '1.2s',
            }}
          />
        ))}
      </div>
    );
  }

  return null;
}

// Shimmer Loading Component
interface ShimmerLoaderProps {
  className?: string;
  lines?: number;
}

export function ShimmerLoader({ className, lines = 3 }: ShimmerLoaderProps) {
  return (
    <div className={cn('animate-pulse space-y-4', className)}>
      {Array.from({ length: lines }).map((_, i) => (
        <div key={i} className="space-y-2">
          <div className={cn(
            'bg-gradient-to-r from-slate-200 to-slate-300 dark:from-slate-700 dark:to-slate-600 rounded h-4',
            i === lines - 1 ? 'w-3/4' : 'w-full'
          )} />
        </div>
      ))}
    </div>
  );
}

// Skeleton Component
interface SkeletonProps {
  className?: string;
  variant?: 'text' | 'rectangular' | 'circular';
}

export function Skeleton({ className, variant = 'text' }: SkeletonProps) {
  const baseClasses = 'animate-pulse bg-gradient-to-r from-slate-200 to-slate-300 dark:from-slate-700 dark:to-slate-600';
  
  if (variant === 'circular') {
    return (
      <div className={cn('rounded-full', baseClasses, className)} />
    );
  }
  
  if (variant === 'rectangular') {
    return (
      <div className={cn('rounded-lg', baseClasses, className)} />
    );
  }
  
  return (
    <div className={cn('rounded', baseClasses, className)} />
  );
}
