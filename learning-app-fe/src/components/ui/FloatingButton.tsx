import React from 'react';
import { motion } from 'framer-motion';
import { Button, ButtonProps } from './Button';

interface FloatingButtonProps extends ButtonProps {
  children: React.ReactNode;
}

export function FloatingButton({ children, className, ...props }: FloatingButtonProps) {
  return (
    <motion.div
      whileHover={{ 
        scale: 1.05,
        boxShadow: '0 10px 25px rgba(0, 0, 0, 0.15)',
      }}
      whileTap={{ 
        scale: 0.95,
      }}
      transition={{
        type: 'spring',
        stiffness: 300,
        damping: 20,
      }}
    >
      <Button
        className={`shadow-lg hover:shadow-xl transition-shadow duration-200 ${className}`}
        {...props}
      >
        {children}
      </Button>
    </motion.div>
  );
}
