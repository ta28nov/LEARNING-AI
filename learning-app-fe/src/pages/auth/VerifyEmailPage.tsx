import React, { useState, useEffect } from 'react';
import { Link, useSearchParams, useNavigate } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { useTranslation } from 'react-i18next';
import { Mail, CheckCircle, RefreshCw } from 'lucide-react';
import toast from 'react-hot-toast';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card';
import { AnimatedPage } from '@/components/ui/AnimatedPage';
import { FadeIn } from '@/components/ui/FadeIn';
import { authService } from '@/services/authService';

const verifyEmailSchema = z.object({
  otp: z.string().length(6, 'OTP must be 6 digits'),
});

type VerifyEmailForm = z.infer<typeof verifyEmailSchema>;

export default function VerifyEmailPage() {
  const { t } = useTranslation();
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const [isLoading, setIsLoading] = useState(false);
  const [isResending, setIsResending] = useState(false);
  const [isVerified, setIsVerified] = useState(false);
  const [resendCooldown, setResendCooldown] = useState(0);

  const email = searchParams.get('email');

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<VerifyEmailForm>({
    resolver: zodResolver(verifyEmailSchema),
  });

  useEffect(() => {
    if (!email) {
      toast.error(t('auth.invalidVerificationLink'));
      navigate('/auth/register');
    }
  }, [email, navigate, t]);

  useEffect(() => {
    let timer: NodeJS.Timeout;
    if (resendCooldown > 0) {
      timer = setTimeout(() => setResendCooldown(resendCooldown - 1), 1000);
    }
    return () => clearTimeout(timer);
  }, [resendCooldown]);

  const onSubmit = async (data: VerifyEmailForm) => {
    if (!email) return;
    
    setIsLoading(true);
    try {
      await authService.verifyEmail({
        email,
        otp: data.otp,
      });
      setIsVerified(true);
      toast.success(t('auth.emailVerifiedSuccess'));
      
      // Redirect to login after 3 seconds
      setTimeout(() => {
        navigate('/auth/login');
      }, 3000);
    } catch (error) {
      toast.error(t('auth.invalidOTP'));
    } finally {
      setIsLoading(false);
    }
  };

  const handleResendOTP = async () => {
    if (!email || resendCooldown > 0) return;
    
    setIsResending(true);
    try {
      // Assuming we have a resend endpoint
      await authService.forgotPassword(email); // Reuse forgot password for now
      toast.success(t('auth.otpResent'));
      setResendCooldown(60); // 60 seconds cooldown
    } catch (error) {
      toast.error(t('errors.unexpectedError'));
    } finally {
      setIsResending(false);
    }
  };

  if (isVerified) {
    return (
      <AnimatedPage className="min-h-screen bg-gray-50 dark:bg-gray-900 flex items-center justify-center px-4">
        <FadeIn>
          <Card className="w-full max-w-md">
            <CardHeader className="text-center">
              <div className="mx-auto w-16 h-16 bg-green-100 dark:bg-green-900/20 rounded-full flex items-center justify-center mb-4">
                <CheckCircle className="h-8 w-8 text-green-600 dark:text-green-400" />
              </div>
              <CardTitle className="text-xl font-semibold">
                {t('auth.emailVerified')}
              </CardTitle>
            </CardHeader>
            <CardContent className="text-center space-y-4">
              <p className="text-gray-600 dark:text-gray-400">
                {t('auth.emailVerifiedDescription')}
              </p>
              <div className="pt-4">
                <Link to="/auth/login">
                  <Button className="w-full">
                    {t('auth.signIn')}
                  </Button>
                </Link>
              </div>
            </CardContent>
          </Card>
        </FadeIn>
      </AnimatedPage>
    );
  }

  return (
    <AnimatedPage className="min-h-screen bg-gray-50 dark:bg-gray-900 flex items-center justify-center px-4">
      <FadeIn>
        <Card className="w-full max-w-md">
          <CardHeader className="text-center">
            <div className="mx-auto w-16 h-16 bg-primary-100 dark:bg-primary-900/20 rounded-full flex items-center justify-center mb-4">
              <Mail className="h-8 w-8 text-primary-600 dark:text-primary-400" />
            </div>
            <CardTitle className="text-2xl font-bold">
              {t('auth.verifyEmail')}
            </CardTitle>
            <p className="text-gray-600 dark:text-gray-400 mt-2">
              {t('auth.verifyEmailDescription', { email })}
            </p>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
              <Input
                label={t('auth.verificationCode')}
                type="text"
                placeholder="123456"
                maxLength={6}
                className="text-center text-2xl tracking-widest"
                error={errors.otp?.message}
                {...register('otp')}
              />

              <Button
                type="submit"
                className="w-full"
                isLoading={isLoading}
                disabled={isLoading}
              >
                {isLoading ? t('common.loading') : t('auth.verifyEmail')}
              </Button>

              <div className="text-center space-y-2">
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  {t('auth.didntReceiveCode')}
                </p>
                <button
                  type="button"
                  onClick={handleResendOTP}
                  disabled={resendCooldown > 0 || isResending}
                  className="text-sm text-primary-600 dark:text-primary-400 hover:text-primary-500 dark:hover:text-primary-300 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-1"
                >
                  <RefreshCw className={`h-4 w-4 ${isResending ? 'animate-spin' : ''}`} />
                  {resendCooldown > 0 
                    ? t('auth.resendIn', { seconds: resendCooldown })
                    : t('auth.resendCode')
                  }
                </button>
              </div>

              <div className="text-center">
                <Link
                  to="/auth/register"
                  className="text-sm text-gray-600 dark:text-gray-400 hover:text-gray-800 dark:hover:text-gray-200"
                >
                  {t('auth.changeEmail')}
                </Link>
              </div>
            </form>
          </CardContent>
        </Card>
      </FadeIn>
    </AnimatedPage>
  );
}
