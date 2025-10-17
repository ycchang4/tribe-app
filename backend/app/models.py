from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table, Text, Float, Boolean, JSON
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()

# Association table for matches (many-to-many)
matches_table = Table(
    'matches',
    Base.metadata,
    Column('user1_id', Integer, ForeignKey('users.id', ondelete='CASCADE'), primary_key=True),
    Column('user2_id', Integer, ForeignKey('users.id', ondelete='CASCADE'), primary_key=True),
    Column('matched_at', DateTime, default=datetime.utcnow),
    Column('compatibility_score', Float)
)

# Association table for swipes
swipes_table = Table(
    'swipes',
    Base.metadata,
    Column('swiper_id', Integer, ForeignKey('users.id', ondelete='CASCADE'), primary_key=True),
    Column('swiped_id', Integer, ForeignKey('users.id', ondelete='CASCADE'), primary_key=True),
    Column('liked', Boolean),  # True for like, False for pass
    Column('swiped_at', DateTime, default=datetime.utcnow)
)


class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    name = Column(String, nullable=False)
    age = Column(Integer)
    gender = Column(String)
    location = Column(String)
    bio = Column(Text)
    life_story = Column(Text)  # Text we analyze for color personality
    
    # Color personality (AI-generated)
    primary_color = Column(String)  # e.g., "Ruby Red"
    color_scores = Column(JSON)  # {"Ruby Red": 0.8, "Ocean Blue": 0.3, ...}
    personality_vector = Column(JSON)  # ML embedding for similarity matching
    
    # Profile
    profile_photo_url = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    # Users I've matched with
    matches = relationship(
        'User',
        secondary=matches_table,
        primaryjoin=id == matches_table.c.user1_id,
        secondaryjoin=id == matches_table.c.user2_id,
        backref='matched_by'
    )
    
    # Messages I've sent
    sent_messages = relationship('Message', foreign_keys='Message.sender_id', back_populates='sender')
    # Messages I've received
    received_messages = relationship('Message', foreign_keys='Message.receiver_id', back_populates='receiver')


class Message(Base):
    __tablename__ = 'messages'
    
    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    receiver_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    read = Column(Boolean, default=False)
    
    # Relationships
    sender = relationship('User', foreign_keys=[sender_id], back_populates='sent_messages')
    receiver = relationship('User', foreign_keys=[receiver_id], back_populates='received_messages')