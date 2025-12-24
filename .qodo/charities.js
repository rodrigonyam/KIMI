// pages/Charities.js
import React from 'react';
import { Heart, Users, Calendar, DollarSign } from 'lucide-react';

const Charities = () => {
  const charityPartners = [
    {
      id: 1,
      name: "Youth Fitness Foundation",
      description: "Providing free fitness programs for underprivileged youth",
      impact: "500+ kids served",
      donation: "$5,000 donated this year",
      image: "https://via.placeholder.com/300x200?text=Youth+Fitness"
    },
    {
      id: 2,
      name: "Senior Wellness Initiative",
      description: "Helping seniors stay active and healthy through specialized programs",
      impact: "200+ seniors helped",
      donation: "$3,000 donated this year",
      image: "https://via.placeholder.com/300x200?text=Senior+Wellness"
    },
    {
      id: 3,
      name: "Community Health Drive",
      description: "Free health screenings and fitness assessments for the community",
      impact: "1,000+ people screened",
      donation: "$2,000 donated this year",
      image: "https://via.placeholder.com/300x200?text=Health+Drive"
    }
  ];

  const upcomingEvents = [
    {
      id: 1,
      title: "Charity Workout Marathon",
      date: "December 28, 2025",
      description: "24-hour workout event raising funds for local charities",
      goal: "$10,000 goal"
    },
    {
      id: 2,
      title: "Community Food Drive",
      date: "January 15, 2026",
      description: "Collecting healthy food for local food banks",
      goal: "500 meals"
    }
  ];

  return (
    <div className="charities-page">
      <div className="container">
        <h1>Community Partnerships</h1>
        <p className="charities-intro">
          At FitLife Gym, we believe in giving back to our community. 
          Partner with us in making a difference through fitness and wellness.
        </p>

        <section className="charity-partners">
          <h2>Our Charity Partners</h2>
          <div className="charity-grid">
            {charityPartners.map(charity => (
              <div key={charity.id} className="charity-card">
                <img src={charity.image} alt={charity.name} />
                <div className="charity-content">
                  <h3>{charity.name}</h3>
                  <p>{charity.description}</p>
                  <div className="charity-stats">
                    <div className="stat">
                      <Users size={16} />
                      <span>{charity.impact}</span>
                    </div>
                    <div className="stat">
                      <DollarSign size={16} />
                      <span>{charity.donation}</span>
                    </div>
                  </div>
                  <button className="btn btn-primary">Learn More</button>
                </div>
              </div>
            ))}
          </div>
        </section>

        <section className="upcoming-events">
          <h2>Upcoming Charity Events</h2>
          <div className="events-list">
            {upcomingEvents.map(event => (
              <div key={event.id} className="event-card">
                <div className="event-date">
                  <Calendar size={20} />
                  <span>{event.date}</span>
                </div>
                <h3>{event.title}</h3>
                <p>{event.description}</p>
                <div className="event-goal">
                  <strong>Goal: {event.goal}</strong>
                </div>
                <button className="btn btn-secondary">Register/Donate</button>
              </div>
            ))}
          </div>
        </section>

        <section className="get-involved">
          <h2>Get Involved</h2>
          <div className="involvement-options">
            <div className="option-card">
              <Heart size={32} />
              <h3>Donate</h3>
              <p>Support our charity partners with a direct donation</p>
              <button className="btn btn-primary">Donate Now</button>
            </div>
            <div className="option-card">
              <Users size={32} />
              <h3>Volunteer</h3>
              <p>Join our team of volunteers at community events</p>
              <button className="btn btn-secondary">Sign Up</button>
            </div>
            <div className="option-card">
              <Calendar size={32} />
              <h3>Participate</h3>
              <p>Join our charity fitness events and fundraisers</p>
              <button className="btn btn-secondary">View Events</button>
            </div>
          </div>
        </section>
      </div>
    </div>
  );
};

export default Charities;