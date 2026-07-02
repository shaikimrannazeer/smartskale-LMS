/**
 * Auth layout component
 */
export const AuthLayout = ({ children }: { children: React.ReactNode }) => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-600 to-blue-800 flex items-center justify-center px-4">
      <div className="w-full max-w-md">
        <div className="bg-white rounded-lg shadow-xl p-8">
          <div className="text-center mb-8">
            <h1 className="text-3xl font-bold text-gray-900 mb-2">SmartSkale LMS</h1>
            <p className="text-gray-600">AI Powered Learning Management Platform</p>
          </div>
          {children}
        </div>
      </div>
    </div>
  );
};
