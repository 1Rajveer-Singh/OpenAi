import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import { AppProvider } from './context/AppContext';
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
    <AppProvider>
      <DemoBanner />
      <Router>
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
              <Route path="/" element={<Dashboard />} />
              <Route path="/dashboard" element={<Dashboard />} />
              <Route path="/inventory" element={<Inventory />} />
              <Route path="/customers" element={<Customers />} />
              <Route path="/finance" element={<Finance />} />
              <Route path="/marketing" element={<Marketing />} />
              <Route path="/reports" element={<Reports />} />
              <Route path="/ai-agents" element={<AIAgents />} />
              <Route path="/settings" element={<Settings />} />
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
  );
}

export default App;