import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useAuth } from '../context/AuthContext';

function MentorList() {
  const [mentors, setMentors] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [filters, setFilters] = useState({
    skill: '',
    sortBy: 'name',
    sortOrder: 'asc'
  });
  const [selectedMentor, setSelectedMentor] = useState(null);
  const [requestMessage, setRequestMessage] = useState('');
  const [submitting, setSubmitting] = useState(false);

  const { user } = useAuth();

  useEffect(() => {
    fetchMentors();
  }, [filters]);

  const fetchMentors = async () => {
    try {
      setLoading(true);
      const params = new URLSearchParams();
      if (filters.skill) params.append('skill', filters.skill);
      if (filters.sortBy) params.append('sortBy', filters.sortBy);
      if (filters.sortOrder) params.append('sortOrder', filters.sortOrder);

      const response = await axios.get(`/api/mentors?${params}`);
      setMentors(response.data);
      setError('');
    } catch (err) {
      setError('Failed to fetch mentors');
      console.error('Error fetching mentors:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleFilterChange = (e) => {
    setFilters({
      ...filters,
      [e.target.name]: e.target.value
    });
  };

  const sendRequest = async (mentorId) => {
    try {
      setSubmitting(true);
      await axios.post('/api/requests', {
        mentorId: mentorId,
        message: requestMessage
      });
      
      setSelectedMentor(null);
      setRequestMessage('');
      alert('Request sent successfully!');
    } catch (err) {
      alert(err.response?.data?.error || 'Failed to send request');
    } finally {
      setSubmitting(false);
    }
  };

  if (user?.role !== 'mentee') {
    return (
      <div className="container">
        <div className="error-message">
          Only mentees can view the mentor list.
        </div>
      </div>
    );
  }

  return (
    <div className="container">
      <h2>Find Mentors</h2>

      {/* Filters */}
      <div className="filters">
        <div className="filters-row">
          <div className="filter-group">
            <label htmlFor="skill">Filter by Skill:</label>
            <input
              type="text"
              id="skill"
              name="skill"
              value={filters.skill}
              onChange={handleFilterChange}
              placeholder="Enter skill name"
            />
          </div>
          
          <div className="filter-group">
            <label htmlFor="sortBy">Sort by:</label>
            <select
              id="sortBy"
              name="sortBy"
              value={filters.sortBy}
              onChange={handleFilterChange}
            >
              <option value="name">Name</option>
              <option value="skill">Skills</option>
            </select>
          </div>
          
          <div className="filter-group">
            <label htmlFor="sortOrder">Order:</label>
            <select
              id="sortOrder"
              name="sortOrder"
              value={filters.sortOrder}
              onChange={handleFilterChange}
            >
              <option value="asc">Ascending</option>
              <option value="desc">Descending</option>
            </select>
          </div>
        </div>
      </div>

      {error && <div className="error-message">{error}</div>}

      {loading ? (
        <div className="loading">Loading mentors...</div>
      ) : mentors.length === 0 ? (
        <div className="empty-state">
          <p>No mentors found matching your criteria.</p>
        </div>
      ) : (
        <div className="mentor-grid">
          {mentors.map((mentor) => (
            <div key={mentor.id} className="mentor-card">
              <img
                src={mentor.imageUrl}
                alt={mentor.name}
                className="profile-image"
              />
              <h3>{mentor.name}</h3>
              <p>{mentor.bio || 'No bio available'}</p>
              <div className="skills">
                {mentor.skills.map((skill, index) => (
                  <span key={index} className="skill-tag">{skill}</span>
                ))}
              </div>
              <button
                onClick={() => setSelectedMentor(mentor)}
                className="btn btn-primary"
                style={{ marginTop: '15px' }}
              >
                Send Request
              </button>
            </div>
          ))}
        </div>
      )}

      {/* Request Modal */}
      {selectedMentor && (
        <div className="modal-overlay">
          <div className="modal-content">
            <div className="modal-header">
              <h3 className="modal-title">Send Request to {selectedMentor.name}</h3>
              <button
                className="close-btn"
                onClick={() => setSelectedMentor(null)}
              >
                ×
              </button>
            </div>
            
            <div className="form-group">
              <label htmlFor="message">Message (optional):</label>
              <textarea
                id="message"
                value={requestMessage}
                onChange={(e) => setRequestMessage(e.target.value)}
                placeholder="Introduce yourself and explain why you'd like this mentor..."
                rows="4"
              />
            </div>
            
            <div style={{ display: 'flex', gap: '10px', justifyContent: 'flex-end' }}>
              <button
                onClick={() => setSelectedMentor(null)}
                className="btn btn-secondary"
              >
                Cancel
              </button>
              <button
                onClick={() => sendRequest(selectedMentor.id)}
                className="btn btn-primary"
                disabled={submitting}
              >
                {submitting ? 'Sending...' : 'Send Request'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default MentorList;
