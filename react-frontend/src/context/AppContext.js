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
    totalSales: 150000,
    totalCustomers: 1250,
    totalProducts: 450,
    monthlyRevenue: 2500000,
    salesData: [
      { month: 'Jan', sales: 180000 },
      { month: 'Feb', sales: 220000 },
      { month: 'Mar', sales: 190000 },
      { month: 'Apr', sales: 250000 },
      { month: 'May', sales: 280000 },
      { month: 'Jun', sales: 150000 }
    ],
    recentTransactions: [
      { id: 1, customer: 'Priya Sharma', amount: 15500, status: 'completed', date: '2024-01-15' },
      { id: 2, customer: 'Amit Patel', amount: 8900, status: 'pending', date: '2024-01-14' },
      { id: 3, customer: 'Sunita Devi', amount: 12000, status: 'completed', date: '2024-01-14' }
    ]
  },
  inventory: [
    { id: 1, name: 'iPhone 15 Pro', stock: 25, price: 129900, category: 'Electronics' },
    { id: 2, name: 'Samsung Galaxy S24', stock: 30, price: 89900, category: 'Electronics' },
    { id: 3, name: 'MacBook Air M3', stock: 10, price: 114900, category: 'Computers' }
  ],
  customers: [
    { id: 1, name: 'Priya Sharma', phone: '+91 98765 43210', email: 'priya@email.com', totalOrders: 15 },
    { id: 2, name: 'Amit Patel', phone: '+91 87654 32109', email: 'amit@email.com', totalOrders: 8 },
    { id: 3, name: 'Sunita Devi', phone: '+91 76543 21098', email: 'sunita@email.com', totalOrders: 12 }
  ],
  loading: false,
  error: null,
  apiConnected: false,
  apiBaseUrl: window.location.hostname === 'localhost' ? 'http://localhost:8000' : null
};

