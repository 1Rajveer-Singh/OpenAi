import React, { useState, useEffect } from 'react';
import { useAppContext } from '../context/AppContext';
import './Pages.css';

const Reports = () => {
  const { state, actions } = useAppContext();
  const [reports, setReports] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedReport, setSelectedReport] = useState('sales');
  const [dateRange, setDateRange] = useState('last-30-days');

  useEffect(() => {
    fetchReports();
  }, [selectedReport, dateRange]);

  const fetchReports = async () => {
    try {
      setLoading(true);
      // Simulate API call
      setTimeout(() => {
        const mockData = {
          sales: {
            total: 485000,
            growth: 12.5,
            orders: 156,
            avgOrderValue: 3109,
            data: [
              { period: 'Week 1', value: 85000 },
              { period: 'Week 2', value: 120000 },
              { period: 'Week 3', value: 135000 },
              { period: 'Week 4', value: 145000 }
            ]
          },
          customers: {
            total: 342,
            newCustomers: 45,
            retentionRate: 78.5,
            avgLifetimeValue: 15600,
            data: [
              { period: 'Week 1', value: 8 },
              { period: 'Week 2', value: 12 },
              { period: 'Week 3', value: 15 },
              { period: 'Week 4', value: 10 }
            ]
          },
          inventory: {
            totalProducts: 248,
            lowStockItems: 12,
            outOfStock: 3,
            turnoverRate: 4.2,
            data: [
              { category: 'Electronics', stock: 45 },
              { category: 'Clothing', stock: 78 },
              { category: 'Home', stock: 92 },
              { category: 'Books', stock: 33 }
            ]
          },
          finance: {
            revenue: 485000,
            expenses: 320000,
            profit: 165000,
            profitMargin: 34.0,
            data: [
              { period: 'Week 1', revenue: 85000, expenses: 58000 },
              { period: 'Week 2', revenue: 120000, expenses: 78000 },
              { period: 'Week 3', revenue: 135000, expenses: 89000 },
              { period: 'Week 4', revenue: 145000, expenses: 95000 }
            ]
          }
        };
        setReports(mockData);
        setLoading(false);
      }, 1000);
    } catch (error) {
      console.error('Error fetching reports:', error);
      setLoading(false);
    }
  };

  const generatePDF = () => {
    alert('PDF generation feature coming soon!');
  };

  const exportExcel = () => {
    alert('Excel export feature coming soon!');
  };

  const shareReport = () => {
    alert('Report sharing feature coming soon!');
  };

  if (loading) {
    return (
      <div className="page-container">
        <div className="loading-spinner">Generating reports...</div>
      </div>
    );
  }

  const currentData = reports[selectedReport];

  return (
    <div className="page-container">
      <div className="page-header">
        <h1>📊 Reports & Analytics</h1>
        <div className="report-actions">
          <button className="btn btn-sm" onClick={generatePDF}>📄 PDF</button>
          <button className="btn btn-sm" onClick={exportExcel}>📈 Excel</button>
          <button className="btn btn-sm" onClick={shareReport}>📤 Share</button>
        </div>
      </div>

      <div className="reports-controls">
        <div className="report-filters">
          <select 
            value={selectedReport} 
            onChange={(e) => setSelectedReport(e.target.value)}
            className="report-selector"
          >
            <option value="sales">📈 Sales Report</option>
            <option value="customers">👥 Customer Report</option>
            <option value="inventory">📦 Inventory Report</option>
            <option value="finance">💰 Financial Report</option>
          </select>

          <select 
            value={dateRange} 
            onChange={(e) => setDateRange(e.target.value)}
            className="date-range-selector"
          >
            <option value="last-7-days">Last 7 Days</option>
            <option value="last-30-days">Last 30 Days</option>
            <option value="last-3-months">Last 3 Months</option>
            <option value="last-year">Last Year</option>
            <option value="custom">Custom Range</option>
          </select>
        </div>
      </div>

      <div className="report-content">
        {selectedReport === 'sales' && (
          <div className="sales-report">
            <div className="report-summary">
              <div className="summary-card">
                <h3>Total Sales</h3>
                <p>₹{currentData.total.toLocaleString()}</p>
                <small className="positive">+{currentData.growth}% growth</small>
              </div>
              <div className="summary-card">
                <h3>Total Orders</h3>
                <p>{currentData.orders}</p>
                <small>This period</small>
              </div>
              <div className="summary-card">
                <h3>Avg Order Value</h3>
                <p>₹{currentData.avgOrderValue.toLocaleString()}</p>
                <small>Per order</small>
              </div>
            </div>

            <div className="chart-section">
              <h3>Sales Trend</h3>
              <div className="simple-bar-chart">
                {currentData.data.map((item, index) => (
                  <div key={index} className="bar-item">
                    <div 
                      className="bar" 
                      style={{height: `${(item.value / 150000) * 100}%`}}
                    ></div>
                    <span>{item.period}</span>
                    <small>₹{(item.value / 1000).toFixed(0)}K</small>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {selectedReport === 'customers' && (
          <div className="customers-report">
            <div className="report-summary">
              <div className="summary-card">
                <h3>Total Customers</h3>
                <p>{currentData.total}</p>
                <small>Active customers</small>
              </div>
              <div className="summary-card">
                <h3>New Customers</h3>
                <p>{currentData.newCustomers}</p>
                <small>This period</small>
              </div>
              <div className="summary-card">
                <h3>Retention Rate</h3>
                <p>{currentData.retentionRate}%</p>
                <small>Customer retention</small>
              </div>
              <div className="summary-card">
                <h3>Avg Lifetime Value</h3>
                <p>₹{currentData.avgLifetimeValue.toLocaleString()}</p>
                <small>Per customer</small>
              </div>
            </div>

            <div className="chart-section">
              <h3>New Customer Acquisition</h3>
              <div className="simple-bar-chart">
                {currentData.data.map((item, index) => (
                  <div key={index} className="bar-item">
                    <div 
                      className="bar customer-bar" 
                      style={{height: `${(item.value / 20) * 100}%`}}
                    ></div>
                    <span>{item.period}</span>
                    <small>{item.value} new</small>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {selectedReport === 'inventory' && (
          <div className="inventory-report">
            <div className="report-summary">
              <div className="summary-card">
                <h3>Total Products</h3>
                <p>{currentData.totalProducts}</p>
                <small>In inventory</small>
              </div>
              <div className="summary-card">
                <h3>Low Stock Items</h3>
                <p className="warning">{currentData.lowStockItems}</p>
                <small>Need attention</small>
              </div>
              <div className="summary-card">
                <h3>Out of Stock</h3>
                <p className="danger">{currentData.outOfStock}</p>
                <small>Items</small>
              </div>
              <div className="summary-card">
                <h3>Turnover Rate</h3>
                <p>{currentData.turnoverRate}x</p>
                <small>Times per year</small>
              </div>
            </div>

            <div className="chart-section">
              <h3>Stock by Category</h3>
              <div className="category-chart">
                {currentData.data.map((item, index) => (
                  <div key={index} className="category-item">
                    <span>{item.category}</span>
                    <div className="progress-bar">
                      <div 
                        className="progress" 
                        style={{width: `${(item.stock / 100) * 100}%`}}
                      ></div>
                    </div>
                    <span>{item.stock} items</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {selectedReport === 'finance' && (
          <div className="finance-report">
            <div className="report-summary">
              <div className="summary-card">
                <h3>Total Revenue</h3>
                <p>₹{currentData.revenue.toLocaleString()}</p>
                <small>This period</small>
              </div>
              <div className="summary-card">
                <h3>Total Expenses</h3>
                <p>₹{currentData.expenses.toLocaleString()}</p>
                <small>This period</small>
              </div>
              <div className="summary-card">
                <h3>Net Profit</h3>
                <p className="positive">₹{currentData.profit.toLocaleString()}</p>
                <small>This period</small>
              </div>
              <div className="summary-card">
                <h3>Profit Margin</h3>
                <p>{currentData.profitMargin}%</p>
                <small>Margin</small>
              </div>
            </div>

            <div className="chart-section">
              <h3>Revenue vs Expenses</h3>
              <div className="comparison-chart">
                {currentData.data.map((item, index) => (
                  <div key={index} className="comparison-item">
                    <span>{item.period}</span>
                    <div className="bars-container">
                      <div className="bar-group">
                        <div 
                          className="bar revenue-bar" 
                          style={{height: `${(item.revenue / 150000) * 100}%`}}
                        ></div>
                        <small>₹{(item.revenue / 1000).toFixed(0)}K</small>
                      </div>
                      <div className="bar-group">
                        <div 
                          className="bar expense-bar" 
                          style={{height: `${(item.expenses / 150000) * 100}%`}}
                        ></div>
                        <small>₹{(item.expenses / 1000).toFixed(0)}K</small>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}
      </div>

      <div className="report-insights">
        <h3>💡 Key Insights</h3>
        <div className="insights-grid">
          <div className="insight-item">
            <h4>Performance Trend</h4>
            <p>Sales have increased by 12.5% compared to the previous period, showing strong business growth.</p>
          </div>
          <div className="insight-item">
            <h4>Customer Behavior</h4>
            <p>Customer retention rate is above industry average at 78.5%, indicating good customer satisfaction.</p>
          </div>
          <div className="insight-item">
            <h4>Operational Efficiency</h4>
            <p>12 items are running low on stock. Consider restocking to avoid potential sales loss.</p>
          </div>
          <div className="insight-item">
            <h4>Financial Health</h4>
            <p>Profit margin of 34% is healthy. Consider investing in growth opportunities.</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Reports;