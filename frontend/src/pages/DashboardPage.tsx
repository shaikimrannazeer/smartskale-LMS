/**
 * Dashboard page
 */
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { DefaultLayout } from '../layouts/DefaultLayout';
import { useAuthStore } from '../store/authStore';
import { authService } from '../services/auth';

export const DashboardPage = () => {
  const navigate = useNavigate();
  const { user, logout } = useAuthStore();
  const [isLoading, setIsLoading] = useState(false);

  const handleLogout = async () => {
    setIsLoading(true);
    try {
      await authService.logout();
      logout();
      navigate('/login');
    } catch (error) {
      console.error('Logout failed:', error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <DefaultLayout>
      <div className="max-w-4xl mx-auto">
        <div className="bg-white rounded-lg shadow-md p-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            Welcome, {user?.full_name}!
          </h1>
          <p className="text-gray-600 mb-8">
            You are logged in as a <span className="font-semibold capitalize">{user?.role}</span>
          </p>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
            <div className="bg-gradient-to-br from-blue-50 to-blue-100 p-6 rounded-lg">
              <h3 className="text-sm font-semibold text-gray-600 mb-2">Email</h3>
              <p className="text-lg text-gray-900">{user?.email}</p>
            </div>
            <div className="bg-gradient-to-br from-green-50 to-green-100 p-6 rounded-lg">
              <h3 className="text-sm font-semibold text-gray-600 mb-2">Role</h3>
              <p className="text-lg text-gray-900 capitalize">{user?.role}</p>
            </div>
            <div className="bg-gradient-to-br from-purple-50 to-purple-100 p-6 rounded-lg">
              <h3 className="text-sm font-semibold text-gray-600 mb-2">Status</h3>
              <p className="text-lg text-gray-900">
                {user?.is_active ? (
                  <span className="text-green-600 font-semibold">✓ Active</span>
                ) : (
                  <span className="text-red-600 font-semibold">✗ Inactive</span>
                )}
              </p>
            </div>
          </div>

          <div className="border-t pt-6">
            <button
              onClick={handleLogout}
              disabled={isLoading}
              className="bg-red-600 hover:bg-red-700 text-white px-6 py-2 rounded-lg font-semibold transition disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isLoading ? 'Logging out...' : 'Logout'}
            </button>
          </div>
        </div>
      </div>
    </DefaultLayout>
  );
};
