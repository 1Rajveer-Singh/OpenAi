import React, { useState, useEffect } from 'react';
import { useAppContext } from '../context/AppContext';
import './Pages.css';

const Inventory = () => {
  const { state, actions } = useAppContext();
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showAddProduct, setShowAddProduct] = useState(false);
  const [newProduct, setNewProduct] = useState({
    name: '',
    category: '',
    price: '',
    stock: '',
    minStock: ''
  });

  useEffect(() => {
    fetchInventory();
  }, []);

  const fetchInventory = async () => {
    try {
      // Simulate API call
      setTimeout(() => {
        setProducts([
          { id: 1, name: 'Product A', category: 'Electronics', price: 299, stock: 50, minStock: 10 },
          { id: 2, name: 'Product B', category: 'Clothing', price: 49, stock: 25, minStock: 5 },
          { id: 3, name: 'Product C', category: 'Home', price: 129, stock: 8, minStock: 15 }
        ]);
        setLoading(false);
      }, 1000);
    } catch (error) {
      console.error('Error fetching inventory:', error);
      setLoading(false);
    }
  };

  const handleAddProduct = (e) => {
    e.preventDefault();
    const product = {
      id: Date.now(),
      ...newProduct,
      price: parseFloat(newProduct.price),
      stock: parseInt(newProduct.stock),
      minStock: parseInt(newProduct.minStock)
    };
    setProducts([...products, product]);
    setNewProduct({ name: '', category: '', price: '', stock: '', minStock: '' });
    setShowAddProduct(false);
  };

  const getStockStatus = (stock, minStock) => {
    if (stock <= minStock) return 'low';
    if (stock <= minStock * 2) return 'medium';
    return 'high';
  };

  if (loading) {
    return (
      <div className="page-container">
        <div className="loading-spinner">Loading inventory...</div>
      </div>
    );
  }

  return (
    <div className="page-container">
      <div className="page-header">
        <h1>📦 Inventory Management</h1>
        <button 
          className="btn btn-primary"
          onClick={() => setShowAddProduct(true)}
        >
          Add Product
        </button>
      </div>

      <div className="inventory-stats">
        <div className="stat-card">
          <h3>Total Products</h3>
          <p>{products.length}</p>
        </div>
        <div className="stat-card">
          <h3>Low Stock Items</h3>
          <p>{products.filter(p => p.stock <= p.minStock).length}</p>
        </div>
        <div className="stat-card">
          <h3>Total Value</h3>
          <p>₹{products.reduce((sum, p) => sum + (p.price * p.stock), 0).toLocaleString()}</p>
        </div>
      </div>

      <div className="inventory-table">
        <table>
          <thead>
            <tr>
              <th>Product Name</th>
              <th>Category</th>
              <th>Price</th>
              <th>Current Stock</th>
              <th>Min Stock</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {products.map(product => (
              <tr key={product.id}>
                <td>{product.name}</td>
                <td>{product.category}</td>
                <td>₹{product.price}</td>
                <td>{product.stock}</td>
                <td>{product.minStock}</td>
                <td>
                  <span className={`stock-status ${getStockStatus(product.stock, product.minStock)}`}>
                    {getStockStatus(product.stock, product.minStock)}
                  </span>
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

      {showAddProduct && (
        <div className="modal-overlay">
          <div className="modal">
            <h2>Add New Product</h2>
            <form onSubmit={handleAddProduct}>
              <input
                type="text"
                placeholder="Product Name"
                value={newProduct.name}
                onChange={(e) => setNewProduct({...newProduct, name: e.target.value})}
                required
              />
              <input
                type="text"
                placeholder="Category"
                value={newProduct.category}
                onChange={(e) => setNewProduct({...newProduct, category: e.target.value})}
                required
              />
              <input
                type="number"
                placeholder="Price"
                value={newProduct.price}
                onChange={(e) => setNewProduct({...newProduct, price: e.target.value})}
                required
              />
              <input
                type="number"
                placeholder="Stock Quantity"
                value={newProduct.stock}
                onChange={(e) => setNewProduct({...newProduct, stock: e.target.value})}
                required
              />
              <input
                type="number"
                placeholder="Minimum Stock"
                value={newProduct.minStock}
                onChange={(e) => setNewProduct({...newProduct, minStock: e.target.value})}
                required
              />
              <div className="modal-actions">
                <button type="submit" className="btn btn-primary">Add Product</button>
                <button type="button" className="btn" onClick={() => setShowAddProduct(false)}>Cancel</button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default Inventory;