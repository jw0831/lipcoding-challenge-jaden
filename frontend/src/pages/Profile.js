import React, { useState, useRef } from 'react';
import { useAuth } from '../context/AuthContext';

function Profile() {
  const { user, updateProfile, updateProfileImage } = useAuth();
  const [editing, setEditing] = useState(false);
  const [formData, setFormData] = useState({
    name: user?.profile?.name || '',
    bio: user?.profile?.bio || '',
    skills: user?.profile?.skills || []
  });
  const [newSkill, setNewSkill] = useState('');
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const fileInputRef = useRef(null);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const addSkill = () => {
    if (newSkill.trim() && !formData.skills.includes(newSkill.trim())) {
      setFormData({
        ...formData,
        skills: [...formData.skills, newSkill.trim()]
      });
      setNewSkill('');
    }
  };

  const removeSkill = (skillToRemove) => {
    setFormData({
      ...formData,
      skills: formData.skills.filter(skill => skill !== skillToRemove)
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage('');
    setLoading(true);

    const result = await updateProfile(formData);
    
    if (result.success) {
      setMessage('Profile updated successfully!');
      setEditing(false);
    } else {
      setMessage(result.error);
    }
    
    setLoading(false);
  };

  const handleImageChange = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setMessage('');
    setLoading(true);

    const result = await updateProfileImage(file);
    
    if (result.success) {
      setMessage('Profile image updated successfully!');
    } else {
      setMessage(result.error);
    }
    
    setLoading(false);
  };

  if (!user) {
    return <div className="loading">Loading...</div>;
  }

  return (
    <div className="container">
      <div className="card">
        <div className="card-header">
          <h2 className="card-title">My Profile</h2>
          {!editing && (
            <button 
              onClick={() => setEditing(true)} 
              className="btn btn-primary"
            >
              Edit Profile
            </button>
          )}
        </div>

        {message && (
          <div className={message.includes('successfully') ? 'success-message' : 'error-message'}>
            {message}
          </div>
        )}

        {editing ? (
          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label htmlFor="name">Name:</label>
              <input
                type="text"
                id="name"
                name="name"
                value={formData.name}
                onChange={handleChange}
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="bio">Bio:</label>
              <textarea
                id="bio"
                name="bio"
                value={formData.bio}
                onChange={handleChange}
                rows="4"
              />
            </div>

            {user.role === 'mentor' && (
              <div className="form-group">
                <label>Skills:</label>
                <div style={{ display: 'flex', gap: '10px', marginBottom: '10px' }}>
                  <input
                    type="text"
                    value={newSkill}
                    onChange={(e) => setNewSkill(e.target.value)}
                    placeholder="Add a skill"
                    onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), addSkill())}
                  />
                  <button type="button" onClick={addSkill} className="btn btn-secondary">
                    Add
                  </button>
                </div>
                <div className="skills">
                  {formData.skills.map((skill, index) => (
                    <span key={index} className="skill-tag">
                      {skill}
                      <button
                        type="button"
                        onClick={() => removeSkill(skill)}
                        style={{ 
                          marginLeft: '5px', 
                          background: 'none', 
                          border: 'none', 
                          cursor: 'pointer' 
                        }}
                      >
                        ×
                      </button>
                    </span>
                  ))}
                </div>
              </div>
            )}

            <div style={{ display: 'flex', gap: '10px' }}>
              <button type="submit" className="btn btn-success" disabled={loading}>
                {loading ? 'Saving...' : 'Save Changes'}
              </button>
              <button 
                type="button" 
                onClick={() => setEditing(false)} 
                className="btn btn-secondary"
              >
                Cancel
              </button>
            </div>
          </form>
        ) : (
          <div>
            <div style={{ display: 'flex', alignItems: 'center', marginBottom: '20px' }}>
              <img
                src={user.profile.imageUrl}
                alt="Profile"
                className="profile-image"
                style={{ marginRight: '20px' }}
              />
              <div>
                <input
                  type="file"
                  ref={fileInputRef}
                  onChange={handleImageChange}
                  accept=".jpg,.jpeg,.png"
                  style={{ display: 'none' }}
                />
                <button
                  onClick={() => fileInputRef.current?.click()}
                  className="btn btn-secondary"
                  disabled={loading}
                >
                  {loading ? 'Uploading...' : 'Change Photo'}
                </button>
              </div>
            </div>

            <div className="form-group">
              <strong>Name:</strong> {user.profile.name || 'Not set'}
            </div>

            <div className="form-group">
              <strong>Email:</strong> {user.email}
            </div>

            <div className="form-group">
              <strong>Role:</strong> {user.role}
            </div>

            <div className="form-group">
              <strong>Bio:</strong> {user.profile.bio || 'No bio added'}
            </div>

            {user.role === 'mentor' && (
              <div className="form-group">
                <strong>Skills:</strong>
                <div className="skills">
                  {user.profile.skills?.length > 0 ? (
                    user.profile.skills.map((skill, index) => (
                      <span key={index} className="skill-tag">{skill}</span>
                    ))
                  ) : (
                    <span>No skills added</span>
                  )}
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default Profile;
