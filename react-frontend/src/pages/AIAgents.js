import React, { useState, useEffect } from 'react';
import { useAppContext } from '../context/AppContext';
import './Pages.css';

const AIAgents = () => {
  const { state, actions } = useAppContext();
  const [agents, setAgents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedAgent, setSelectedAgent] = useState(null);
  const [showCreateAgent, setShowCreateAgent] = useState(false);
  const [newAgent, setNewAgent] = useState({
    name: '',
    type: 'customer-service',
    description: '',
    enabled: true
  });

  useEffect(() => {
    fetchAgents();
  }, []);

  const fetchAgents = async () => {
    try {
      // Simulate API call
      setTimeout(() => {
        setAgents([
          {
            id: 1,
            name: 'Customer Support Bot',
            type: 'customer-service',
            description: 'Handles customer inquiries and support tickets',
            enabled: true,
            status: 'active',
            interactions: 1247,
            successRate: 89.5,
            avgResponseTime: '2.3s',
            lastActive: '2025-09-15T10:30:00'
          },
          {
            id: 2,
            name: 'Sales Assistant',
            type: 'sales',
            description: 'Helps with lead qualification and product recommendations',
            enabled: true,
            status: 'active',
            interactions: 856,
            successRate: 76.2,
            avgResponseTime: '1.8s',
            lastActive: '2025-09-15T11:15:00'
          },
          {
            id: 3,
            name: 'Inventory Optimizer',
            type: 'inventory',
            description: 'Automatically manages stock levels and reorder points',
            enabled: false,
            status: 'paused',
            interactions: 342,
            successRate: 94.1,
            avgResponseTime: '0.5s',
            lastActive: '2025-09-14T16:45:00'
          },
          {
            id: 4,
            name: 'Marketing Analyst',
            type: 'marketing',
            description: 'Analyzes campaign performance and suggests optimizations',
            enabled: true,
            status: 'learning',
            interactions: 89,
            successRate: 67.4,
            avgResponseTime: '3.1s',
            lastActive: '2025-09-15T09:20:00'
          }
        ]);
        setLoading(false);
      }, 1000);
    } catch (error) {
      console.error('Error fetching AI agents:', error);
      setLoading(false);
    }
  };

  const handleCreateAgent = (e) => {
    e.preventDefault();
    const agent = {
      id: Date.now(),
      ...newAgent,
      status: 'training',
      interactions: 0,
      successRate: 0,
      avgResponseTime: 'N/A',
      lastActive: new Date().toISOString()
    };
    setAgents([agent, ...agents]);
    setNewAgent({
      name: '',
      type: 'customer-service',
      description: '',
      enabled: true
    });
    setShowCreateAgent(false);
  };

  const toggleAgent = (agentId) => {
    setAgents(agents.map(agent => 
      agent.id === agentId 
        ? { ...agent, enabled: !agent.enabled, status: agent.enabled ? 'paused' : 'active' }
        : agent
    ));
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'active': return 'green';
      case 'learning': return 'blue';
      case 'training': return 'orange';
      case 'paused': return 'gray';
      case 'error': return 'red';
      default: return 'gray';
    }
  };

  const getAgentIcon = (type) => {
    switch (type) {
      case 'customer-service': return '🎧';
      case 'sales': return '💼';
      case 'inventory': return '📦';
      case 'marketing': return '📈';
      case 'finance': return '💰';
      default: return '🤖';
    }
  };

  if (loading) {
    return (
      <div className="page-container">
        <div className="loading-spinner">Loading AI agents...</div>
      </div>
    );
  }

  const activeAgents = agents.filter(a => a.enabled).length;
  const totalInteractions = agents.reduce((sum, a) => sum + a.interactions, 0);
  const avgSuccessRate = agents.length > 0 
    ? (agents.reduce((sum, a) => sum + a.successRate, 0) / agents.length).toFixed(1)
    : 0;

  return (
    <div className="page-container">
      <div className="page-header">
        <h1>🤖 AI Agents</h1>
        <button 
          className="btn btn-primary"
          onClick={() => setShowCreateAgent(true)}
        >
          Create Agent
        </button>
      </div>

      <div className="ai-overview">
        <div className="stat-card">
          <h3>Active Agents</h3>
          <p>{activeAgents}</p>
          <small>Currently running</small>
        </div>
        <div className="stat-card">
          <h3>Total Interactions</h3>
          <p>{totalInteractions.toLocaleString()}</p>
          <small>All time</small>
        </div>
        <div className="stat-card">
          <h3>Avg Success Rate</h3>
          <p>{avgSuccessRate}%</p>
          <small>Across all agents</small>
        </div>
        <div className="stat-card">
          <h3>Cost Savings</h3>
          <p>₹2.4L</p>
          <small>This month</small>
        </div>
      </div>

      <div className="agents-grid">
        {agents.map(agent => (
          <div key={agent.id} className="agent-card">
            <div className="agent-header">
              <div className="agent-info">
                <span className="agent-icon">{getAgentIcon(agent.type)}</span>
                <div>
                  <h3>{agent.name}</h3>
                  <p className="agent-type">{agent.type.replace('-', ' ').toUpperCase()}</p>
                </div>
              </div>
              <div className="agent-controls">
                <span className={`status ${getStatusColor(agent.status)}`}>
                  {agent.status}
                </span>
                <button 
                  className={`toggle-btn ${agent.enabled ? 'enabled' : 'disabled'}`}
                  onClick={() => toggleAgent(agent.id)}
                >
                  {agent.enabled ? 'ON' : 'OFF'}
                </button>
              </div>
            </div>

            <p className="agent-description">{agent.description}</p>

            <div className="agent-metrics">
              <div className="metric">
                <span>Interactions</span>
                <strong>{agent.interactions.toLocaleString()}</strong>
              </div>
              <div className="metric">
                <span>Success Rate</span>
                <strong>{agent.successRate}%</strong>
              </div>
              <div className="metric">
                <span>Response Time</span>
                <strong>{agent.avgResponseTime}</strong>
              </div>
            </div>

            <div className="agent-actions">
              <button 
                className="btn btn-sm"
                onClick={() => setSelectedAgent(agent)}
              >
                Configure
              </button>
              <button className="btn btn-sm">Analytics</button>
              <button className="btn btn-sm">Train</button>
            </div>

            <div className="last-active">
              Last active: {new Date(agent.lastActive).toLocaleString()}
            </div>
          </div>
        ))}
      </div>

      <div className="ai-insights">
        <h3>🧠 AI Insights & Recommendations</h3>
        <div className="insights-grid">
          <div className="insight-card">
            <h4>Performance Alert</h4>
            <p>Customer Support Bot is performing exceptionally well with 89.5% success rate. Consider expanding its capabilities.</p>
          </div>
          <div className="insight-card">
            <h4>Training Needed</h4>
            <p>Marketing Analyst needs additional training data to improve its 67.4% success rate.</p>
          </div>
          <div className="insight-card">
            <h4>Optimization Opportunity</h4>
            <p>Inventory Optimizer has been paused. Reactivating it could save ₹15,000 in operational costs.</p>
          </div>
          <div className="insight-card">
            <h4>Scaling Suggestion</h4>
            <p>Consider creating a Finance Assistant agent to automate invoice processing and expense categorization.</p>
          </div>
        </div>
      </div>

      {selectedAgent && (
        <div className="modal-overlay">
          <div className="modal agent-config-modal">
            <h2>Configure {selectedAgent.name}</h2>
            <div className="config-section">
              <h3>Agent Settings</h3>
              <div className="config-item">
                <label>Response Personality</label>
                <select>
                  <option value="professional">Professional</option>
                  <option value="friendly">Friendly</option>
                  <option value="formal">Formal</option>
                  <option value="casual">Casual</option>
                </select>
              </div>
              <div className="config-item">
                <label>Confidence Threshold</label>
                <input type="range" min="0" max="100" defaultValue="75" />
                <span>75%</span>
              </div>
              <div className="config-item">
                <label>Max Response Time</label>
                <input type="number" defaultValue="5" />
                <span>seconds</span>
              </div>
              <div className="config-item">
                <label>Escalation Rules</label>
                <textarea placeholder="Define when to escalate to human agents..." rows="3"></textarea>
              </div>
            </div>
            
            <div className="config-section">
              <h3>Training Data</h3>
              <button className="btn">Upload Training Files</button>
              <button className="btn">Import Conversations</button>
              <button className="btn">Add Knowledge Base</button>
            </div>

            <div className="modal-actions">
              <button className="btn btn-primary">Save Configuration</button>
              <button className="btn" onClick={() => setSelectedAgent(null)}>Cancel</button>
            </div>
          </div>
        </div>
      )}

      {showCreateAgent && (
        <div className="modal-overlay">
          <div className="modal">
            <h2>Create New AI Agent</h2>
            <form onSubmit={handleCreateAgent}>
              <input
                type="text"
                placeholder="Agent Name"
                value={newAgent.name}
                onChange={(e) => setNewAgent({...newAgent, name: e.target.value})}
                required
              />
              
              <select
                value={newAgent.type}
                onChange={(e) => setNewAgent({...newAgent, type: e.target.value})}
                required
              >
                <option value="customer-service">🎧 Customer Service</option>
                <option value="sales">💼 Sales Assistant</option>
                <option value="inventory">📦 Inventory Management</option>
                <option value="marketing">📈 Marketing Analyst</option>
                <option value="finance">💰 Finance Assistant</option>
                <option value="hr">👥 HR Assistant</option>
              </select>
              
              <textarea
                placeholder="Agent Description"
                value={newAgent.description}
                onChange={(e) => setNewAgent({...newAgent, description: e.target.value})}
                rows="3"
                required
              />
              
              <label className="checkbox-label">
                <input
                  type="checkbox"
                  checked={newAgent.enabled}
                  onChange={(e) => setNewAgent({...newAgent, enabled: e.target.checked})}
                />
                Enable agent immediately
              </label>
              
              <div className="modal-actions">
                <button type="submit" className="btn btn-primary">Create Agent</button>
                <button type="button" className="btn" onClick={() => setShowCreateAgent(false)}>Cancel</button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default AIAgents;