import React from 'react';

// Simple placeholder components for now
export const SalesChart = ({ data }) => (
  <div className="chart-widget">
    <h3>Sales Chart</h3>
    <p>Chart implementation coming soon...</p>
  </div>
);

export const RevenueChart = ({ data }) => (
  <div className="chart-widget">
    <h3>Revenue Chart</h3>
    <p>Chart implementation coming soon...</p>
  </div>
);

export const RecentTransactions = ({ transactions }) => (
  <div className="transactions-widget">
    <h3>Recent Transactions</h3>
    <p>Transactions list coming soon...</p>
  </div>
);

export const TopProducts = ({ products }) => (
  <div className="products-widget">
    <h3>Top Products</h3>
    <p>Products list coming soon...</p>
  </div>
);