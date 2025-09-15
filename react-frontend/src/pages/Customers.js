import React, { useState, useEffect } from 'react';
import { useAppContext } from '../context/AppContext';
import './Pages.css';

const Customers = () => {
  const { state, actions } = useAppContext();
  const [customers, setCustomers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showAddCustomer, setShowAddCustomer] = useState(false);
  const [newCustomer, setNewCustomer] = useState({
    name: '',
    email: '',
    phone: '',
    company: '',
    address: ''
  });

  useEffect(() => {
    fetchCustomers();
  }, []);

  const fetchCustomers = async () => {
    try {
      // Simulate API call
      setTimeout(() => {
        setCustomers([
          { 
            id: 1, 
            name: 'Rajesh Kumar', 
            email: 'rajesh@example.com', 
            phone: '+91 98765 43210', 
            company: 'Tech Solutions Ltd',
            address: 'Mumbai, Maharashtra',
            totalOrders: 15,
            totalSpent: 45000,
            lastOrder: '2025-09-10'
          },
          { 
            id: 2, 
            name: 'Priya Sharma', 
            email: 'priya@example.com', 
            phone: '+91 87654 32109', 
            company: 'Fashion Hub',
            address: 'Delhi, NCR',
            totalOrders: 8,
            totalSpent: 22000,
            lastOrder: '2025-09-12'
          },
          { 
            id: 3, 
            name: 'Amit Patel', 
            email: 'amit@example.com', 
            phone: '+91 76543 21098', 
            company: 'Home Decor Plus',
            address: 'Bangalore, Karnataka',
            totalOrders: 22,
            totalSpent: 67000,
            lastOrder: '2025-09-14'
          }
        ]);
        setLoading(false);
      }, 1000);
    } catch (error) {
      console.error('Error fetching customers:', error);
      setLoading(false);
    }
  };

  const handleAddCustomer = (e) => {
    e.preventDefault();
    const customer = {
      id: Date.now(),
      ...newCustomer,
      totalOrders: 0,
      totalSpent: 0,
      lastOrder: new Date().toISOString().split('T')[0]
    };
    setCustomers([...customers, customer]);
    setNewCustomer({ name: '', email: '', phone: '', company: '', address: '' });
    setShowAddCustomer(false);
  };

  const getCustomerTier = (totalSpent) => {
    if (totalSpent >= 50000) return 'Premium';
    if (totalSpent >= 20000) return 'Gold';
    return 'Silver';
  };

  if (loading) {
    return (
      <div className="page-container">
        <div className="loading-spinner">Loading customers...</div>
      </div>
    );
  }

  return (
    <div className="page-container">
      <div className="page-header">
        <h1>👥 Customer Management</h1>
        <button 
          className="btn btn-primary"
          onClick={() => setShowAddCustomer(true)}
        >
          Add Customer
        </button>
      </div>

      <div className="customer-stats">
        <div className="stat-card">
          <h3>Total Customers</h3>
          <p>{customers.length}</p>
        </div>
        <div className="stat-card">
          <h3>Premium Customers</h3>
          <p>{customers.filter(c => c.totalSpent >= 50000).length}</p>
        </div>
        <div className="stat-card">
          <h3>Total Revenue</h3>
          <p>₹{customers.reduce((sum, c) => sum + c.totalSpent, 0).toLocaleString()}</p>
        </div>
        <div className="stat-card">
          <h3>Average Order Value</h3>
          <p>₹{Math.round(customers.reduce((sum, c) => sum + c.totalSpent, 0) / customers.reduce((sum, c) => sum + c.totalOrders, 1)).toLocaleString()}</p>
        </div>
      </div>

      <div className="customers-table">
        <table>
          <thead>
            <tr>
              <th>Customer Name</th>
              <th>Email</th>
              <th>Phone</th>
              <th>Company</th>
              <th>Total Orders</th>
              <th>Total Spent</th>
              <th>Tier</th>
              <th>Last Order</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {customers.map(customer => (
              <tr key={customer.id}>
                <td>{customer.name}</td>
                <td>{customer.email}</td>
                <td>{customer.phone}</td>
                <td>{customer.company}</td>
                <td>{customer.totalOrders}</td>
                <td>₹{customer.totalSpent.toLocaleString()}</td>
                <td>
                  <span className={`customer-tier ${getCustomerTier(customer.totalSpent).toLowerCase()}`}>
                    {getCustomerTier(customer.totalSpent)}
                  </span>
                </td>
                <td>{customer.lastOrder}</td>
                <td>
                  <button className="btn btn-sm">View</button>
                  <button className="btn btn-sm">Edit</button>
                  <button className="btn btn-sm btn-danger">Delete</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {showAddCustomer && (
        <div className="modal-overlay">
          <div className="modal">
            <h2>Add New Customer</h2>
            <form onSubmit={handleAddCustomer}>
              <input
                type="text"
                placeholder="Customer Name"
                value={newCustomer.name}
                onChange={(e) => setNewCustomer({...newCustomer, name: e.target.value})}
                required
              />
              <input
                type="email"
                placeholder="Email Address"
                value={newCustomer.email}
                onChange={(e) => setNewCustomer({...newCustomer, email: e.target.value})}
                required
              />
              <input
                type="tel"
                placeholder="Phone Number"
                value={newCustomer.phone}
                onChange={(e) => setNewCustomer({...newCustomer, phone: e.target.value})}
                required
              />
              <input
                type="text"
                placeholder="Company"
                value={newCustomer.company}
                onChange={(e) => setNewCustomer({...newCustomer, company: e.target.value})}
              />
              <textarea
                placeholder="Address"
                value={newCustomer.address}
                onChange={(e) => setNewCustomer({...newCustomer, address: e.target.value})}
                rows="3"
              />
              <div className="modal-actions">
                <button type="submit" className="btn btn-primary">Add Customer</button>
                <button type="button" className="btn" onClick={() => setShowAddCustomer(false)}>Cancel</button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default Customers;