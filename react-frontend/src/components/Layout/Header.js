import React, { useState } from 'react';
import { useAppContext } from '../../context/AppContext';
import './Header.css';

const Header = ({ onMenuToggle, onThemeToggle, theme }) => {
  const { state } = useAppContext();
  const [searchQuery, setSearchQuery] = useState('');
  const [showNotifications, setShowNotifications] = useState(false);
  const [showProfile, setShowProfile] = useState(false);

  const handleSearch = (e) => {
    setSearchQuery(e.target.value);
    // Implement search functionality
  };

  const notifications = [
    {
      id: 1,
      type: 'success',
      title: 'New Sale',
      message: 'Order #1234 completed successfully',
      time: '2 min ago',
      unread: true
    },
    {
      id: 2,
      type: 'warning',
      title: 'Low Stock Alert',
      message: 'iPhone 15 Pro stock is running low',
      time: '10 min ago',
      unread: true
    },
    {
      id: 3,
      type: 'info',
      title: 'New Customer',
      message: 'Priya Sharma registered as new customer',
      time: '1 hour ago',
      unread: false
    }
  ];

  const unreadCount = notifications.filter(n => n.unread).length;

  return (
    <header className="header">
      <div className="header-left">
        {/* Mobile Menu Toggle */}
        <button className="menu-toggle md:hidden" onClick={onMenuToggle}>
          <i className="fas fa-bars"></i>
        </button>

        {/* Search Bar */}
        <div className="search-container">
          <div className="search-input-wrapper">
            <i className="fas fa-search search-icon"></i>
            <input
              type="text"
              className="search-input"
              placeholder="Search products, customers, orders... | खोजें..."
              value={searchQuery}
              onChange={handleSearch}
            />
            <div className="search-shortcuts">
              <span className="shortcut-key">⌘</span>
              <span className="shortcut-key">K</span>
            </div>
          </div>

          {/* Search Results Dropdown */}
          {searchQuery && (
            <div className="search-results">
              <div className="search-section">
                <div className="search-section-title">Products</div>
                <div className="search-result-item">
                  <i className="fas fa-mobile-alt"></i>
                  <span>iPhone 15 Pro</span>
                </div>
                <div className="search-result-item">
                  <i className="fas fa-laptop"></i>
                  <span>MacBook Air M2</span>
                </div>
              </div>
              <div className="search-section">
                <div className="search-section-title">Customers</div>
                <div className="search-result-item">
                  <i className="fas fa-user"></i>
                  <span>Rajesh Kumar</span>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>

      <div className="header-right">
        {/* Voice Assistant Toggle */}
        <button className="header-btn voice-btn" title="Voice Assistant">
          <i className="fas fa-microphone"></i>
          <span className="voice-indicator"></span>
        </button>

        {/* Notifications */}
        <div className="dropdown-container">
          <button 
            className="header-btn notification-btn"
            onClick={() => setShowNotifications(!showNotifications)}
            title="Notifications"
          >
            <i className="fas fa-bell"></i>
            {unreadCount > 0 && (
              <span className="notification-badge">{unreadCount}</span>
            )}
          </button>

          {showNotifications && (
            <div className="dropdown notification-dropdown">
              <div className="dropdown-header">
                <h3>Notifications</h3>
                <button className="mark-all-read">Mark all read</button>
              </div>
              <div className="dropdown-content">
                {notifications.map(notification => (
                  <div 
                    key={notification.id} 
                    className={`notification-item ${notification.unread ? 'unread' : ''}`}
                  >
                    <div className={`notification-icon ${notification.type}`}>
                      <i className={`fas ${
                        notification.type === 'success' ? 'fa-check-circle' :
                        notification.type === 'warning' ? 'fa-exclamation-triangle' :
                        'fa-info-circle'
                      }`}></i>
                    </div>
                    <div className="notification-content">
                      <div className="notification-title">{notification.title}</div>
                      <div className="notification-message">{notification.message}</div>
                      <div className="notification-time">{notification.time}</div>
                    </div>
                  </div>
                ))}
              </div>
              <div className="dropdown-footer">
                <button className="view-all-btn">View All Notifications</button>
              </div>
            </div>
          )}
        </div>

        {/* Theme Toggle */}
        <button 
          className="header-btn theme-toggle"
          onClick={onThemeToggle}
          title={`Switch to ${theme === 'light' ? 'dark' : 'light'} mode`}
        >
          <i className={`fas ${theme === 'light' ? 'fa-moon' : 'fa-sun'}`}></i>
        </button>

        {/* User Profile */}
        <div className="dropdown-container">
          <button 
            className="profile-btn"
            onClick={() => setShowProfile(!showProfile)}
            title="User Profile"
          >
            <div className="profile-avatar">
              <img 
                src="https://ui-avatars.com/api/?name=Rajesh+Kumar&background=4CAF50&color=fff" 
                alt="Profile"
              />
            </div>
            <div className="profile-info">
              <div className="profile-name">{state.user.name}</div>
              <div className="profile-role">{state.user.role}</div>
            </div>
            <i className="fas fa-chevron-down profile-arrow"></i>
          </button>

          {showProfile && (
            <div className="dropdown profile-dropdown">
              <div className="dropdown-header">
                <div className="profile-header">
                  <div className="profile-avatar large">
                    <img 
                      src="https://ui-avatars.com/api/?name=Rajesh+Kumar&background=4CAF50&color=fff" 
                      alt="Profile"
                    />
                  </div>
                  <div className="profile-details">
                    <div className="profile-name">{state.user.name}</div>
                    <div className="profile-business">{state.user.business}</div>
                    <div className="profile-email">rajesh@kumarelectronics.com</div>
                  </div>
                </div>
              </div>
              <div className="dropdown-content">
                <div className="profile-menu-item">
                  <i className="fas fa-user"></i>
                  <span>Profile Settings</span>
                </div>
                <div className="profile-menu-item">
                  <i className="fas fa-store"></i>
                  <span>Business Profile</span>
                </div>
                <div className="profile-menu-item">
                  <i className="fas fa-cog"></i>
                  <span>Preferences</span>
                </div>
                <div className="profile-menu-item">
                  <i className="fas fa-question-circle"></i>
                  <span>Help & Support</span>
                </div>
                <div className="profile-menu-divider"></div>
                <div className="profile-menu-item logout">
                  <i className="fas fa-sign-out-alt"></i>
                  <span>Logout</span>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </header>
  );
};

export default Header;