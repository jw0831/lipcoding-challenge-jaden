import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useAuth } from '../context/AuthContext';

function Requests() {
  const [requests, setRequests] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const { user } = useAuth();

  useEffect(() => {
    fetchRequests();
  }, []);

  const fetchRequests = async () => {
    try {
      setLoading(true);
      const response = await axios.get('/api/requests');
      setRequests(response.data);
      setError('');
    } catch (err) {
      setError('Failed to fetch requests');
      console.error('Error fetching requests:', err);
    } finally {
      setLoading(false);
    }
  };

  const updateRequestStatus = async (requestId, status) => {
    try {
      await axios.put(`/api/requests/${requestId}`, { status });
      fetchRequests(); // Refresh the list
      alert(`Request ${status} successfully!`);
    } catch (err) {
      alert(err.response?.data?.error || `Failed to ${status} request`);
    }
  };

  const deleteRequest = async (requestId) => {
    if (!window.confirm('Are you sure you want to delete this request?')) {
      return;
    }

    try {
      await axios.delete(`/api/requests/${requestId}`);
      fetchRequests(); // Refresh the list
      alert('Request deleted successfully!');
    } catch (err) {
      alert(err.response?.data?.error || 'Failed to delete request');
    }
  };

  const getStatusBadgeClass = (status) => {
    switch (status) {
      case 'pending': return 'status-badge status-pending';
      case 'accepted': return 'status-badge status-accepted';
      case 'rejected': return 'status-badge status-rejected';
      default: return 'status-badge';
    }
  };

  if (!user) {
    return <div className="loading">Loading...</div>;
  }

  return (
    <div className="container">
      <h2>
        {user.role === 'mentor' ? 'Received Requests' : 'My Requests'}
      </h2>

      {error && <div className="error-message">{error}</div>}

      {loading ? (
        <div className="loading">Loading requests...</div>
      ) : requests.length === 0 ? (
        <div className="empty-state">
          <p>
            {user.role === 'mentor' 
              ? 'No requests received yet.' 
              : 'No requests sent yet.'}
          </p>
        </div>
      ) : (
        <div>
          {requests.map((request) => (
            <div key={request.id} className="card">
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                <div style={{ flex: 1 }}>
                  {user.role === 'mentor' ? (
                    // Mentor view - show mentee info
                    <div style={{ display: 'flex', alignItems: 'center', marginBottom: '15px' }}>
                      <img
                        src={request.mentee.imageUrl}
                        alt={request.mentee.name}
                        className="profile-image"
                        style={{ width: '60px', height: '60px', marginRight: '15px' }}
                      />
                      <div>
                        <h3 style={{ margin: '0 0 5px 0' }}>{request.mentee.name}</h3>
                        <p style={{ margin: 0, color: '#666' }}>{request.mentee.bio || 'No bio available'}</p>
                      </div>
                    </div>
                  ) : (
                    // Mentee view - show mentor info
                    <div style={{ display: 'flex', alignItems: 'center', marginBottom: '15px' }}>
                      <img
                        src={request.mentor.imageUrl}
                        alt={request.mentor.name}
                        className="profile-image"
                        style={{ width: '60px', height: '60px', marginRight: '15px' }}
                      />
                      <div>
                        <h3 style={{ margin: '0 0 5px 0' }}>{request.mentor.name}</h3>
                        <p style={{ margin: '0 0 5px 0', color: '#666' }}>{request.mentor.bio || 'No bio available'}</p>
                        <div className="skills">
                          {request.mentor.skills.map((skill, index) => (
                            <span key={index} className="skill-tag">{skill}</span>
                          ))}
                        </div>
                      </div>
                    </div>
                  )}

                  {request.message && (
                    <div style={{ marginBottom: '15px' }}>
                      <strong>Message:</strong>
                      <p style={{ margin: '5px 0', padding: '10px', backgroundColor: '#f8f9fa', borderRadius: '4px' }}>
                        {request.message}
                      </p>
                    </div>
                  )}

                  <div style={{ display: 'flex', gap: '20px', fontSize: '0.9em', color: '#666' }}>
                    <span>Created: {new Date(request.createdAt).toLocaleDateString()}</span>
                    <span>Updated: {new Date(request.updatedAt).toLocaleDateString()}</span>
                  </div>
                </div>

                <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-end', gap: '10px' }}>
                  <span className={getStatusBadgeClass(request.status)}>
                    {request.status.charAt(0).toUpperCase() + request.status.slice(1)}
                  </span>

                  {user.role === 'mentor' && request.status === 'pending' && (
                    <div style={{ display: 'flex', gap: '10px' }}>
                      <button
                        onClick={() => updateRequestStatus(request.id, 'accepted')}
                        className="btn btn-success"
                      >
                        Accept
                      </button>
                      <button
                        onClick={() => updateRequestStatus(request.id, 'rejected')}
                        className="btn btn-danger"
                      >
                        Reject
                      </button>
                    </div>
                  )}

                  {user.role === 'mentee' && (
                    <button
                      onClick={() => deleteRequest(request.id)}
                      className="btn btn-danger"
                    >
                      Delete
                    </button>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default Requests;
