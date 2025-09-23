import React, { useState, useEffect, useCallback } from 'react';
import { Clock, AlertTriangle } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

interface QuizTimerProps {
  duration: number; // in seconds
  onTimeUp: () => void;
  isActive: boolean;
  className?: string;
}

export function QuizTimer({ duration, onTimeUp, isActive, className }: QuizTimerProps) {
  const [timeLeft, setTimeLeft] = useState(duration);
  const [isWarning, setIsWarning] = useState(false);
  const [isCritical, setIsCritical] = useState(false);

  const formatTime = useCallback((seconds: number) => {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;
    
    if (hours > 0) {
      return `${hours}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    }
    return `${minutes}:${secs.toString().padStart(2, '0')}`;
  }, []);

  const getProgressPercentage = useCallback(() => {
    return ((duration - timeLeft) / duration) * 100;
  }, [duration, timeLeft]);

  const getProgressColor = useCallback(() => {
    if (isCritical) return 'text-red-600';
    if (isWarning) return 'text-yellow-600';
    return 'text-primary-600';
  }, [isWarning, isCritical]);

  const getBackgroundColor = useCallback(() => {
    if (isCritical) return 'from-red-500 to-red-600';
    if (isWarning) return 'from-yellow-500 to-yellow-600';
    return 'from-primary-500 to-primary-600';
  }, [isWarning, isCritical]);

  useEffect(() => {
    if (!isActive) return;

    const timer = setInterval(() => {
      setTimeLeft((prev) => {
        if (prev <= 1) {
          onTimeUp();
          return 0;
        }
        return prev - 1;
      });
    }, 1000);

    return () => clearInterval(timer);
  }, [isActive, onTimeUp]);

  useEffect(() => {
    const percentage = (timeLeft / duration) * 100;
    setIsWarning(percentage <= 25 && percentage > 10);
    setIsCritical(percentage <= 10);
  }, [timeLeft, duration]);

  if (!isActive) return null;

  return (
    <div className={`flex items-center gap-3 ${className}`}>
      {/* Timer Display */}
      <div className={`flex items-center gap-2 px-3 py-2 rounded-lg bg-white dark:bg-gray-800 border-2 transition-colors ${
        isCritical ? 'border-red-200 dark:border-red-800' :
        isWarning ? 'border-yellow-200 dark:border-yellow-800' :
        'border-gray-200 dark:border-gray-700'
      }`}>
        <Clock className={`h-4 w-4 ${getProgressColor()}`} />
        <span className={`font-mono text-sm font-semibold ${getProgressColor()}`}>
          {formatTime(timeLeft)}
        </span>
        
        {/* Warning Icon */}
        <AnimatePresence>
          {(isWarning || isCritical) && (
            <motion.div
              initial={{ scale: 0, rotate: -180 }}
              animate={{ scale: 1, rotate: 0 }}
              exit={{ scale: 0, rotate: 180 }}
              transition={{ duration: 0.3 }}
            >
              <AlertTriangle className={`h-4 w-4 ${
                isCritical ? 'text-red-600' : 'text-yellow-600'
              }`} />
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      {/* Progress Bar */}
      <div className="flex-1 h-2 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
        <motion.div
          className={`h-full bg-gradient-to-r ${getBackgroundColor()}`}
          initial={{ width: 0 }}
          animate={{ width: `${getProgressPercentage()}%` }}
          transition={{ duration: 0.5, ease: "easeOut" }}
        />
      </div>

      {/* Percentage */}
      <div className={`text-xs font-medium ${getProgressColor()}`}>
        {Math.round((timeLeft / duration) * 100)}%
      </div>
      
      {/* Pulsing Effect for Critical Time */}
      <AnimatePresence>
        {isCritical && (
          <motion.div
            className="absolute inset-0 bg-red-500 opacity-10 rounded-lg pointer-events-none"
            animate={{ opacity: [0.1, 0.3, 0.1] }}
            transition={{ duration: 1, repeat: Infinity }}
          />
        )}
      </AnimatePresence>
    </div>
  );
}

export default QuizTimer;
