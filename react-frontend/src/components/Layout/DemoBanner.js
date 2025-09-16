import React from 'react';
import { useAppContext } from '../../context/AppContext';
import './DemoBanner.css';

const DemoBanner = () => {
  const { state } = useAppContext();

  if (state.apiConnected) return null;

  return (
    <div className="demo-banner">
      <div className="demo-banner-content">
        <i className="fas fa-info-circle"></i>
        <span>
          🚀 Demo Mode: This is a preview version with sample data. 
          Some features are limited in demo mode.
        </span>
      </div>
    </div>
  );
};

export default DemoBanner;