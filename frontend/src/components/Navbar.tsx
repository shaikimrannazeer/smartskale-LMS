/**
 * Navbar component
 */
import { Link } from 'react-router-dom';
import { useAppStore } from '../store/appStore';

export const Navbar = () => {
  const toggleSidebar = useAppStore((state) => state.toggleSidebar);

  return (
    <nav className="bg-gradient-to-r from-blue-600 to-blue-800 text-white shadow-lg">
      <div className="px-6 py-4 flex items-center justify-between">
        <div className="flex items-center gap-4">
          <button
            onClick={toggleSidebar}
            className="p-2 hover:bg-blue-700 rounded-lg transition-colors"
            aria-label="Toggle sidebar"
          >
            <svg
              className="w-6 h-6"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M4 6h16M4 12h16M4 18h16"
              />
            </svg>
          </button>
          <Link to="/" className="text-2xl font-bold hover:text-blue-200">
            SmartSkale LMS
          </Link>
        </div>
        <div className="flex items-center gap-4">
          <span className="text-sm opacity-75">v1.0.0</span>
        </div>
      </div>
    </nav>
  );
};
