from flask import Flask, request, jsonify, send_file, redirect
from flask_cors import CORS
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    jwt_required,
    get_jwt_identity,
    get_jwt,
)
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
import os
import uuid
from PIL import Image
import io
import base64
from email_validator import validate_email, EmailNotValidError

app = Flask(__name__)
app.config["SECRET_KEY"] = "your-secret-key-change-in-production"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mentor_mentee.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "jwt-secret-key-change-in-production"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
app.config["UPLOAD_FOLDER"] = "uploads"
app.config["MAX_CONTENT_LENGTH"] = 1 * 1024 * 1024  # 1MB max file size

# Initialize extensions
db = SQLAlchemy(app)
jwt = JWTManager(app)
CORS(app, origins=["http://localhost:3000"], supports_credentials=True)

# Create upload directory
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)


# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(10), nullable=False)  # 'mentor' or 'mentee'
    name = db.Column(db.String(100), nullable=True)
    bio = db.Column(db.Text, nullable=True)
    profile_image = db.Column(db.LargeBinary, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    mentor_skills = db.relationship(
        "MentorSkill", backref="user", lazy=True, cascade="all, delete-orphan"
    )
    sent_requests = db.relationship(
        "MatchingRequest",
        foreign_keys="MatchingRequest.mentee_id",
        backref="mentee",
        lazy=True,
    )
    received_requests = db.relationship(
        "MatchingRequest",
        foreign_keys="MatchingRequest.mentor_id",
        backref="mentor",
        lazy=True,
    )


class MentorSkill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    skill = db.Column(db.String(50), nullable=False)


class MatchingRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mentor_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    mentee_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    message = db.Column(db.Text, nullable=True)
    status = db.Column(
        db.String(20), default="pending"
    )  # 'pending', 'accepted', 'rejected'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)


# Utility functions
def validate_image(file):
    """Validate uploaded image"""
    if not file:
        return False, "No file provided"

    # Check file extension
    allowed_extensions = {"jpg", "jpeg", "png"}
    if (
        "." not in file.filename
        or file.filename.rsplit(".", 1)[1].lower() not in allowed_extensions
    ):
        return False, "Only JPG and PNG files are allowed"

    try:
        # Check image dimensions and size
        image = Image.open(file.stream)
        width, height = image.size

        if width < 500 or height < 500 or width > 1000 or height > 1000:
            return False, "Image must be between 500x500 and 1000x1000 pixels"

        if width != height:
            return False, "Image must be square"

        # Reset stream position
        file.stream.seek(0)
        return True, "Valid image"
    except Exception as e:
        return False, f"Invalid image file: {str(e)}"


def create_jwt_token(user):
    """Create JWT token with all required claims"""
    additional_claims = {
        "iss": "mentor-mentee-app",  # Issuer
        "sub": str(user.id),         # Subject (user ID)
        "aud": "mentor-mentee-users", # Audience
        "jti": str(uuid.uuid4()),    # JWT ID
        "name": user.name or "",     # User name
        "email": user.email,         # User email
        "role": user.role,           # User role
        "nbf": datetime.utcnow(),    # Not before
        "iat": datetime.utcnow(),    # Issued at
    }
    return create_access_token(identity=user.id, additional_claims=additional_claims)


# Routes
@app.route("/")
def index():
    """Redirect to Swagger UI"""
    return redirect("/swagger-ui")


@app.route("/swagger-ui")
def swagger_ui():
    """Serve Swagger UI"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Mentor-Mentee API Documentation</title>
        <link rel="stylesheet" type="text/css" href="https://unpkg.com/swagger-ui-dist@3.25.0/swagger-ui.css" />
    </head>
    <body>
        <div id="swagger-ui"></div>
        <script src="https://unpkg.com/swagger-ui-dist@3.25.0/swagger-ui-bundle.js"></script>
        <script>
            SwaggerUIBundle({
                url: '/openapi.json',
                dom_id: '#swagger-ui',
                presets: [
                    SwaggerUIBundle.presets.apis,
                    SwaggerUIBundle.presets.standalone
                ]
            });
        </script>
    </body>
    </html>
    """


@app.route("/openapi.json")
def openapi_spec():
    """Serve OpenAPI specification"""
    spec = {
        "openapi": "3.0.0",
        "info": {
            "title": "Mentor-Mentee Matching API",
            "version": "1.0.0",
            "description": "API for mentor-mentee matching application",
        },
        "servers": [
            {"url": "http://localhost:8080", "description": "Development server"}
        ],
        "paths": {
            "/api/signup": {
                "post": {
                    "summary": "User registration",
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "email": {"type": "string"},
                                        "password": {"type": "string"},
                                        "name": {"type": "string"},
                                        "role": {
                                            "type": "string",
                                            "enum": ["mentor", "mentee"],
                                        },
                                    },
                                }
                            }
                        }
                    },
                    "responses": {
                        "201": {"description": "User created successfully"},
                        "400": {"description": "Bad request"},
                        "500": {"description": "Internal server error"},
                    },
                }
            },
            "/api/login": {
                "post": {
                    "summary": "User login",
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "email": {"type": "string"},
                                        "password": {"type": "string"},
                                    },
                                }
                            }
                        }
                    },
                    "responses": {
                        "200": {"description": "Login successful"},
                        "401": {"description": "Unauthorized"},
                        "500": {"description": "Internal server error"},
                    },
                }
            },
        },
    }
    return jsonify(spec)


