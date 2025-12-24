// pages/Membership.js
import React, { useState } from 'react';
import { Check, X } from 'lucide-react';

const Membership = () => {
  const [selectedPlan, setSelectedPlan] = useState(null);

  const plans = [
    {
      id: 'basic',
      name: 'Basic',
      price: 29.99,
      period: 'month',
      features: [
        { name: 'Gym Access', included: true },
        { name: 'Locker Room', included: true },
        { name: 'Group Classes', included: false },
        { name: 'Personal Training', included: false },
        { name: 'Nutrition Plan', included: false }
      ]
    },
    {
      id: 'premium',
      name: 'Premium',
      price: 49.99,
      period: 'month',
      popular: true,
      features: [
        { name: 'Gym Access', included: true },
        { name: 'Locker Room', included: true },
        { name: 'Group Classes', included: true },
        { name: 'Personal Training', included: true },
        { name: 'Nutrition Plan', included: false }
      ]
    },
    {
      id: 'elite',
      name: 'Elite',
      price: 79.99,
      period: 'month',
      features: [
        { name: 'Gym Access', included: true },
        { name: 'Locker Room', included: true },
        { name: 'Group Classes', included: true },
        { name: 'Personal Training', included: true },
        { name: 'Nutrition Plan', included: true }
      ]
    }
  ];

  return (
    <div className="membership-page">
      <div className="container">
        <h1>Choose Your Membership</h1>
        <p className="membership-subtitle">Select the perfect plan for your fitness journey</p>

        <div className="membership-grid">
          {plans.map(plan => (
            <div key={plan.id} className={`membership-card ${plan.popular ? 'popular' : ''}`}>
              {plan.popular && <div className="popular-badge">Most Popular</div>}
              <h3>{plan.name}</h3>
              <div className="price">
                <span className="amount">${plan.price}</span>
                <span className="period">/{plan.period}</span>
              </div>
              
              <ul className="features-list">
                {plan.features.map((feature, index) => (
                  <li key={index} className={feature.included ? 'included' : 'excluded'}>
                    {feature.included ? <Check size={16} /> : <X size={16} />}
                    {feature.name}
                  </li>
                ))}
              </ul>

              <button 
                className={`select-plan-btn ${plan.popular ? 'btn-primary' : 'btn-secondary'}`}
                onClick={() => setSelectedPlan(plan.id)}
              >
                Select Plan
              </button>
            </div>
          ))}
        </div>

        <div className="membership-benefits">
          <h2>All Memberships Include</h2>
          <div className="benefits-grid">
            <div className="benefit-item">
              <h4>24/7 Access</h4>
              <p>Work out on your schedule</p>
            </div>
            <div className="benefit-item">
              <h4>Free Parking</h4>
              <p>Convenient parking available</p>
            </div>
            <div className="benefit-item">
              <h4>WiFi & Showers</h4>
              <p>Stay connected and fresh</p>
            </div>
            <div className="benefit-item">
              <h4>Member Discounts</h4>
              <p>Save on products and services</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Membership;