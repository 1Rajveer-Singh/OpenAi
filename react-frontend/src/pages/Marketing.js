import React, { useState, useEffect } from 'react';
import { useAppContext } from '../context/AppContext';
import './Pages.css';

const Marketing = () => {
  const { state, actions } = useAppContext();
  const [campaigns, setCampaigns] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showCreateCampaign, setShowCreateCampaign] = useState(false);
  const [newCampaign, setNewCampaign] = useState({
    name: '',
    type: 'email',
    budget: '',
    startDate: new Date().toISOString().split('T')[0],
    endDate: '',
    description: ''
  });

  useEffect(() => {
    fetchCampaigns();
  }, []);

  const fetchCampaigns = async () => {
    try {
      // Simulate API call
      setTimeout(() => {
        setCampaigns([
          {
            id: 1,
            name: 'Summer Sale 2025',
            type: 'email',
            budget: 15000,
            spent: 8500,
            startDate: '2025-09-01',
            endDate: '2025-09-30',
            status: 'active',
            impressions: 45000,
            clicks: 2250,
            conversions: 180
          },
          {
            id: 2,
            name: 'New Product Launch',
            type: 'social',
            budget: 25000,
            spent: 12000,
            startDate: '2025-09-10',
            endDate: '2025-10-10',
            status: 'active',
            impressions: 78000,
            clicks: 3900,
            conversions: 312
          },
          {
            id: 3,
            name: 'Customer Retention',
            type: 'sms',
            budget: 8000,
            spent: 8000,
            startDate: '2025-08-15',
            endDate: '2025-09-15',
            status: 'completed',
            impressions: 15000,
            clicks: 1500,
            conversions: 225
          }
        ]);
        setLoading(false);
      }, 1000);
    } catch (error) {
      console.error('Error fetching campaigns:', error);
      setLoading(false);
    }
  };

  const handleCreateCampaign = (e) => {
    e.preventDefault();
    const campaign = {
      id: Date.now(),
      ...newCampaign,
      budget: parseFloat(newCampaign.budget),
      spent: 0,
      status: 'draft',
      impressions: 0,
      clicks: 0,
      conversions: 0
    };
    setCampaigns([campaign, ...campaigns]);
    setNewCampaign({
      name: '',
      type: 'email',
      budget: '',
      startDate: new Date().toISOString().split('T')[0],
      endDate: '',
      description: ''
    });
    setShowCreateCampaign(false);
  };

  const getCampaignStatusColor = (status) => {
    switch (status) {
      case 'active': return 'green';
      case 'completed': return 'blue';
      case 'paused': return 'orange';
      case 'draft': return 'gray';
      default: return 'gray';
    }
  };

  const calculateROI = (budget, conversions) => {
    const avgOrderValue = 500; // Assumed average order value
    const revenue = conversions * avgOrderValue;
    const roi = budget > 0 ? (((revenue - budget) / budget) * 100).toFixed(1) : 0;
    return roi;
  };

  if (loading) {
    return (
      <div className="page-container">
        <div className="loading-spinner">Loading marketing data...</div>
      </div>
    );
  }

  const totalBudget = campaigns.reduce((sum, c) => sum + c.budget, 0);
  const totalSpent = campaigns.reduce((sum, c) => sum + c.spent, 0);
  const totalConversions = campaigns.reduce((sum, c) => sum + c.conversions, 0);
  const activeCampaigns = campaigns.filter(c => c.status === 'active').length;

  return (
    <div className="page-container">
      <div className="page-header">
        <h1>📈 Marketing Tools</h1>
        <button 
          className="btn btn-primary"
          onClick={() => setShowCreateCampaign(true)}
        >
          Create Campaign
        </button>
      </div>

      <div className="marketing-overview">
        <div className="stat-card">
          <h3>Total Budget</h3>
          <p>₹{totalBudget.toLocaleString()}</p>
          <small>All campaigns</small>
        </div>
        <div className="stat-card">
          <h3>Total Spent</h3>
          <p>₹{totalSpent.toLocaleString()}</p>
          <small>{((totalSpent/totalBudget)*100).toFixed(1)}% of budget</small>
        </div>
        <div className="stat-card">
          <h3>Active Campaigns</h3>
          <p>{activeCampaigns}</p>
          <small>Currently running</small>
        </div>
        <div className="stat-card">
          <h3>Total Conversions</h3>
          <p>{totalConversions}</p>
          <small>This month</small>
        </div>
      </div>

      <div className="marketing-tools">
        <div className="tool-section">
          <h3>🎯 Campaign Performance</h3>
          <div className="campaigns-grid">
            {campaigns.map(campaign => (
              <div key={campaign.id} className="campaign-card">
                <div className="campaign-header">
                  <h4>{campaign.name}</h4>
                  <span className={`status ${getCampaignStatusColor(campaign.status)}`}>
                    {campaign.status}
                  </span>
                </div>
                <div className="campaign-type">
                  {campaign.type === 'email' && '📧'} 
                  {campaign.type === 'social' && '📱'} 
                  {campaign.type === 'sms' && '💬'} 
                  {campaign.type.toUpperCase()}
                </div>
                <div className="campaign-metrics">
                  <div className="metric">
                    <span>Budget</span>
                    <strong>₹{campaign.budget.toLocaleString()}</strong>
                  </div>
                  <div className="metric">
                    <span>Spent</span>
                    <strong>₹{campaign.spent.toLocaleString()}</strong>
                  </div>
                  <div className="metric">
                    <span>Impressions</span>
                    <strong>{campaign.impressions.toLocaleString()}</strong>
                  </div>
                  <div className="metric">
                    <span>Clicks</span>
                    <strong>{campaign.clicks.toLocaleString()}</strong>
                  </div>
                  <div className="metric">
                    <span>Conversions</span>
                    <strong>{campaign.conversions}</strong>
                  </div>
                  <div className="metric">
                    <span>ROI</span>
                    <strong className={calculateROI(campaign.spent, campaign.conversions) >= 0 ? 'positive' : 'negative'}>
                      {calculateROI(campaign.spent, campaign.conversions)}%
                    </strong>
                  </div>
                </div>
                <div className="campaign-actions">
                  <button className="btn btn-sm">Edit</button>
                  <button className="btn btn-sm">Analytics</button>
                  <button className="btn btn-sm btn-danger">Pause</button>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="marketing-insights">
          <div className="insight-card">
            <h3>📊 Quick Insights</h3>
            <ul>
              <li>Email campaigns have the highest conversion rate (15%)</li>
              <li>Social media campaigns reach the widest audience</li>
              <li>SMS campaigns have the fastest response time</li>
              <li>Best performing time: Tuesday-Thursday, 10 AM - 2 PM</li>
            </ul>
          </div>

          <div className="insight-card">
            <h3>🎯 Recommendations</h3>
            <ul>
              <li>Increase budget for "New Product Launch" campaign</li>
              <li>A/B test email subject lines for better open rates</li>
              <li>Retarget users who clicked but didn't convert</li>
              <li>Create lookalike audiences from top customers</li>
            </ul>
          </div>
        </div>
      </div>

      {showCreateCampaign && (
        <div className="modal-overlay">
          <div className="modal">
            <h2>Create New Campaign</h2>
            <form onSubmit={handleCreateCampaign}>
              <input
                type="text"
                placeholder="Campaign Name"
                value={newCampaign.name}
                onChange={(e) => setNewCampaign({...newCampaign, name: e.target.value})}
                required
              />
              
              <select
                value={newCampaign.type}
                onChange={(e) => setNewCampaign({...newCampaign, type: e.target.value})}
                required
              >
                <option value="email">📧 Email Campaign</option>
                <option value="social">📱 Social Media</option>
                <option value="sms">💬 SMS Campaign</option>
                <option value="display">🖥️ Display Ads</option>
                <option value="search">🔍 Search Ads</option>
              </select>
              
              <input
                type="number"
                placeholder="Budget (₹)"
                value={newCampaign.budget}
                onChange={(e) => setNewCampaign({...newCampaign, budget: e.target.value})}
                required
              />
              
              <input
                type="date"
                placeholder="Start Date"
                value={newCampaign.startDate}
                onChange={(e) => setNewCampaign({...newCampaign, startDate: e.target.value})}
                required
              />
              
              <input
                type="date"
                placeholder="End Date"
                value={newCampaign.endDate}
                onChange={(e) => setNewCampaign({...newCampaign, endDate: e.target.value})}
                required
              />
              
              <textarea
                placeholder="Campaign Description"
                value={newCampaign.description}
                onChange={(e) => setNewCampaign({...newCampaign, description: e.target.value})}
                rows="3"
              />
              
              <div className="modal-actions">
                <button type="submit" className="btn btn-primary">Create Campaign</button>
                <button type="button" className="btn" onClick={() => setShowCreateCampaign(false)}>Cancel</button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default Marketing;