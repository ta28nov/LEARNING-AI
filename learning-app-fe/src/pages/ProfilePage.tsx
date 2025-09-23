import React from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { useAuthStore } from '@/stores/authStore';
import { User, Mail, Lock } from 'lucide-react';

export function ProfilePage() {
  const { user } = useAuthStore();

  return (
    <div className="p-6 space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Profile Settings</h1>
        <p className="text-gray-600">Manage your account settings and preferences</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Personal Information</CardTitle>
            <CardDescription>Update your personal details</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <Input
              label="Full Name"
              defaultValue={user?.name}
              icon={<User className="h-4 w-4" />}
            />
            <Input
              label="Email"
              defaultValue={user?.email}
              icon={<Mail className="h-4 w-4" />}
              disabled
            />
            <Button>Update Profile</Button>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Change Password</CardTitle>
            <CardDescription>Update your account password</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <Input
              label="Current Password"
              type="password"
              icon={<Lock className="h-4 w-4" />}
            />
            <Input
              label="New Password"
              type="password"
              icon={<Lock className="h-4 w-4" />}
            />
            <Input
              label="Confirm New Password"
              type="password"
              icon={<Lock className="h-4 w-4" />}
            />
            <Button>Change Password</Button>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
