import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

function Navbar() {
  const { user, logout } = useAuth();

  return (
    <nav className="navbar">
      <div className="navbar-content">
        <Link to="/" className="navbar-brand">
          Mentor-Mentee App
        </Link>
        
        {user && (
          <ul className="navbar-nav">
            <li>
              <Link to="/profile">Profile</Link>
            </li>
            {user.role === 'mentee' && (
              <li>
                <Link to="/mentors">Find Mentors</Link>
              </li>
            )}
            <li>
              <Link to="/requests">
                {user.role === 'mentor' ? 'Received Requests' : 'My Requests'}
              </Link>
            </li>
            <li>
              <button onClick={logout} className="btn btn-secondary">
                Logout
              </button>
            </li>
          </ul>
        )}
      </div>
    </nav>
  );
}

export default Navbar;
