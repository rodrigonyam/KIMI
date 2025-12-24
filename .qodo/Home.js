// pages/Home.js
import React from 'react';
import { Link } from 'react-router-dom';
import { ArrowRight, Users, Heart, Star } from 'lucide-react';

const Home = () => {
  return (
    <div className="home">
      {/* Hero Section */}
      <section className="hero">
        <div className="hero-content">
          <h1>Transform Your Body, Transform Your Life</h1>
          <p>Join FitLife Gym for premium fitness equipment, expert training, and community support</p>
          <div className="hero-buttons">
            <Link to="/membership" className="btn btn-primary">Join Now</Link>
            <Link to="/products" className="btn btn-secondary">Shop Equipment</Link>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="features">
        <div className="container">
          <h2>Why Choose FitLife?</h2>
          <div className="features-grid">
            <div className="feature-card">
              <Users size={48} />
              <h3>Expert Trainers</h3>
              <p>Certified professionals ready to guide your fitness journey</p>
            </div>
            <div className="feature-card">
              <Star size={48} />
              <h3>Premium Equipment</h3>
              <p>Top-of-the-line workout gear and supplements</p>
            </div>
            <div className="feature-card">
              <Heart size={48} />
              <h3>Community Impact</h3>
              <p>Partnering with local charities to give back</p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="cta">
        <div className="container">
          <h2>Ready to Start Your Journey?</h2>
          <Link to="/membership" className="btn btn-primary">
            Get Your Membership <ArrowRight size={20} />
          </Link>
        </div>
      </section>
    </div>
  );
};

export default Home;