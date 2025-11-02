# E-Commerce Frontend

Modern React application built with Vite, Tailwind CSS, and industry-standard libraries.

## ��� Tech Stack

- **React 18** - UI library
- **Vite** - Build tool and dev server
- **Tailwind CSS 3** - Utility-first CSS framework
- **React Router** - Client-side routing
- **Zustand** - State management
- **React Query** - Server state management
- **Axios** - HTTP client
- **Lucide React** - Icon library

## ��� Installation

```bash
# Install dependencies
npm install
```

## ���️ Development

```bash
# Start dev server (with hot reload)
npm run dev

# Access at: http://localhost:5173
```

## ���️ Build for Production

```bash
# Build optimized production bundle
npm run build

# Preview production build
npm run preview
```

## �� Project Structure

```
src/
├── api/              # API client and endpoints
│   └── client.js    # Axios instance with interceptors
├── components/      # Reusable components
│   ├── common/     # Buttons, inputs, cards
│   ├── layout/     # Header, footer, sidebar
│   └── features/   # Feature-specific components
├── pages/          # Route pages
│   └── Home/       # Home page
├── hooks/          # Custom React hooks
├── store/          # Zustand state management
│   └── cartStore.js # Shopping cart state
├── utils/          # Utility functions
├── styles/         # Global styles
└── App.jsx         # Main app component
```

## ��� API Integration

The frontend connects to the BFF (Backend for Frontend) service:

```javascript
// Default: http://localhost:3001/api
// Configure in .env file:
VITE_BFF_URL=http://localhost:3001/api
```

## ��� Styling

Using Tailwind CSS utility classes:

```jsx
<button className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
  Click Me
</button>
```

## ��� Testing

```bash
# Run tests
npm test

# Run tests with UI
npm run test:ui

# Run tests with coverage
npm run test:coverage
```

## ��� Environment Variables

Create a `.env` file:

```bash
VITE_BFF_URL=http://localhost:3001/api
VITE_APP_NAME=E-Commerce Platform
VITE_ENVIRONMENT=development
```

## ��� Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Lint code
- `npm test` - Run tests

## ��� Features Implemented

- ✅ Home page with hero section
- ✅ Feature cards
- ✅ Shopping cart state management
- ✅ API client with interceptors
- ✅ Correlation ID for distributed tracing
- ✅ Authentication token handling
- ✅ Responsive design

## ��� Coming Soon

- Products listing page
- Product detail page
- Shopping cart page
- Checkout flow
- User authentication
- Order history

## ��� Documentation

- [React Documentation](https://react.dev)
- [Vite Documentation](https://vitejs.dev)
- [Tailwind CSS](https://tailwindcss.com)
- [React Router](https://reactrouter.com)

## ��� Troubleshooting

### Port already in use

```bash
# Kill process on port 5173
npx kill-port 5173
```

### Dependencies issues

```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

## ��� Contributing

1. Create feature branch
2. Make changes
3. Run tests
4. Submit pull request

---
