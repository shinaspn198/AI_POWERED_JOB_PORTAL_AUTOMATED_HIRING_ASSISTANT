from api.database import Base, engine
from api.models.user import User
from api.models.candidate_assessment import CandidateAssessment


print("Creating database tables...")

Base.metadata.create_all(bind=engine)

print("Database tables created successfully!")