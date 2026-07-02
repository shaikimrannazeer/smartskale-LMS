/**
 * Sidebar component
 */
import { Link } from 'react-router-dom';
import { useAppStore } from '../store/appStore';

export const Sidebar = () => {
  const isSidebarOpen = useAppStore((state) => state.isSidebarOpen);

  return (
    <aside
      className={`bg-gray-900 text-white transition-all duration-300 ${
        isSidebarOpen ? 'w-64' : 'w-0'
      } overflow-hidden`}
    >
      <div className="p-6">
        <nav className="space-y-4">
          <Link
            to="/"
            className="block px-4 py-2 rounded hover:bg-gray-800 transition-colors"
          >
            Home
          </Link>
          {/* Additional navigation items will be added in future modules */}
        </nav>
      </div>
    </aside>
  );
};
