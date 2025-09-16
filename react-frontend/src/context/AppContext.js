import React, { createContext, useContext, useReducer, useEffect } from 'react';
import toast from 'react-hot-toast';

  // Initial state
const initialState = {
  user: {
    name: 'Rajesh Kumar',
    business: 'Kumar Electronics',
    role: 'Owner',
    avatar: null
  },
  business: {
    name: 'Kumar Electronics',
    type: 'retail',
    currency: 'INR',
    language: 'hi',
    gstEnabled: true
  },
  dashboard: {
    totalSales: 0,
    totalCustomers: 0,
    totalProducts: 0,
    monthlyRevenue: 0,
    salesData: [],
    recentTransactions: []
  },
  inventory: [],
  customers: [],
  loading: false,
  error: null,
  apiBaseUrl: window.location.hostname === 'localhost' ? 'http://localhost:8000' : '/api'
};

// Action types
const ActionTypes = {
  SET_LOADING: 'SET_LOADING',
  SET_ERROR: 'SET_ERROR',
  UPDATE_DASHBOARD: 'UPDATE_DASHBOARD',
  UPDATE_INVENTORY: 'UPDATE_INVENTORY',
  ADD_INVENTORY_ITEM: 'ADD_INVENTORY_ITEM',
  UPDATE_INVENTORY_ITEM: 'UPDATE_INVENTORY_ITEM',
  DELETE_INVENTORY_ITEM: 'DELETE_INVENTORY_ITEM',
  UPDATE_CUSTOMERS: 'UPDATE_CUSTOMERS',
  ADD_CUSTOMER: 'ADD_CUSTOMER',
  UPDATE_CUSTOMER: 'UPDATE_CUSTOMER',
  DELETE_CUSTOMER: 'DELETE_CUSTOMER',
  UPDATE_BUSINESS_PROFILE: 'UPDATE_BUSINESS_PROFILE'
};

// Reducer
const appReducer = (state, action) => {
  switch (action.type) {
    case ActionTypes.SET_LOADING:
      return { ...state, loading: action.payload };
    
    case ActionTypes.SET_ERROR:
      return { ...state, error: action.payload, loading: false };
    
    case ActionTypes.UPDATE_DASHBOARD:
      return { ...state, dashboard: { ...state.dashboard, ...action.payload } };
    
    case ActionTypes.UPDATE_INVENTORY:
      return { ...state, inventory: action.payload };
    
    case ActionTypes.ADD_INVENTORY_ITEM:
      return { ...state, inventory: [...state.inventory, action.payload] };
    
    case ActionTypes.UPDATE_INVENTORY_ITEM:
      return {
        ...state,
        inventory: state.inventory.map(item =>
          item.id === action.payload.id ? { ...item, ...action.payload } : item
        )
      };
    
    case ActionTypes.DELETE_INVENTORY_ITEM:
      return {
        ...state,
        inventory: state.inventory.filter(item => item.id !== action.payload)
      };
    
    case ActionTypes.UPDATE_CUSTOMERS:
      return { ...state, customers: action.payload };
    
    case ActionTypes.ADD_CUSTOMER:
      return { ...state, customers: [...state.customers, action.payload] };
    
    case ActionTypes.UPDATE_CUSTOMER:
      return {
        ...state,
        customers: state.customers.map(customer =>
          customer.id === action.payload.id ? { ...customer, ...action.payload } : customer
        )
      };
    
    case ActionTypes.DELETE_CUSTOMER:
      return {
        ...state,
        customers: state.customers.filter(customer => customer.id !== action.payload)
      };
    
    case ActionTypes.UPDATE_BUSINESS_PROFILE:
      return { ...state, business: { ...state.business, ...action.payload } };
    
    default:
      return state;
  }
};

// Context
const AppContext = createContext();

