# SmartSkale LMS Frontend

React TypeScript frontend for SmartSkale Learning Management System.

## Setup

### Prerequisites

- Node.js 18+
- npm or yarn

### Installation

```bash
npm install
```

### Running the Application

```bash
npm run dev
```

Server will start at `http://localhost:5173`

### Building for Production

```bash
npm run build
```

### Project Structure

```
src/
├── assets/          # Static assets
├── components/      # Reusable components
├── layouts/         # Layout components
├── pages/           # Page components
├── hooks/           # Custom hooks
├── services/        # API services
├── store/           # Zustand stores
├── types/           # TypeScript types
├── utils/           # Utility functions
├── App.tsx          # App component
├── main.tsx         # Entry point
└── index.css        # Global styles
```

## Technology Stack

- **React 18**: UI library
- **TypeScript**: Type safety
- **Vite**: Build tool and dev server
- **TailwindCSS**: Utility-first CSS
- **React Router**: Client-side routing
- **Axios**: HTTP client
- **React Query**: Server state management
- **Zustand**: Client state management

## Features

- Responsive design
- Dark/Light mode ready
- API integration
- Health check monitoring
- Clean component architecture

## Development

### Type Checking

```bash
npm run type-check
```

### Linting

```bash
npm run lint
```
