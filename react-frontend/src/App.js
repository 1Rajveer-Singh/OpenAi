import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import { AppProvider } from './context/AppContext';
import ErrorBoundary from './components/ErrorBoundary';
import DemoBanner from './components/Layout/DemoBanner';
import Sidebar from './components/Layout/Sidebar';
import Header from './components/Layout/Header';
import { Dashboard, Inventory, Customers, Finance, Marketing, Reports, AIAgents, Settings } from './pages';
import VoiceInterface from './components/VoiceInterface/VoiceInterface';
import './styles/App.css';
import './styles/themes.css';

function App() {
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  const [theme, setTheme] = useState(localStorage.getItem('theme') || 'light');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Apply theme
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
  }, [theme]);

  useEffect(() => {
    // Simulate app initialization
    const timer = setTimeout(() => {
      setLoading(false);
    }, 2000);

    return () => clearTimeout(timer);
  }, []);

  const toggleSidebar = () => {
    setSidebarCollapsed(!sidebarCollapsed);
  };

  const toggleTheme = () => {
    setTheme(prevTheme => prevTheme === 'light' ? 'dark' : 'light');
  };

  if (loading) {
    return null; // Loading screen is handled by public/index.html
  }

  return (
    <ErrorBoundary>
      <AppProvider>
        <DemoBanner />
        <Router 
          future={{
            v7_startTransition: true,
            v7_relativeSplatPath: true
          }}
        >
          <div className={`app-container ${sidebarCollapsed ? 'sidebar-collapsed' : ''}`} data-theme={theme}>
            <Sidebar 
              collapsed={sidebarCollapsed} 
              onToggle={toggleSidebar}
            />
            
            <Header 
              onMenuToggle={toggleSidebar}
              onThemeToggle={toggleTheme}
              theme={theme}
            />
            
            <main className="main-content">
              <Routes>
                <Route path="/" element={<ErrorBoundary><Dashboard /></ErrorBoundary>} />
                <Route path="/dashboard" element={<ErrorBoundary><Dashboard /></ErrorBoundary>} />
                <Route path="/inventory" element={<ErrorBoundary><Inventory /></ErrorBoundary>} />
                <Route path="/customers" element={<ErrorBoundary><Customers /></ErrorBoundary>} />
                <Route path="/finance" element={<ErrorBoundary><Finance /></ErrorBoundary>} />
                <Route path="/marketing" element={<ErrorBoundary><Marketing /></ErrorBoundary>} />
                <Route path="/reports" element={<ErrorBoundary><Reports /></ErrorBoundary>} />
                <Route path="/ai-agents" element={<ErrorBoundary><AIAgents /></ErrorBoundary>} />
                <Route path="/settings" element={<ErrorBoundary><Settings /></ErrorBoundary>} />
              </Routes>
            </main>
            
            <VoiceInterface />
            
            <Toaster 
              position="top-right"
              toastOptions={{
                duration: 4000,
                style: {
                  background: 'var(--bg-secondary)',
                  color: 'var(--text-primary)',
                  border: '1px solid var(--border-color)',
                },
              }}
            />
          </div>
        </Router>
      </AppProvider>
    </ErrorBoundary>
  );
}

export default App;