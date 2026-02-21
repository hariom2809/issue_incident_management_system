from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.database import Base


class IssueComment(Base):
    __tablename__ = "issue_comments"

    id = Column(Integer, primary_key=True, index=True)

    issue_id = Column(Integer, ForeignKey("issues.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    comment = Column(Text, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)

    # relationships
    issue = relationship("Issue", backref="comments")
    user = relationship("User")