// Provider component
export const AppProvider = ({ children }) => {
  const [state, dispatch] = useReducer(appReducer, initialState);

  // API helper function
  const apiCall = async (endpoint, options = {}) => {
    try {
      const response = await fetch(`${state.apiBaseUrl}${endpoint}`, {
        headers: {
          'Content-Type': 'application/json',
          ...options.headers
        },
        ...options
      });

      if (!response.ok) {
        throw new Error(`API Error: ${response.status} ${response.statusText}`);
      }

      return await response.json();
    } catch (error) {
      console.error('API Call Error:', error);
      throw error;
    }
  };

  // Action creators
  const actions = {
    setLoading: (loading) => dispatch({ type: ActionTypes.SET_LOADING, payload: loading }),
    
    setError: (error) => {
      dispatch({ type: ActionTypes.SET_ERROR, payload: error });
      if (error) {
        toast.error(error);
      }
    },

    // Dashboard actions
    fetchDashboardData: async () => {
      try {
        actions.setLoading(true);
        const data = await apiCall('/dashboard');
        dispatch({ type: ActionTypes.UPDATE_DASHBOARD, payload: data });
      } catch (error) {
        actions.setError('Failed to fetch dashboard data');
      } finally {
        actions.setLoading(false);
      }
    },

    // Inventory actions
    fetchInventory: async () => {
      try {
        actions.setLoading(true);
        const data = await apiCall('/inventory');
        dispatch({ type: ActionTypes.UPDATE_INVENTORY, payload: data });
      } catch (error) {
        actions.setError('Failed to fetch inventory');
      } finally {
        actions.setLoading(false);
      }
    },

    addInventoryItem: async (item) => {
      try {
        const newItem = await apiCall('/inventory', {
          method: 'POST',
          body: JSON.stringify(item)
        });
        dispatch({ type: ActionTypes.ADD_INVENTORY_ITEM, payload: newItem });
        toast.success('Inventory item added successfully');
      } catch (error) {
        actions.setError('Failed to add inventory item');
      }
    },

    updateInventoryItem: async (id, updates) => {
      try {
        const updatedItem = await apiCall(`/inventory/${id}`, {
          method: 'PUT',
          body: JSON.stringify(updates)
        });
        dispatch({ type: ActionTypes.UPDATE_INVENTORY_ITEM, payload: updatedItem });
        toast.success('Inventory item updated successfully');
      } catch (error) {
        actions.setError('Failed to update inventory item');
      }
    },

    deleteInventoryItem: async (id) => {
      try {
        await apiCall(`/inventory/${id}`, { method: 'DELETE' });
        dispatch({ type: ActionTypes.DELETE_INVENTORY_ITEM, payload: id });
        toast.success('Inventory item deleted successfully');
      } catch (error) {
        actions.setError('Failed to delete inventory item');
      }
    },

    // Customer actions
    fetchCustomers: async () => {
      try {
        actions.setLoading(true);
        const data = await apiCall('/customers');
        dispatch({ type: ActionTypes.UPDATE_CUSTOMERS, payload: data });
      } catch (error) {
        actions.setError('Failed to fetch customers');
      } finally {
        actions.setLoading(false);
      }
    },

    addCustomer: async (customer) => {
      try {
        const newCustomer = await apiCall('/customers', {
          method: 'POST',
          body: JSON.stringify(customer)
        });
        dispatch({ type: ActionTypes.ADD_CUSTOMER, payload: newCustomer });
        toast.success('Customer added successfully');
      } catch (error) {
        actions.setError('Failed to add customer');
      }
    },

    updateCustomer: async (id, updates) => {
      try {
        const updatedCustomer = await apiCall(`/customers/${id}`, {
          method: 'PUT',
          body: JSON.stringify(updates)
        });
        dispatch({ type: ActionTypes.UPDATE_CUSTOMER, payload: updatedCustomer });
        toast.success('Customer updated successfully');
      } catch (error) {
        actions.setError('Failed to update customer');
      }
    },

    deleteCustomer: async (id) => {
      try {
        await apiCall(`/customers/${id}`, { method: 'DELETE' });
        dispatch({ type: ActionTypes.DELETE_CUSTOMER, payload: id });
        toast.success('Customer deleted successfully');
      } catch (error) {
        actions.setError('Failed to delete customer');
      }
    },

    // Business profile actions
    updateBusinessProfile: async (updates) => {
      try {
        const updatedProfile = await apiCall('/business/profile', {
          method: 'POST',
          body: JSON.stringify(updates)
        });
        dispatch({ type: ActionTypes.UPDATE_BUSINESS_PROFILE, payload: updatedProfile });
        toast.success('Business profile updated successfully');
      } catch (error) {
        actions.setError('Failed to update business profile');
      }
    }
  };

  // Load initial data
  useEffect(() => {
    actions.fetchDashboardData();
  }, [actions]);

  const value = {
    state,
    actions,
    apiCall
  };

  return (
    <AppContext.Provider value={value}>
      {children}
    </AppContext.Provider>
  );
};

// Hook to use the context
export const useAppContext = () => {
  const context = useContext(AppContext);
  if (!context) {
    throw new Error('useAppContext must be used within an AppProvider');
  }
  return context;
};

export default AppProvider;