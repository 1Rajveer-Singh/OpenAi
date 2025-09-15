import React from 'react';
import './DashboardCard.css';

const DashboardCard = ({ title, titleHi, value, change, changeType, icon, color }) => {
  return (
    <div className={`dashboard-card ${color}`}>
      <div className="card-header">
        <div className="card-icon">
          <i className={icon}></i>
        </div>
        <div className="card-titles">
          <h3 className="card-title">{title}</h3>
          <span className="card-title-hi">{titleHi}</span>
        </div>
      </div>
      
      <div className="card-content">
        <div className="card-value">{value}</div>
        <div className={`card-change ${changeType}`}>
          <i className={`fas ${changeType === 'positive' ? 'fa-arrow-up' : 'fa-arrow-down'}`}></i>
          <span>{change}</span>
        </div>
      </div>
    </div>
  );
};

export default DashboardCard;