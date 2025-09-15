import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import './Sidebar.css';

const Sidebar = ({ collapsed, onToggle }) => {
  const location = useLocation();

  const menuItems = [
    {
      path: '/dashboard',
      icon: 'fas fa-chart-line',
      label: 'Dashboard',
      labelHi: 'डैशबोर्ड'
    },
    {
      path: '/inventory',
      icon: 'fas fa-boxes',
      label: 'Inventory',
      labelHi: 'इन्वेंटरी'
    },
    {
      path: '/customers',
      icon: 'fas fa-users',
      label: 'Customers',
      labelHi: 'ग्राहक'
    },
    {
      path: '/finance',
      icon: 'fas fa-rupee-sign',
      label: 'Finance',
      labelHi: 'वित्त'
    },
    {
      path: '/marketing',
      icon: 'fas fa-bullhorn',
      label: 'Marketing',
      labelHi: 'मार्केटिंग'
    },
    {
      path: '/reports',
      icon: 'fas fa-chart-bar',
      label: 'Reports',
      labelHi: 'रिपोर्ट'
    },
    {
      path: '/ai-agents',
      icon: 'fas fa-robot',
      label: 'AI Agents',
      labelHi: 'AI एजेंट'
    },
    {
      path: '/settings',
      icon: 'fas fa-cog',
      label: 'Settings',
      labelHi: 'सेटिंग्स'
    }
  ];

  return (
    <aside className={`sidebar ${collapsed ? 'collapsed' : ''}`}>
      {/* Logo Section */}
      <div className="sidebar-header">
        <div className="logo">
          <span className="logo-icon">🇮🇳</span>
          {!collapsed && (
            <div className="logo-text">
              <span className="logo-title">VyapaarGPT</span>
              <span className="logo-subtitle">Business OS</span>
            </div>
          )}
        </div>
      </div>

      {/* Navigation */}
      <nav className="sidebar-nav">
        <ul className="nav-list">
          {menuItems.map((item) => (
            <li key={item.path} className="nav-item">
              <Link
                to={item.path}
                className={`nav-link ${location.pathname === item.path ? 'active' : ''}`}
                title={collapsed ? item.label : ''}
              >
                <i className={`nav-icon ${item.icon}`}></i>
                {!collapsed && (
                  <div className="nav-text">
                    <span className="nav-label-en">{item.label}</span>
                    <span className="nav-label-hi">{item.labelHi}</span>
                  </div>
                )}
              </Link>
            </li>
          ))}
        </ul>
      </nav>

      {/* Bottom Section */}
      <div className="sidebar-footer">
        {!collapsed && (
          <div className="business-info">
            <div className="business-avatar">
              <i className="fas fa-store"></i>
            </div>
            <div className="business-details">
              <div className="business-name">Kumar Electronics</div>
              <div className="business-type">Retail Store</div>
            </div>
          </div>
        )}
        
        {/* Collapse Toggle */}
        <button 
          className="collapse-btn"
          onClick={onToggle}
          title={collapsed ? 'Expand Sidebar' : 'Collapse Sidebar'}
        >
          <i className={`fas ${collapsed ? 'fa-chevron-right' : 'fa-chevron-left'}`}></i>
        </button>
      </div>
    </aside>
  );
};

export default Sidebar;