# Authentication routes
@app.route("/api/signup", methods=["POST"])
def signup():
    try:
        data = request.get_json()

        # Validate required fields
        required_fields = ["email", "password", "name", "role"]
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({"error": f"{field} is required"}), 400

        # Validate email format
        try:
            validate_email(data["email"])
        except EmailNotValidError:
            return jsonify({"error": "Invalid email format"}), 400

        # Validate role
        if data["role"] not in ["mentor", "mentee"]:
            return jsonify({"error": "Role must be either mentor or mentee"}), 400

        # Check if user already exists
        if User.query.filter_by(email=data["email"]).first():
            return jsonify({"error": "Email already registered"}), 400

        # Create new user
        user = User(
            email=data["email"],
            password_hash=generate_password_hash(data["password"]),
            name=data["name"],
            role=data["role"],
        )

        db.session.add(user)
        db.session.commit()

        return jsonify({"message": "User created successfully"}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Internal server error"}), 500


@app.route("/api/login", methods=["POST"])
def login():
    try:
        data = request.get_json()
        print(f"Login attempt with data: {data}")

        if not data or "email" not in data or "password" not in data:
            return jsonify({"error": "Email and password are required"}), 400

        user = User.query.filter_by(email=data["email"]).first()
        print(f"User found: {user.email if user else 'None'}")

        if user and check_password_hash(user.password_hash, data["password"]):
            token = create_jwt_token(user)
            print(f"Login successful for {user.email}, token created")
            return jsonify({"token": token}), 200
        else:
            print("Invalid credentials")
            return jsonify({"error": "Invalid credentials"}), 401

    except Exception as e:
        print(f"Login error: {e}")
        return jsonify({"error": "Internal server error"}), 500


@app.route("/api/me", methods=["GET"])
@jwt_required()
def get_me():
    try:
        user_id = get_jwt_identity()
        print(f"GET /api/me - User ID from token: {user_id}")
        
        user = User.query.get(user_id)
        print(f"User found: {user.email if user else 'None'}")

        if not user:
            return jsonify({"error": "User not found"}), 404

        profile_data = {
            "id": user.id,
            "email": user.email,
            "role": user.role,
            "profile": {
                "name": user.name,
                "bio": user.bio,
                "imageUrl": f"/api/images/{user.role}/{user.id}",
            },
        }

        # Add skills for mentors
        if user.role == "mentor":
            skills = [skill.skill for skill in user.mentor_skills]
            profile_data["profile"]["skills"] = skills

        print(f"Returning profile data: {profile_data}")
        return jsonify(profile_data), 200

    except Exception as e:
        print(f"Error in get_me: {e}")
        return jsonify({"error": "Internal server error"}), 500


@app.route("/api/me", methods=["PUT"])
@jwt_required()
def update_profile():
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if not user:
            return jsonify({"error": "User not found"}), 404

        data = request.get_json()

        # Update basic profile fields
        if "name" in data:
            user.name = data["name"]
        if "bio" in data:
            user.bio = data["bio"]

        # Update skills for mentors
        if user.role == "mentor" and "skills" in data:
            # Remove existing skills
            MentorSkill.query.filter_by(user_id=user.id).delete()

            # Add new skills
            for skill in data["skills"]:
                new_skill = MentorSkill(user_id=user.id, skill=skill)
                db.session.add(new_skill)

        db.session.commit()
        return jsonify({"message": "Profile updated successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Internal server error"}), 500


@app.route("/api/images/<role>/<int:user_id>", methods=["GET"])
def get_profile_image(role, user_id):
    try:
        user = User.query.get(user_id)

        if not user or user.role != role:
            # Return default image
            default_url = f"https://placehold.co/500x500.jpg?text={role.upper()}"
            return redirect(default_url)

        if user.profile_image:
            return send_file(
                io.BytesIO(user.profile_image),
                mimetype="image/jpeg",
                as_attachment=False,
            )
        else:
            # Return default image
            default_url = f"https://placehold.co/500x500.jpg?text={role.upper()}"
            return redirect(default_url)

    except Exception as e:
        default_url = f"https://placehold.co/500x500.jpg?text={role.upper()}"
        return redirect(default_url)


@app.route("/api/images/<role>/<int:user_id>", methods=["PUT"])
@jwt_required()
def update_profile_image(role, user_id):
    try:
        current_user_id = get_jwt_identity()

        # Check if user is updating their own image
        if current_user_id != user_id:
            return jsonify({"error": "Unauthorized"}), 403

        user = User.query.get(user_id)
        if not user or user.role != role:
            return jsonify({"error": "User not found"}), 404

        if "image" not in request.files:
            return jsonify({"error": "No image file provided"}), 400

        file = request.files["image"]

        # Validate image
        is_valid, message = validate_image(file)
        if not is_valid:
            return jsonify({"error": message}), 400

        # Process and save image
        image_data = file.read()
        user.profile_image = image_data

        db.session.commit()
        return jsonify({"message": "Profile image updated successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Internal server error"}), 500


# Mentor listing routes
@app.route("/api/mentors", methods=["GET"])
@jwt_required()
def get_mentors():
    try:
        # Get query parameters
        skill_filter = request.args.get("skill")
        sort_by = request.args.get("sortBy", "name")  # 'name' or 'skill'
        sort_order = request.args.get("sortOrder", "asc")  # 'asc' or 'desc'

        # Base query for mentors
        query = User.query.filter_by(role="mentor")

        # Apply skill filter
        if skill_filter:
            query = query.join(MentorSkill).filter(
                MentorSkill.skill.ilike(f"%{skill_filter}%")
            )

        # Apply sorting
        if sort_by == "name":
            if sort_order == "desc":
                query = query.order_by(User.name.desc())
            else:
                query = query.order_by(User.name.asc())

        mentors = query.all()

        mentor_list = []
        for mentor in mentors:
            skills = [skill.skill for skill in mentor.mentor_skills]
            mentor_data = {
                "id": mentor.id,
                "email": mentor.email,
                "role": mentor.role,
                "profile": {
                    "name": mentor.name,
                    "bio": mentor.bio,
                    "imageUrl": f"/api/images/mentor/{mentor.id}",
                    "skills": skills,
                }
            }
            mentor_list.append(mentor_data)

        # Sort by skills if requested
        if sort_by == "skill":
            mentor_list.sort(
                key=lambda x: ", ".join(x["skills"]), reverse=(sort_order == "desc")
            )

        return jsonify(mentor_list), 200

    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500


# Matching request routes
@app.route("/api/requests", methods=["POST"])
@jwt_required()
def create_request():
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if user.role != "mentee":
            return jsonify({"error": "Only mentees can send requests"}), 403

        data = request.get_json()

        if "mentorId" not in data:
            return jsonify({"error": "mentorId is required"}), 400

        mentor_id = data["mentorId"]
        mentor = User.query.get(mentor_id)

        if not mentor or mentor.role != "mentor":
            return jsonify({"error": "Mentor not found"}), 404

        # Check if mentee already has a pending request
        existing_request = MatchingRequest.query.filter_by(
            mentee_id=user_id, status="pending"
        ).first()

        if existing_request:
            return jsonify({"error": "You already have a pending request"}), 400

        # Check if request to this mentor already exists
        existing_to_mentor = MatchingRequest.query.filter_by(
            mentor_id=mentor_id, mentee_id=user_id
        ).first()

        if existing_to_mentor:
            return jsonify({"error": "Request to this mentor already exists"}), 400

        # Create new request
        new_request = MatchingRequest(
            mentor_id=mentor_id, mentee_id=user_id, message=data.get("message", "")
        )

        db.session.add(new_request)
        db.session.commit()

        return jsonify({"message": "Request sent successfully"}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Internal server error"}), 500


@app.route("/api/requests", methods=["GET"])
@jwt_required()
def get_requests():
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if user.role == "mentee":
            # Get requests sent by mentee
            requests = MatchingRequest.query.filter_by(mentee_id=user_id).all()
            request_list = []

            for req in requests:
                mentor = User.query.get(req.mentor_id)
                skills = [skill.skill for skill in mentor.mentor_skills]

                request_data = {
                    "id": req.id,
                    "mentor": {
                        "id": mentor.id,
                        "name": mentor.name,
                        "bio": mentor.bio,
                        "imageUrl": f"/api/images/mentor/{mentor.id}",
                        "skills": skills,
                    },
                    "message": req.message,
                    "status": req.status,
                    "createdAt": req.created_at.isoformat(),
                    "updatedAt": req.updated_at.isoformat(),
                }
                request_list.append(request_data)

        elif user.role == "mentor":
            # Get requests received by mentor
            requests = MatchingRequest.query.filter_by(mentor_id=user_id).all()
            request_list = []

            for req in requests:
                mentee = User.query.get(req.mentee_id)

                request_data = {
                    "id": req.id,
                    "mentee": {
                        "id": mentee.id,
                        "name": mentee.name,
                        "bio": mentee.bio,
                        "imageUrl": f"/api/images/mentee/{mentee.id}",
                    },
                    "message": req.message,
                    "status": req.status,
                    "createdAt": req.created_at.isoformat(),
                    "updatedAt": req.updated_at.isoformat(),
                }
                request_list.append(request_data)

        return jsonify(request_list), 200

    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500


@app.route("/api/requests/<int:request_id>", methods=["PUT"])
@jwt_required()
def update_request(request_id):
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        matching_request = MatchingRequest.query.get(request_id)
        if not matching_request:
            return jsonify({"error": "Request not found"}), 404

        data = request.get_json()

        if user.role == "mentor" and matching_request.mentor_id == user_id:
            # Mentor accepting/rejecting request
            if "status" not in data or data["status"] not in ["accepted", "rejected"]:
                return jsonify({"error": "Valid status is required"}), 400

            # If accepting, check if mentor already has an accepted request
            if data["status"] == "accepted":
                existing_accepted = MatchingRequest.query.filter_by(
                    mentor_id=user_id, status="accepted"
                ).first()

                if existing_accepted:
                    return (
                        jsonify(
                            {
                                "error": "You already have an accepted mentoring relationship"
                            }
                        ),
                        400,
                    )

            matching_request.status = data["status"]
            matching_request.updated_at = datetime.utcnow()

        else:
            return jsonify({"error": "Unauthorized"}), 403

        db.session.commit()
        return jsonify({"message": "Request updated successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Internal server error"}), 500


@app.route("/api/requests/<int:request_id>", methods=["DELETE"])
@jwt_required()
def delete_request(request_id):
    try:
        user_id = get_jwt_identity()

        matching_request = MatchingRequest.query.get(request_id)
        if not matching_request:
            return jsonify({"error": "Request not found"}), 404

        # Only mentee can delete their own request
        if matching_request.mentee_id != user_id:
            return jsonify({"error": "Unauthorized"}), 403

        db.session.delete(matching_request)
        db.session.commit()

        return jsonify({"message": "Request deleted successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Internal server error"}), 500


# API Spec compliant matching request routes
@app.route("/api/match-requests", methods=["POST"])
@jwt_required()
def create_match_request():
    """Create matching request according to API spec"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if user.role != "mentee":
            return jsonify({"error": "Only mentees can send requests"}), 403

        data = request.get_json()

        if "mentorId" not in data:
            return jsonify({"error": "mentorId is required"}), 400

        mentor_id = data["mentorId"]
        mentor = User.query.get(mentor_id)

        if not mentor or mentor.role != "mentor":
            return jsonify({"error": "Mentor not found"}), 400

        # Check if mentee already has a pending request
        existing_request = MatchingRequest.query.filter_by(
            mentee_id=user_id, status="pending"
        ).first()

        if existing_request:
            return jsonify({"error": "You already have a pending request"}), 400

        # Check if request to this mentor already exists
        existing_to_mentor = MatchingRequest.query.filter_by(
            mentor_id=mentor_id, mentee_id=user_id
        ).first()

        if existing_to_mentor:
            return jsonify({"error": "Request to this mentor already exists"}), 400

        # Create new request
        new_request = MatchingRequest(
            mentor_id=mentor_id, 
            mentee_id=user_id, 
            message=data.get("message", "")
        )

        db.session.add(new_request)
        db.session.commit()

        # Return response according to API spec
        response_data = {
            "id": new_request.id,
            "mentorId": new_request.mentor_id,
            "menteeId": new_request.mentee_id,
            "message": new_request.message,
            "status": new_request.status
        }

        return jsonify(response_data), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Internal server error"}), 500


@app.route("/api/match-requests/incoming", methods=["GET"])
@jwt_required()
def get_incoming_requests():
    """Get incoming requests for mentors"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if user.role != "mentor":
            return jsonify({"error": "Only mentors can view incoming requests"}), 403
        
        requests = MatchingRequest.query.filter_by(mentor_id=user_id).all()
        request_list = []
        
        for req in requests:
            request_data = {
                "id": req.id,
                "mentorId": req.mentor_id,
                "menteeId": req.mentee_id,
                "message": req.message,
                "status": req.status
            }
            request_list.append(request_data)
        
        return jsonify(request_list), 200
        
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500


@app.route("/api/match-requests/outgoing", methods=["GET"])
@jwt_required()
def get_outgoing_requests():
    """Get outgoing requests for mentees"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if user.role != "mentee":
            return jsonify({"error": "Only mentees can view outgoing requests"}), 403
        
        requests = MatchingRequest.query.filter_by(mentee_id=user_id).all()
        request_list = []
        
        for req in requests:
            request_data = {
                "id": req.id,
                "mentorId": req.mentor_id,
                "menteeId": req.mentee_id,
                "status": req.status
            }
            request_list.append(request_data)
        
        return jsonify(request_list), 200
        
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500


@app.route("/api/match-requests/<int:request_id>/accept", methods=["PUT"])
@jwt_required()
def accept_request(request_id):
    """Accept a matching request"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if user.role != "mentor":
            return jsonify({"error": "Only mentors can accept requests"}), 403
        
        matching_request = MatchingRequest.query.get(request_id)
        if not matching_request:
            return jsonify({"error": "Request not found"}), 404
        
        if matching_request.mentor_id != int(user_id):  # Convert user_id to int
            return jsonify({"error": "Unauthorized"}), 403
        
        # Check if mentor already has an accepted request
        existing_accepted = MatchingRequest.query.filter_by(
            mentor_id=user_id, status="accepted"
        ).first()
        
        if existing_accepted:
            return jsonify({"error": "You already have an accepted mentoring relationship"}), 400
        
        matching_request.status = "accepted"
        matching_request.updated_at = datetime.utcnow()
        db.session.commit()
        
        response_data = {
            "id": matching_request.id,
            "mentorId": matching_request.mentor_id,
            "menteeId": matching_request.mentee_id,
            "message": matching_request.message,
            "status": matching_request.status
        }
        
        return jsonify(response_data), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Internal server error"}), 500


@app.route("/api/match-requests/<int:request_id>/reject", methods=["PUT"])
@jwt_required()
def reject_request(request_id):
    """Reject a matching request"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if user.role != "mentor":
            return jsonify({"error": "Only mentors can reject requests"}), 403
        
        matching_request = MatchingRequest.query.get(request_id)
        if not matching_request:
            return jsonify({"error": "Request not found"}), 404
        
        if matching_request.mentor_id != user_id:
            return jsonify({"error": "Unauthorized"}), 403
        
        matching_request.status = "rejected"
        matching_request.updated_at = datetime.utcnow()
        db.session.commit()
        
        response_data = {
            "id": matching_request.id,
            "mentorId": matching_request.mentor_id,
            "menteeId": matching_request.mentee_id,
            "message": matching_request.message,
            "status": matching_request.status
        }
        
        return jsonify(response_data), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Internal server error"}), 500


@app.route("/api/match-requests/<int:request_id>", methods=["DELETE"])
@jwt_required()
def cancel_request(request_id):
    """Cancel/delete a matching request"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if user.role != "mentee":
            return jsonify({"error": "Only mentees can cancel requests"}), 403
        
        matching_request = MatchingRequest.query.get(request_id)
        if not matching_request:
            return jsonify({"error": "Request not found"}), 404
        
        if matching_request.mentee_id != user_id:
            return jsonify({"error": "Unauthorized"}), 403
        
        # According to API spec, mark as cancelled instead of deleting
        matching_request.status = "cancelled"
        matching_request.updated_at = datetime.utcnow()
        db.session.commit()
        
        response_data = {
            "id": matching_request.id,
            "mentorId": matching_request.mentor_id,
            "menteeId": matching_request.mentee_id,
            "message": matching_request.message,
            "status": matching_request.status
        }
        
        return jsonify(response_data), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Internal server error"}), 500


# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({"error": "Internal server error"}), 500


@app.route("/api/profile", methods=["GET", "PUT"])
@jwt_required()
def profile_spec():
    """Get or update profile according to API spec"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if not user:
            return jsonify({"error": "User not found"}), 404

        if request.method == "GET":
            # Return user profile data
            profile_data = {
                "id": user.id,
                "email": user.email,
                "name": user.name,
                "role": user.role,
                "bio": user.bio
            }
            
            if user.role == "mentor":
                # Get skills from relationship
                skills = [skill.skill for skill in user.mentor_skills]
                profile_data["skills"] = skills
                # Note: availability is not in the current model
            # Note: interests is not in the current model for mentees
            
            if user.profile_image:
                profile_data["imageUrl"] = f"/api/profile/image/{user.id}"
                
            return jsonify(profile_data), 200

        # Handle PUT request
        data = request.get_json()

        # Update basic profile fields
        if "name" in data:
            user.name = data["name"]
        if "bio" in data:
            user.bio = data["bio"]
        
        # Handle base64 image upload
        if "image" in data and data["image"]:
            try:
                # Decode base64 image
                import base64
                image_data = base64.b64decode(data["image"])
                
                # Validate image
                image = Image.open(io.BytesIO(image_data))
                width, height = image.size
                
                if width < 500 or height < 500 or width > 1000 or height > 1000:
                    return jsonify({"error": "Image must be between 500x500 and 1000x1000 pixels"}), 400
                
                if width != height:
                    return jsonify({"error": "Image must be square"}), 400
                
                if len(image_data) > 1024 * 1024:  # 1MB
                    return jsonify({"error": "Image size must be less than 1MB"}), 400
                
                user.profile_image = image_data
                
            except Exception as img_error:
                return jsonify({"error": f"Invalid image data: {str(img_error)}"}), 400

        # Update skills for mentors
        if user.role == "mentor" and "skills" in data:
            # Remove existing skills
            MentorSkill.query.filter_by(user_id=user.id).delete()
            
            # Add new skills
            if data["skills"]:
                for skill in data["skills"]:
                    new_skill = MentorSkill(user_id=user.id, skill=skill)
                    db.session.add(new_skill)

        db.session.commit()
        
        # Return updated profile data according to spec
        profile_data = {
            "id": user.id,
            "email": user.email,
            "role": user.role,
            "profile": {
                "name": user.name,
                "bio": user.bio,
                "imageUrl": f"/api/images/{user.role}/{user.id}",
            },
        }
        
        if user.role == "mentor":
            skills = [skill.skill for skill in user.mentor_skills]
            profile_data["profile"]["skills"] = skills
        
        return jsonify(profile_data), 200

    except Exception as e:
        db.session.rollback()
        print(f"Error in update_profile_spec: {e}")
        return jsonify({"error": "Internal server error"}), 500


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(host="0.0.0.0", port=8080, debug=True)
