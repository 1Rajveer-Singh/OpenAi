import React, { useState, useEffect } from 'react';
import { useAppContext } from '../context/AppContext';
import './Pages.css';

const Finance = () => {
  const { state, actions } = useAppContext();
  const [financialData, setFinancialData] = useState({});
  const [transactions, setTransactions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showAddTransaction, setShowAddTransaction] = useState(false);
  const [newTransaction, setNewTransaction] = useState({
    type: 'income',
    amount: '',
    description: '',
    category: '',
    date: new Date().toISOString().split('T')[0]
  });

  useEffect(() => {
    fetchFinancialData();
  }, []);

  const fetchFinancialData = async () => {
    try {
      // Simulate API call
      setTimeout(() => {
        const mockTransactions = [
          { id: 1, type: 'income', amount: 25000, description: 'Product Sales', category: 'Sales', date: '2025-09-15' },
          { id: 2, type: 'expense', amount: 5000, description: 'Office Rent', category: 'Rent', date: '2025-09-14' },
          { id: 3, type: 'income', amount: 15000, description: 'Service Revenue', category: 'Services', date: '2025-09-13' },
          { id: 4, type: 'expense', amount: 2000, description: 'Marketing Campaign', category: 'Marketing', date: '2025-09-12' },
          { id: 5, type: 'expense', amount: 3000, description: 'Supplies Purchase', category: 'Supplies', date: '2025-09-11' }
        ];

        const totalIncome = mockTransactions.filter(t => t.type === 'income').reduce((sum, t) => sum + t.amount, 0);
        const totalExpenses = mockTransactions.filter(t => t.type === 'expense').reduce((sum, t) => sum + t.amount, 0);
        const netProfit = totalIncome - totalExpenses;

        setTransactions(mockTransactions);
        setFinancialData({
          totalIncome,
          totalExpenses,
          netProfit,
          cashFlow: netProfit > 0 ? 'positive' : 'negative',
          profitMargin: ((netProfit / totalIncome) * 100).toFixed(2)
        });
        setLoading(false);
      }, 1000);
    } catch (error) {
      console.error('Error fetching financial data:', error);
      setLoading(false);
    }
  };

  const handleAddTransaction = (e) => {
    e.preventDefault();
    const transaction = {
      id: Date.now(),
      ...newTransaction,
      amount: parseFloat(newTransaction.amount)
    };
    setTransactions([transaction, ...transactions]);
    setNewTransaction({
      type: 'income',
      amount: '',
      description: '',
      category: '',
      date: new Date().toISOString().split('T')[0]
    });
    setShowAddTransaction(false);
    
    // Recalculate financial data
    const updatedTransactions = [transaction, ...transactions];
    const totalIncome = updatedTransactions.filter(t => t.type === 'income').reduce((sum, t) => sum + t.amount, 0);
    const totalExpenses = updatedTransactions.filter(t => t.type === 'expense').reduce((sum, t) => sum + t.amount, 0);
    const netProfit = totalIncome - totalExpenses;
    
    setFinancialData({
      totalIncome,
      totalExpenses,
      netProfit,
      cashFlow: netProfit > 0 ? 'positive' : 'negative',
      profitMargin: totalIncome > 0 ? ((netProfit / totalIncome) * 100).toFixed(2) : '0'
    });
  };

  if (loading) {
    return (
      <div className="page-container">
        <div className="loading-spinner">Loading financial data...</div>
      </div>
    );
  }

  return (
    <div className="page-container">
      <div className="page-header">
        <h1>💰 Finance Dashboard</h1>
        <button 
          className="btn btn-primary"
          onClick={() => setShowAddTransaction(true)}
        >
          Add Transaction
        </button>
      </div>

      <div className="finance-overview">
        <div className="stat-card income">
          <h3>Total Income</h3>
          <p>₹{financialData.totalIncome?.toLocaleString()}</p>
          <small>This month</small>
        </div>
        <div className="stat-card expense">
          <h3>Total Expenses</h3>
          <p>₹{financialData.totalExpenses?.toLocaleString()}</p>
          <small>This month</small>
        </div>
        <div className={`stat-card ${financialData.netProfit >= 0 ? 'profit' : 'loss'}`}>
          <h3>Net Profit</h3>
          <p>₹{financialData.netProfit?.toLocaleString()}</p>
          <small>{financialData.profitMargin}% margin</small>
        </div>
        <div className={`stat-card ${financialData.cashFlow}`}>
          <h3>Cash Flow</h3>
          <p className={financialData.cashFlow}>
            {financialData.cashFlow === 'positive' ? '↗️ Positive' : '↘️ Negative'}
          </p>
          <small>Current trend</small>
        </div>
      </div>

      <div className="finance-charts">
        <div className="chart-container">
          <h3>Income vs Expenses (Last 7 Days)</h3>
          <div className="simple-chart">
            <div className="chart-bar">
              <div className="bar income-bar" style={{height: '60%'}}></div>
              <span>Income</span>
            </div>
            <div className="chart-bar">
              <div className="bar expense-bar" style={{height: '35%'}}></div>
              <span>Expenses</span>
            </div>
          </div>
        </div>

        <div className="chart-container">
          <h3>Category Breakdown</h3>
          <div className="category-breakdown">
            <div className="category-item">
              <span>Sales</span>
              <div className="progress-bar">
                <div className="progress" style={{width: '65%'}}></div>
              </div>
              <span>65%</span>
            </div>
            <div className="category-item">
              <span>Services</span>
              <div className="progress-bar">
                <div className="progress" style={{width: '35%'}}></div>
              </div>
              <span>35%</span>
            </div>
          </div>
        </div>
      </div>

      <div className="transactions-section">
        <h3>Recent Transactions</h3>
        <div className="transactions-table">
          <table>
            <thead>
              <tr>
                <th>Date</th>
                <th>Type</th>
                <th>Description</th>
                <th>Category</th>
                <th>Amount</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {transactions.map(transaction => (
                <tr key={transaction.id}>
                  <td>{transaction.date}</td>
                  <td>
                    <span className={`transaction-type ${transaction.type}`}>
                      {transaction.type === 'income' ? '↗️' : '↘️'} {transaction.type}
                    </span>
                  </td>
                  <td>{transaction.description}</td>
                  <td>{transaction.category}</td>
                  <td className={transaction.type}>
                    {transaction.type === 'income' ? '+' : '-'}₹{transaction.amount.toLocaleString()}
                  </td>
                  <td>
                    <button className="btn btn-sm">Edit</button>
                    <button className="btn btn-sm btn-danger">Delete</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {showAddTransaction && (
        <div className="modal-overlay">
          <div className="modal">
            <h2>Add New Transaction</h2>
            <form onSubmit={handleAddTransaction}>
              <select
                value={newTransaction.type}
                onChange={(e) => setNewTransaction({...newTransaction, type: e.target.value})}
                required
              >
                <option value="income">Income</option>
                <option value="expense">Expense</option>
              </select>
              
              <input
                type="number"
                placeholder="Amount"
                value={newTransaction.amount}
                onChange={(e) => setNewTransaction({...newTransaction, amount: e.target.value})}
                required
              />
              
              <input
                type="text"
                placeholder="Description"
                value={newTransaction.description}
                onChange={(e) => setNewTransaction({...newTransaction, description: e.target.value})}
                required
              />
              
              <input
                type="text"
                placeholder="Category"
                value={newTransaction.category}
                onChange={(e) => setNewTransaction({...newTransaction, category: e.target.value})}
                required
              />
              
              <input
                type="date"
                value={newTransaction.date}
                onChange={(e) => setNewTransaction({...newTransaction, date: e.target.value})}
                required
              />
              
              <div className="modal-actions">
                <button type="submit" className="btn btn-primary">Add Transaction</button>
                <button type="button" className="btn" onClick={() => setShowAddTransaction(false)}>Cancel</button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default Finance;