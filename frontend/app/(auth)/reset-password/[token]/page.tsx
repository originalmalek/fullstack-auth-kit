'use client';

import { useEffect } from 'react';
import { useRouter, useParams } from 'next/navigation';
import { ResetPasswordForm } from '@/components/auth/reset-password-form';
import { useAuthStore } from '@/lib/stores/auth-store';

export default function ResetPasswordPage() {
  const router = useRouter();
  const { isAuthenticated, isLoading } = useAuthStore();
  const params = useParams();
  const token = (params?.token as string) || null;

  useEffect(() => {
    if (!isLoading && isAuthenticated) {
      router.replace('/settings');
    }
  }, [isAuthenticated, isLoading, router]);

  // Show loading or redirect for authenticated users
  if (isLoading || isAuthenticated || !token) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-900">
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary mx-auto"></div>
          <p className="mt-2 text-sm text-gray-600 dark:text-gray-400">Loading...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-900 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <ResetPasswordForm token={token} />
      </div>
    </div>
  );
}
