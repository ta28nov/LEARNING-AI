import React from 'react';
import { motion } from 'framer-motion';

interface PulseLoaderProps {
  size?: 'sm' | 'md' | 'lg';
  color?: string;
}

export function PulseLoader({ size = 'md', color = 'bg-primary-600' }: PulseLoaderProps) {
  const sizeClasses = {
    sm: 'w-2 h-2',
    md: 'w-3 h-3',
    lg: 'w-4 h-4',
  };

  const containerClass = {
    sm: 'gap-1',
    md: 'gap-2',
    lg: 'gap-3',
  };

  const pulseVariants = {
    initial: { scale: 0.8, opacity: 0.5 },
    animate: { scale: 1.2, opacity: 1 },
  };

  const transition = {
    duration: 0.6,
    repeat: Infinity,
    repeatType: 'reverse' as const,
    ease: 'easeInOut',
  };

  return (
    <div className={`flex items-center justify-center ${containerClass[size]}`}>
      {[0, 1, 2].map((index) => (
        <motion.div
          key={index}
          className={`rounded-full ${sizeClasses[size]} ${color}`}
          variants={pulseVariants}
          initial="initial"
          animate="animate"
          transition={{
            ...transition,
            delay: index * 0.2,
          }}
        />
      ))}
    </div>
  );
}