// Action types
const ActionTypes = {
  SET_LOADING: 'SET_LOADING',
  SET_ERROR: 'SET_ERROR',
  SET_API_CONNECTION: 'SET_API_CONNECTION',
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
    
    case ActionTypes.SET_API_CONNECTION:
      return { ...state, apiConnected: action.payload };
    
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
    // Get current apiBaseUrl from state
    const currentApiBaseUrl = window.location.hostname === 'localhost' ? 'http://localhost:8000' : null;
    
    // If no API base URL (production), return null to use fallback data
    if (!currentApiBaseUrl) {
      console.log('API not available, using fallback data');
      return null;
    }

    try {
      const response = await fetch(`${currentApiBaseUrl}${endpoint}`, {
        headers: {
          'Content-Type': 'application/json',
          ...options.headers
        },
        ...options
      });

      if (!response.ok) {
        throw new Error(`API Error: ${response.status} ${response.statusText}`);
      }

      dispatch({ type: ActionTypes.SET_API_CONNECTION, payload: true });
      return await response.json();
    } catch (error) {
      console.error('API Call Error:', error);
      dispatch({ type: ActionTypes.SET_API_CONNECTION, payload: false });
      // Don't throw error, return null to use fallback data
      return null;
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

    setApiConnection: (connected) => dispatch({ type: ActionTypes.SET_API_CONNECTION, payload: connected }),

    // Dashboard actions
    fetchDashboardData: async () => {
      try {
        actions.setLoading(true);
        const data = await apiCall('/api/dashboard');
        
        // If API call returns null (API not available), use existing fallback data
        if (data) {
          dispatch({ type: ActionTypes.UPDATE_DASHBOARD, payload: data });
        } else {
          console.log('Using fallback dashboard data');
        }
      } catch (error) {
        console.log('API not available, using fallback data');
        // Don't show error to user, just use fallback data
      } finally {
        actions.setLoading(false);
      }
    },

    // Inventory actions
    fetchInventory: async () => {
      try {
        actions.setLoading(true);
        const data = await apiCall('/api/inventory');
        
        if (data) {
          dispatch({ type: ActionTypes.UPDATE_INVENTORY, payload: data });
        } else {
          console.log('Using fallback inventory data');
        }
      } catch (error) {
        console.log('API not available, using fallback data');
      } finally {
        actions.setLoading(false);
      }
    },

    addInventoryItem: async (item) => {
      if (!state.apiConnected) {
        toast.error('Feature not available in demo mode');
        return;
      }
      
      try {
        const newItem = await apiCall('/api/inventory', {
          method: 'POST',
          body: JSON.stringify(item)
        });
        
        if (newItem) {
          dispatch({ type: ActionTypes.ADD_INVENTORY_ITEM, payload: newItem });
          toast.success('Inventory item added successfully');
        }
      } catch (error) {
        actions.setError('Failed to add inventory item');
      }
    },

    updateInventoryItem: async (id, updates) => {
      if (!state.apiConnected) {
        toast.error('Feature not available in demo mode');
        return;
      }
      
      try {
        const updatedItem = await apiCall(`/api/inventory/${id}`, {
          method: 'PUT',
          body: JSON.stringify(updates)
        });
        
        if (updatedItem) {
          dispatch({ type: ActionTypes.UPDATE_INVENTORY_ITEM, payload: updatedItem });
          toast.success('Inventory item updated successfully');
        }
      } catch (error) {
        actions.setError('Failed to update inventory item');
      }
    },

    deleteInventoryItem: async (id) => {
      if (!state.apiConnected) {
        toast.error('Feature not available in demo mode');
        return;
      }
      
      try {
        await apiCall(`/api/inventory/${id}`, { method: 'DELETE' });
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
        const data = await apiCall('/api/customers');
        
        if (data) {
          dispatch({ type: ActionTypes.UPDATE_CUSTOMERS, payload: data });
        } else {
          console.log('Using fallback customer data');
        }
      } catch (error) {
        console.log('API not available, using fallback data');
      } finally {
        actions.setLoading(false);
      }
    },

    addCustomer: async (customer) => {
      if (!state.apiConnected) {
        toast.error('Feature not available in demo mode');
        return;
      }
      
      try {
        const newCustomer = await apiCall('/api/customers', {
          method: 'POST',
          body: JSON.stringify(customer)
        });
        
        if (newCustomer) {
          dispatch({ type: ActionTypes.ADD_CUSTOMER, payload: newCustomer });
          toast.success('Customer added successfully');
        }
      } catch (error) {
        actions.setError('Failed to add customer');
      }
    },

    updateCustomer: async (id, updates) => {
      if (!state.apiConnected) {
        toast.error('Feature not available in demo mode');
        return;
      }
      
      try {
        const updatedCustomer = await apiCall(`/api/customers/${id}`, {
          method: 'PUT',
          body: JSON.stringify(updates)
        });
        
        if (updatedCustomer) {
          dispatch({ type: ActionTypes.UPDATE_CUSTOMER, payload: updatedCustomer });
          toast.success('Customer updated successfully');
        }
      } catch (error) {
        actions.setError('Failed to update customer');
      }
    },

    deleteCustomer: async (id) => {
      if (!state.apiConnected) {
        toast.error('Feature not available in demo mode');
        return;
      }
      
      try {
        await apiCall(`/api/customers/${id}`, { method: 'DELETE' });
        dispatch({ type: ActionTypes.DELETE_CUSTOMER, payload: id });
        toast.success('Customer deleted successfully');
      } catch (error) {
        actions.setError('Failed to delete customer');
      }
    },

    // Business profile actions
    updateBusinessProfile: async (updates) => {
      if (!state.apiConnected) {
        toast.error('Feature not available in demo mode');
        return;
      }
      
      try {
        const updatedProfile = await apiCall('/api/business/profile', {
          method: 'POST',
          body: JSON.stringify(updates)
        });
        
        if (updatedProfile) {
          dispatch({ type: ActionTypes.UPDATE_BUSINESS_PROFILE, payload: updatedProfile });
          toast.success('Business profile updated successfully');
        }
      } catch (error) {
        actions.setError('Failed to update business profile');
      }
    }
  };

  // Load initial data
  useEffect(() => {
    // Only fetch dashboard data once on component mount
    const loadInitialData = async () => {
      try {
        if (state.apiBaseUrl) {
          const data = await apiCall('/api/dashboard');
          if (data) {
            dispatch({ type: ActionTypes.UPDATE_DASHBOARD, payload: data });
            dispatch({ type: ActionTypes.SET_API_CONNECTION, payload: true });
          }
        }
      } catch (error) {
        console.log('API not available, using fallback data');
        dispatch({ type: ActionTypes.SET_API_CONNECTION, payload: false });
      }
    };
    
    loadInitialData();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []); // Empty dependency array to run only once

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