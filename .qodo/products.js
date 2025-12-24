// pages/Products.js
import React, { useState } from 'react';
import { ShoppingCart, Star, Filter } from 'lucide-react';

const Products = () => {
  const [products] = useState([
    {
      id: 1,
      name: "Premium Dumbbell Set",
      price: 299.99,
      image: "https://via.placeholder.com/300x200?text=Dumbbells",
      category: "weights",
      rating: 4.8,
      description: "Adjustable dumbbell set from 5-50 lbs"
    },
    {
      id: 2,
      name: "Protein Powder - Chocolate",
      price: 49.99,
      image: "https://via.placeholder.com/300x200?text=Protein",
      category: "supplements",
      rating: 4.6,
      description: "25g protein per serving, 5lb container"
    },
    {
      id: 3,
      name: "Resistance Band Kit",
      price: 79.99,
      image: "https://via.placeholder.com/300x200?text=Bands",
      category: "accessories",
      rating: 4.7,
      description: "Complete set with door anchor and handles"
    },
    {
      id: 4,
      name: "Yoga Mat Premium",
      price: 89.99,
      image: "https://via.placeholder.com/300x200?text=Yoga+Mat",
      category: "accessories",
      rating: 4.9,
      description: "Extra thick, non-slip surface"
    },
    {
      id: 5,
      name: "Kettlebell Set",
      price: 199.99,
      image: "https://via.placeholder.com/300x200?text=Kettlebells",
      category: "weights",
      rating: 4.5,
      description: "Set of 3 kettlebells (15, 25, 35 lbs)"
    },
    {
      id: 6,
      name: "Pre-Workout Formula",
      price: 39.99,
      image: "https://via.placeholder.com/300x200?text=Pre-Workout",
      category: "supplements",
      rating: 4.4,
      description: "Energy boost for intense workouts"
    }
  ]);

  const [category, setCategory] = useState('all');
  const [cart, setCart] = useState([]);

  const addToCart = (product) => {
    setCart([...cart, product]);
  };

  const filteredProducts = category === 'all' 
    ? products 
    : products.filter(p => p.category === category);

  return (
    <div className="products-page">
      <div className="container">
        <h1>Workout Products</h1>
        
        <div className="products-header">
          <div className="filter-buttons">
            <button 
              className={`filter-btn ${category === 'all' ? 'active' : ''}`}
              onClick={() => setCategory('all')}
            >
              All Products
            </button>
            <button 
              className={`filter-btn ${category === 'weights' ? 'active' : ''}`}
              onClick={() => setCategory('weights')}
            >
              Weights
            </button>
            <button 
              className={`filter-btn ${category === 'supplements' ? 'active' : ''}`}
              onClick={() => setCategory('supplements')}
            >
              Supplements
            </button>
            <button 
              className={`filter-btn ${category === 'accessories' ? 'active' : ''}`}
              onClick={() => setCategory('accessories')}
            >
              Accessories
            </button>
          </div>
        </div>

        <div className="products-grid">
          {filteredProducts.map(product => (
            <div key={product.id} className="product-card">
              <img src={product.image} alt={product.name} />
              <div className="product-info">
                <h3>{product.name}</h3>
                <p>{product.description}</p>
                <div className="product-rating">
                  <Star size={16} fill="gold" />
                  <span>{product.rating}</span>
                </div>
                <div className="product-footer">
                  <span className="price">${product.price}</span>
                  <button 
                    className="add-to-cart-btn"
                    onClick={() => addToCart(product)}
                  >
                    <ShoppingCart size={16} />
                    Add to Cart
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Products;