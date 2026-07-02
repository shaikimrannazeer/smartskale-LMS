/**
 * Footer component
 */
export const Footer = () => {
  return (
    <footer className="bg-gray-900 text-white border-t border-gray-800 mt-auto">
      <div className="max-w-7xl mx-auto px-6 py-8">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div>
            <h3 className="text-lg font-semibold mb-4">SmartSkale LMS</h3>
            <p className="text-gray-400 text-sm">
              AI Powered Learning Management Platform
            </p>
          </div>
          <div>
            <h4 className="text-sm font-semibold mb-4 text-gray-300">Version</h4>
            <p className="text-gray-400 text-sm">1.0.0 - Module 1</p>
          </div>
          <div>
            <h4 className="text-sm font-semibold mb-4 text-gray-300">Status</h4>
            <p className="text-green-400 text-sm">● Operational</p>
          </div>
        </div>
        <div className="border-t border-gray-800 mt-8 pt-8 text-center text-gray-400 text-sm">
          <p>&copy; 2024 SmartSkale. All rights reserved.</p>
        </div>
      </div>
    </footer>
  );
};
