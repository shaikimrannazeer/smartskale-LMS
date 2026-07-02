/**
 * Home page
 */
import { useNavigate } from 'react-router-dom';
import { DefaultLayout } from '../layouts/DefaultLayout';
import { useHealthCheck } from '../hooks/useHealthCheck';

export const HomePage = () => {
  const navigate = useNavigate();
  const { data: health, isLoading } = useHealthCheck();

  return (
    <DefaultLayout>
      <div className="min-h-screen flex flex-col items-center justify-center text-center">
        <div className="space-y-8">
          <div>
            <h1 className="text-6xl font-bold text-gray-900 mb-4">
              SmartSkale LMS
            </h1>
            <p className="text-2xl text-gray-600 mb-8">
              AI Powered Learning Management Platform
            </p>
          </div>

          {/* API Status */}
          <div className="bg-white p-6 rounded-lg shadow-md max-w-md mx-auto">
            {isLoading ? (
              <div className="flex items-center justify-center gap-2">
                <div className="w-3 h-3 bg-blue-500 rounded-full animate-pulse"></div>
                <span className="text-gray-600">Checking API status...</span>
              </div>
            ) : health ? (
              <div className="space-y-2">
                <div className="flex items-center justify-center gap-2">
                  <div className="w-3 h-3 bg-green-500 rounded-full"></div>
                  <span className="text-green-600 font-semibold">API Status: Healthy</span>
                </div>
                <p className="text-sm text-gray-600">{health.application}</p>
                <p className="text-xs text-gray-500">Version: {health.version}</p>
              </div>
            ) : (
              <div className="flex items-center justify-center gap-2">
                <div className="w-3 h-3 bg-red-500 rounded-full"></div>
                <span className="text-red-600 font-semibold">API Status: Offline</span>
              </div>
            )}
          </div>

          {/* Call to Action */}
          <button
            onClick={() => navigate('/dashboard')}
            className="bg-gradient-to-r from-blue-600 to-blue-800 text-white px-8 py-3 rounded-lg font-semibold hover:from-blue-700 hover:to-blue-900 transition-all transform hover:scale-105"
          >
            Get Started
          </button>
        </div>
      </div>
    </DefaultLayout>
  );
};
