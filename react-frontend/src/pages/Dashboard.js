import React, { useEffect, useState } from 'react';
import { useAppContext } from '../context/AppContext';
import DashboardCard from '../components/Dashboard/DashboardCard';
import { SalesChart, RevenueChart, RecentTransactions, TopProducts } from '../components/Dashboard';
import './Dashboard.css';

const Dashboard = () => {
  const { state, actions } = useAppContext();
  const [greeting, setGreeting] = useState('');

  useEffect(() => {
    // Set greeting based on time
    const hour = new Date().getHours();
    if (hour < 12) {
      setGreeting('Good Morning! सुप्रभात!');
    } else if (hour < 17) {
      setGreeting('Good Afternoon! शुभ दोपहर!');
    } else {
      setGreeting('Good Evening! शुभ संध्या!');
    }

    // Fetch dashboard data
    actions.fetchDashboardData();
  }, [actions]);

  const dashboardStats = [
    {
      title: 'Today\'s Sales',
      titleHi: 'आज की बिक्री',
      value: `₹${(state.dashboard.totalSales || 0).toLocaleString('en-IN')}`,
      change: '+12.5%',
      changeType: 'positive',
      icon: 'fas fa-rupee-sign',
      color: 'success'
    },
    {
      title: 'Total Customers',
      titleHi: 'कुल ग्राहक',
      value: (state.dashboard.totalCustomers || 0).toLocaleString('en-IN'),
      change: '+8 new',
      changeType: 'positive',
      icon: 'fas fa-users',
      color: 'primary'
    },
    {
      title: 'Products',
      titleHi: 'उत्पाद',
      value: (state.dashboard.totalProducts || 0).toLocaleString('en-IN'),
      change: '+5 added',
      changeType: 'positive',
      icon: 'fas fa-boxes',
      color: 'info'
    },
    {
      title: 'Monthly Revenue',
      titleHi: 'मासिक आय',
      value: `₹${(state.dashboard.monthlyRevenue || 0).toLocaleString('en-IN')}`,
      change: '+18.2%',
      changeType: 'positive',
      icon: 'fas fa-chart-line',
      color: 'warning'
    }
  ];

  const quickActions = [
    {
      title: 'Add Sale',
      titleHi: 'बिक्री जोड़ें',
      icon: 'fas fa-plus-circle',
      color: 'success',
      action: () => console.log('Add sale')
    },
    {
      title: 'New Customer',
      titleHi: 'नया ग्राहक',
      icon: 'fas fa-user-plus',
      color: 'primary',
      action: () => console.log('Add customer')
    },
    {
      title: 'Add Product',
      titleHi: 'उत्पाद जोड़ें',
      icon: 'fas fa-box',
      color: 'info',
      action: () => console.log('Add product')
    },
    {
      title: 'Voice Command',
      titleHi: 'आवाज़ कमांड',
      icon: 'fas fa-microphone',
      color: 'warning',
      action: () => console.log('Voice command')
    }
  ];

  if (state.loading) {
    return (
      <div className="dashboard-loading">
        <div className="spinner"></div>
        <p>Loading dashboard...</p>
      </div>
    );
  }

  return (
    <div className="dashboard">
      {/* Header Section */}
      <div className="dashboard-header">
        <div className="greeting-section">
          <h1 className="dashboard-title">
            {greeting}
          </h1>
          <p className="dashboard-subtitle">
            Welcome back, {state.user.name}! Here's what's happening with your business today.
            <br />
            <span className="subtitle-hi">
              स्वागत है, {state.user.name}! आज आपके व्यापार में यह हो रहा है।
            </span>
          </p>
        </div>
        
        <div className="date-time-section">
          <div className="current-date">
            {new Date().toLocaleDateString('en-IN', { 
              weekday: 'long', 
              year: 'numeric', 
              month: 'long', 
              day: 'numeric' 
            })}
          </div>
          <div className="current-time">
            {new Date().toLocaleTimeString('en-IN', { 
              hour: '2-digit', 
              minute: '2-digit',
              hour12: true 
            })}
          </div>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="stats-grid">
        {dashboardStats.map((stat, index) => (
          <DashboardCard
            key={index}
            title={stat.title}
            titleHi={stat.titleHi}
            value={stat.value}
            change={stat.change}
            changeType={stat.changeType}
            icon={stat.icon}
            color={stat.color}
          />
        ))}
      </div>

      {/* Quick Actions */}
      <div className="quick-actions-section">
        <h2 className="section-title">
          Quick Actions
          <span className="title-hi">त्वरित कार्य</span>
        </h2>
        <div className="quick-actions-grid">
          {quickActions.map((action, index) => (
            <button 
              key={index}
              className={`quick-action-btn ${action.color}`}
              onClick={action.action}
            >
              <i className={action.icon}></i>
              <div className="action-text">
                <span className="action-title">{action.title}</span>
                <span className="action-title-hi">{action.titleHi}</span>
              </div>
            </button>
          ))}
        </div>
      </div>

      {/* Charts Section */}
      <div className="charts-section">
        <div className="chart-container">
          <SalesChart data={state.dashboard.salesData} />
        </div>
        <div className="chart-container">
          <RevenueChart data={state.dashboard.revenueData} />
        </div>
      </div>

      {/* Bottom Section */}
      <div className="bottom-section">
        <div className="recent-transactions-container">
          <RecentTransactions transactions={state.dashboard.recentTransactions} />
        </div>
        <div className="top-products-container">
          <TopProducts products={state.dashboard.topProducts} />
        </div>
      </div>

      {/* AI Insights */}
      <div className="ai-insights-section">
        <div className="ai-insights-card">
          <div className="ai-insights-header">
            <i className="fas fa-robot"></i>
            <h3>AI Business Insights</h3>
            <span className="insights-hi">AI व्यापार अंतर्दृष्टि</span>
          </div>
          <div className="ai-insights-content">
            <div className="insight-item">
              <div className="insight-icon success">
                <i className="fas fa-arrow-up"></i>
              </div>
              <div className="insight-text">
                <p>Sales are up 15% this week compared to last week. iPhone sales are driving growth.</p>
                <p className="insight-hi">इस हफ्ते बिक्री पिछले हफ्ते की तुलना में 15% बढ़ी है। iPhone की बिक्री वृद्धि का कारण है।</p>
              </div>
            </div>
            <div className="insight-item">
              <div className="insight-icon warning">
                <i className="fas fa-exclamation-triangle"></i>
              </div>
              <div className="insight-text">
                <p>Stock alert: Samsung Galaxy S24 is running low. Consider reordering soon.</p>
                <p className="insight-hi">स्टॉक अलर्ट: Samsung Galaxy S24 कम हो गया है। जल्द ही दोबारा ऑर्डर करने पर विचार करें।</p>
              </div>
            </div>
            <div className="insight-item">
              <div className="insight-icon info">
                <i className="fas fa-lightbulb"></i>
              </div>
              <div className="insight-text">
                <p>Festive season approaching! Consider stocking up on popular items and creating special offers.</p>
                <p className="insight-hi">त्योहारी सीजन आ रहा है! लोकप्रिय वस्तुओं का स्टॉक बढ़ाने और विशेष ऑफर बनाने पर विचार करें।</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;