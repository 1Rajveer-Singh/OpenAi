import React, { useState } from 'react';
import { useAppContext } from '../context/AppContext';
import './Pages.css';

const Settings = () => {
  const { state, actions } = useAppContext();
  const [activeTab, setActiveTab] = useState('general');
  const [settings, setSettings] = useState({
    general: {
      companyName: 'VyapaarGPT Solutions',
      email: 'admin@vyapaargpt.com',
      phone: '+91 98765 43210',
      address: 'Mumbai, Maharashtra, India',
      timezone: 'Asia/Kolkata',
      currency: 'INR',
      language: 'en',
      theme: 'light'
    },
    notifications: {
      emailNotifications: true,
      smsNotifications: false,
      pushNotifications: true,
      lowStockAlerts: true,
      orderUpdates: true,
      customerMessages: true,
      systemUpdates: false,
      marketingEmails: false
    },
    security: {
      twoFactorAuth: false,
      sessionTimeout: 30,
      passwordRequirements: 'strong',
      ipWhitelist: '',
      auditLogs: true,
      dataEncryption: true
    },
    billing: {
      plan: 'Professional',
      billingCycle: 'monthly',
      nextBillingDate: '2025-10-15',
      paymentMethod: '**** **** **** 1234',
      autoRenewal: true
    },
    integrations: {
      googleAnalytics: false,
      facebookPixel: false,
      whatsappBusiness: true,
      razorpay: true,
      zoho: false,
      salesforce: false
    }
  });

  const handleSettingChange = (category, key, value) => {
    setSettings(prev => ({
      ...prev,
      [category]: {
        ...prev[category],
        [key]: value
      }
    }));
  };

  const saveSettings = () => {
    // Here you would typically send the settings to your API
    alert('Settings saved successfully!');
  };

  const resetSettings = () => {
    if (window.confirm('Are you sure you want to reset all settings to default?')) {
      // Reset to default settings
      alert('Settings reset to default!');
    }
  };

  const exportData = () => {
    alert('Data export feature coming soon!');
  };

  const importData = () => {
    alert('Data import feature coming soon!');
  };

  return (
    <div className="page-container">
      <div className="page-header">
        <h1>⚙️ Settings</h1>
        <div className="settings-actions">
          <button className="btn btn-sm" onClick={exportData}>📤 Export</button>
          <button className="btn btn-sm" onClick={importData}>📥 Import</button>
          <button className="btn btn-sm" onClick={resetSettings}>🔄 Reset</button>
          <button className="btn btn-primary" onClick={saveSettings}>💾 Save</button>
        </div>
      </div>

      <div className="settings-container">
        <div className="settings-sidebar">
          <div className="settings-tabs">
            <button 
              className={`tab ${activeTab === 'general' ? 'active' : ''}`}
              onClick={() => setActiveTab('general')}
            >
              🏢 General
            </button>
            <button 
              className={`tab ${activeTab === 'notifications' ? 'active' : ''}`}
              onClick={() => setActiveTab('notifications')}
            >
              🔔 Notifications
            </button>
            <button 
              className={`tab ${activeTab === 'security' ? 'active' : ''}`}
              onClick={() => setActiveTab('security')}
            >
              🔒 Security
            </button>
            <button 
              className={`tab ${activeTab === 'billing' ? 'active' : ''}`}
              onClick={() => setActiveTab('billing')}
            >
              💳 Billing
            </button>
            <button 
              className={`tab ${activeTab === 'integrations' ? 'active' : ''}`}
              onClick={() => setActiveTab('integrations')}
            >
              🔌 Integrations
            </button>
          </div>
        </div>

        <div className="settings-content">
          {activeTab === 'general' && (
            <div className="settings-section">
              <h2>General Settings</h2>
              
              <div className="setting-group">
                <h3>Company Information</h3>
                <div className="setting-item">
                  <label>Company Name</label>
                  <input
                    type="text"
                    value={settings.general.companyName}
                    onChange={(e) => handleSettingChange('general', 'companyName', e.target.value)}
                  />
                </div>
                <div className="setting-item">
                  <label>Email Address</label>
                  <input
                    type="email"
                    value={settings.general.email}
                    onChange={(e) => handleSettingChange('general', 'email', e.target.value)}
                  />
                </div>
                <div className="setting-item">
                  <label>Phone Number</label>
                  <input
                    type="tel"
                    value={settings.general.phone}
                    onChange={(e) => handleSettingChange('general', 'phone', e.target.value)}
                  />
                </div>
                <div className="setting-item">
                  <label>Address</label>
                  <textarea
                    value={settings.general.address}
                    onChange={(e) => handleSettingChange('general', 'address', e.target.value)}
                    rows="3"
                  />
                </div>
              </div>

              <div className="setting-group">
                <h3>Localization</h3>
                <div className="setting-item">
                  <label>Timezone</label>
                  <select
                    value={settings.general.timezone}
                    onChange={(e) => handleSettingChange('general', 'timezone', e.target.value)}
                  >
                    <option value="Asia/Kolkata">Asia/Kolkata (IST)</option>
                    <option value="Asia/Dubai">Asia/Dubai (GST)</option>
                    <option value="America/New_York">America/New_York (EST)</option>
                    <option value="Europe/London">Europe/London (GMT)</option>
                  </select>
                </div>
                <div className="setting-item">
                  <label>Currency</label>
                  <select
                    value={settings.general.currency}
                    onChange={(e) => handleSettingChange('general', 'currency', e.target.value)}
                  >
                    <option value="INR">INR (₹)</option>
                    <option value="USD">USD ($)</option>
                    <option value="EUR">EUR (€)</option>
                    <option value="GBP">GBP (£)</option>
                  </select>
                </div>
                <div className="setting-item">
                  <label>Language</label>
                  <select
                    value={settings.general.language}
                    onChange={(e) => handleSettingChange('general', 'language', e.target.value)}
                  >
                    <option value="en">English</option>
                    <option value="hi">हिंदी</option>
                    <option value="bn">বাংলা</option>
                    <option value="ta">தமிழ்</option>
                  </select>
                </div>
                <div className="setting-item">
                  <label>Theme</label>
                  <select
                    value={settings.general.theme}
                    onChange={(e) => handleSettingChange('general', 'theme', e.target.value)}
                  >
                    <option value="light">Light</option>
                    <option value="dark">Dark</option>
                    <option value="auto">Auto</option>
                  </select>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'notifications' && (
            <div className="settings-section">
              <h2>Notification Settings</h2>
              
              <div className="setting-group">
                <h3>Notification Channels</h3>
                <div className="setting-item toggle-item">
                  <label>Email Notifications</label>
                  <input
                    type="checkbox"
                    checked={settings.notifications.emailNotifications}
                    onChange={(e) => handleSettingChange('notifications', 'emailNotifications', e.target.checked)}
                  />
                </div>
                <div className="setting-item toggle-item">
                  <label>SMS Notifications</label>
                  <input
                    type="checkbox"
                    checked={settings.notifications.smsNotifications}
                    onChange={(e) => handleSettingChange('notifications', 'smsNotifications', e.target.checked)}
                  />
                </div>
                <div className="setting-item toggle-item">
                  <label>Push Notifications</label>
                  <input
                    type="checkbox"
                    checked={settings.notifications.pushNotifications}
                    onChange={(e) => handleSettingChange('notifications', 'pushNotifications', e.target.checked)}
                  />
                </div>
              </div>

              <div className="setting-group">
                <h3>Alert Types</h3>
                <div className="setting-item toggle-item">
                  <label>Low Stock Alerts</label>
                  <input
                    type="checkbox"
                    checked={settings.notifications.lowStockAlerts}
                    onChange={(e) => handleSettingChange('notifications', 'lowStockAlerts', e.target.checked)}
                  />
                </div>
                <div className="setting-item toggle-item">
                  <label>Order Updates</label>
                  <input
                    type="checkbox"
                    checked={settings.notifications.orderUpdates}
                    onChange={(e) => handleSettingChange('notifications', 'orderUpdates', e.target.checked)}
                  />
                </div>
                <div className="setting-item toggle-item">
                  <label>Customer Messages</label>
                  <input
                    type="checkbox"
                    checked={settings.notifications.customerMessages}
                    onChange={(e) => handleSettingChange('notifications', 'customerMessages', e.target.checked)}
                  />
                </div>
                <div className="setting-item toggle-item">
                  <label>System Updates</label>
                  <input
                    type="checkbox"
                    checked={settings.notifications.systemUpdates}
                    onChange={(e) => handleSettingChange('notifications', 'systemUpdates', e.target.checked)}
                  />
                </div>
                <div className="setting-item toggle-item">
                  <label>Marketing Emails</label>
                  <input
                    type="checkbox"
                    checked={settings.notifications.marketingEmails}
                    onChange={(e) => handleSettingChange('notifications', 'marketingEmails', e.target.checked)}
                  />
                </div>
              </div>
            </div>
          )}

          {activeTab === 'security' && (
            <div className="settings-section">
              <h2>Security Settings</h2>
              
              <div className="setting-group">
                <h3>Authentication</h3>
                <div className="setting-item toggle-item">
                  <label>Two-Factor Authentication</label>
                  <input
                    type="checkbox"
                    checked={settings.security.twoFactorAuth}
                    onChange={(e) => handleSettingChange('security', 'twoFactorAuth', e.target.checked)}
                  />
                </div>
                <div className="setting-item">
                  <label>Session Timeout (minutes)</label>
                  <input
                    type="number"
                    value={settings.security.sessionTimeout}
                    onChange={(e) => handleSettingChange('security', 'sessionTimeout', parseInt(e.target.value))}
                    min="5"
                    max="480"
                  />
                </div>
                <div className="setting-item">
                  <label>Password Requirements</label>
                  <select
                    value={settings.security.passwordRequirements}
                    onChange={(e) => handleSettingChange('security', 'passwordRequirements', e.target.value)}
                  >
                    <option value="basic">Basic (6+ characters)</option>
                    <option value="medium">Medium (8+ chars, numbers)</option>
                    <option value="strong">Strong (8+ chars, numbers, symbols)</option>
                  </select>
                </div>
              </div>

              <div className="setting-group">
                <h3>Access Control</h3>
                <div className="setting-item">
                  <label>IP Whitelist (comma separated)</label>
                  <textarea
                    value={settings.security.ipWhitelist}
                    onChange={(e) => handleSettingChange('security', 'ipWhitelist', e.target.value)}
                    placeholder="192.168.1.1, 10.0.0.1"
                    rows="2"
                  />
                </div>
                <div className="setting-item toggle-item">
                  <label>Audit Logs</label>
                  <input
                    type="checkbox"
                    checked={settings.security.auditLogs}
                    onChange={(e) => handleSettingChange('security', 'auditLogs', e.target.checked)}
                  />
                </div>
                <div className="setting-item toggle-item">
                  <label>Data Encryption</label>
                  <input
                    type="checkbox"
                    checked={settings.security.dataEncryption}
                    onChange={(e) => handleSettingChange('security', 'dataEncryption', e.target.checked)}
                  />
                </div>
              </div>
            </div>
          )}

          {activeTab === 'billing' && (
            <div className="settings-section">
              <h2>Billing & Subscription</h2>
              
              <div className="billing-overview">
                <div className="billing-card">
                  <h3>Current Plan</h3>
                  <div className="plan-info">
                    <h4>{settings.billing.plan}</h4>
                    <p>₹2,999/{settings.billing.billingCycle}</p>
                    <small>Next billing: {settings.billing.nextBillingDate}</small>
                  </div>
                  <button className="btn">Upgrade Plan</button>
                </div>

                <div className="billing-card">
                  <h3>Payment Method</h3>
                  <div className="payment-info">
                    <p>💳 {settings.billing.paymentMethod}</p>
                    <small>Expires: 12/2027</small>
                  </div>
                  <button className="btn">Update Payment</button>
                </div>

                <div className="billing-card">
                  <h3>Usage This Month</h3>
                  <div className="usage-info">
                    <div className="usage-item">
                      <span>API Calls</span>
                      <span>8,500 / 10,000</span>
                    </div>
                    <div className="usage-item">
                      <span>Storage</span>
                      <span>2.3 GB / 5 GB</span>
                    </div>
                    <div className="usage-item">
                      <span>Users</span>
                      <span>3 / 5</span>
                    </div>
                  </div>
                </div>
              </div>

              <div className="setting-group">
                <h3>Billing Preferences</h3>
                <div className="setting-item">
                  <label>Billing Cycle</label>
                  <select
                    value={settings.billing.billingCycle}
                    onChange={(e) => handleSettingChange('billing', 'billingCycle', e.target.value)}
                  >
                    <option value="monthly">Monthly</option>
                    <option value="quarterly">Quarterly (5% discount)</option>
                    <option value="yearly">Yearly (10% discount)</option>
                  </select>
                </div>
                <div className="setting-item toggle-item">
                  <label>Auto Renewal</label>
                  <input
                    type="checkbox"
                    checked={settings.billing.autoRenewal}
                    onChange={(e) => handleSettingChange('billing', 'autoRenewal', e.target.checked)}
                  />
                </div>
              </div>
            </div>
          )}

          {activeTab === 'integrations' && (
            <div className="settings-section">
              <h2>Integrations</h2>
              
              <div className="integrations-grid">
                <div className="integration-card">
                  <div className="integration-header">
                    <span className="integration-icon">📊</span>
                    <h3>Google Analytics</h3>
                  </div>
                  <p>Track website traffic and user behavior</p>
                  <div className="integration-toggle">
                    <input
                      type="checkbox"
                      checked={settings.integrations.googleAnalytics}
                      onChange={(e) => handleSettingChange('integrations', 'googleAnalytics', e.target.checked)}
                    />
                    <button className="btn btn-sm">Configure</button>
                  </div>
                </div>

                <div className="integration-card">
                  <div className="integration-header">
                    <span className="integration-icon">📘</span>
                    <h3>Facebook Pixel</h3>
                  </div>
                  <p>Track conversions and optimize ads</p>
                  <div className="integration-toggle">
                    <input
                      type="checkbox"
                      checked={settings.integrations.facebookPixel}
                      onChange={(e) => handleSettingChange('integrations', 'facebookPixel', e.target.checked)}
                    />
                    <button className="btn btn-sm">Configure</button>
                  </div>
                </div>

                <div className="integration-card">
                  <div className="integration-header">
                    <span className="integration-icon">💬</span>
                    <h3>WhatsApp Business</h3>
                  </div>
                  <p>Send order updates and support messages</p>
                  <div className="integration-toggle">
                    <input
                      type="checkbox"
                      checked={settings.integrations.whatsappBusiness}
                      onChange={(e) => handleSettingChange('integrations', 'whatsappBusiness', e.target.checked)}
                    />
                    <button className="btn btn-sm">Configure</button>
                  </div>
                </div>

                <div className="integration-card">
                  <div className="integration-header">
                    <span className="integration-icon">💳</span>
                    <h3>Razorpay</h3>
                  </div>
                  <p>Process payments and manage transactions</p>
                  <div className="integration-toggle">
                    <input
                      type="checkbox"
                      checked={settings.integrations.razorpay}
                      onChange={(e) => handleSettingChange('integrations', 'razorpay', e.target.checked)}
                    />
                    <button className="btn btn-sm">Configure</button>
                  </div>
                </div>

                <div className="integration-card">
                  <div className="integration-header">
                    <span className="integration-icon">📋</span>
                    <h3>Zoho</h3>
                  </div>
                  <p>CRM and business management suite</p>
                  <div className="integration-toggle">
                    <input
                      type="checkbox"
                      checked={settings.integrations.zoho}
                      onChange={(e) => handleSettingChange('integrations', 'zoho', e.target.checked)}
                    />
                    <button className="btn btn-sm">Configure</button>
                  </div>
                </div>

                <div className="integration-card">
                  <div className="integration-header">
                    <span className="integration-icon">🏢</span>
                    <h3>Salesforce</h3>
                  </div>
                  <p>Enterprise CRM and sales automation</p>
                  <div className="integration-toggle">
                    <input
                      type="checkbox"
                      checked={settings.integrations.salesforce}
                      onChange={(e) => handleSettingChange('integrations', 'salesforce', e.target.checked)}
                    />
                    <button className="btn btn-sm">Configure</button>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Settings;