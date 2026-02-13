# College Baseball Stats - Frontend

React frontend for the College Baseball Statistics application.

## Tech Stack

- **React 18** - UI library
- **TypeScript** - Type safety
- **Vite** - Build tool and dev server
- **React Router** - Client-side routing
- **Axios** - HTTP client

## Development

### Prerequisites

- Node.js 18+ and npm
- Backend API running on `http://localhost:8000`

### Setup

```bash
# Install dependencies
npm install

# Copy environment file
cp .env.example .env

# Start development server
npm run dev
```

The frontend will be available at `http://localhost:5173`.

### Available Scripts

- `npm run dev` - Start development server with hot reload
- `npm run build` - Build production bundle
- `npm run preview` - Preview production build locally
- `npm run lint` - Run ESLint

## Project Structure

```
frontend/
├── src/
│   ├── components/        # Reusable UI components
│   │   ├── Navbar.tsx
│   │   └── StatBar.tsx    # Percentile visualization
│   ├── pages/             # Route components
│   │   ├── Home.tsx
│   │   ├── IndividualBatting.tsx
│   │   ├── IndividualPitching.tsx
│   │   ├── TeamBatting.tsx
│   │   └── TeamPitching.tsx
│   ├── api.ts             # API client and types
│   ├── App.tsx            # Main app component with routes
│   ├── main.tsx           # Entry point
│   └── index.css          # Global styles
├── public/                # Static assets
├── index.html             # HTML template
├── vite.config.ts         # Vite configuration
└── package.json           # Dependencies and scripts
```

## Features

### Individual Player Views

- Select team and player from dropdowns
- Toggle between standard and advanced statistics
- Visual percentile bars with color gradient
- Real-time data fetching from API

### Team Views

- View all batters/pitchers for a team
- Filter by minimum playing time (PA/IP)
- Sort by performance
- Compact stat display showing top 5 metrics

### API Integration

The frontend communicates with the FastAPI backend through a clean API layer (`api.ts`):

- `GET /api/teams` - List all teams
- `GET /api/teams/{team}/roster` - Get team roster
- `GET /api/players/{player}/batting` - Get batting stats
- `GET /api/players/{player}/pitching` - Get pitching stats

## Configuration

Environment variables (`.env`):

```
VITE_API_URL=http://localhost:8000  # Backend API URL
```

## Production Build

```bash
# Build for production
npm run build

# Output will be in dist/ directory
# Serve with any static file server
npx serve -s dist
```

The production build can be hosted on:
- Netlify
- Vercel
- GitHub Pages
- Any static hosting service

## Deployment

### Static Hosting

```bash
# Build
npm run build

# Deploy dist/ folder to your hosting service
```

### With Backend

If deploying with the FastAPI backend:

1. Update `VITE_API_URL` to your production API URL
2. Build the frontend
3. Serve `dist/` folder via your backend or CDN
4. Configure CORS on the backend for your frontend domain

## Development Notes

- Vite proxies `/api` requests to `http://localhost:8000` during development
- Type definitions match the backend Pydantic schemas
- All percentiles are pre-calculated by the backend
- Color gradient: blue (0%) → purple (50%) → red (100%)
