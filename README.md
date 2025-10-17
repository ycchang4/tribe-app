# tribe-app
# 🎨 ColorMatch - Find Your Tribe

A dating app that matches people based on personality colors. Users share their life story, get assigned a TRIBE color via AI, and connect with compatible matches.

> **Status:** In active development

## 🌈 The TRIBE Color System

### Primary Colors
- 🔴 **Ruby Red** - The Passionate Driver (achievement, leadership)
- 🔵 **Ocean Blue** - The Deep Connector (empathy, relationships)
- 🟡 **Sunlight Yellow** - The Joyful Explorer (adventure, optimism)
- 🟢 **Forest Green** - The Steady Builder (growth, stability)

### Secondary Colors
- 🟠 **Amber Gold** - The Warm Mentor (guidance, wisdom)
- 🟣 **Lavender Purple** - The Creative Dreamer (creativity, intuition)
- 🩷 **Coral Pink** - The Playful Optimist (joy, connection)
- 🤎 **Earth Brown** - The Grounded Realist (authenticity, loyalty)

## 🛠️ Tech Stack

**Backend:** FastAPI, PostgreSQL, SQLAlchemy, WebSocket  
**Frontend (Planned):** React, TypeScript, Tailwind CSS  
**AI/ML (Planned):** HuggingFace, sentence-transformers  
**Auth:** JWT (python-jose), passlib

## 🚀 Quick Start

```bash
# Clone and setup
git clone https://github.com/yourusername/colormatch.git
cd colormatch

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start PostgreSQL
brew services start postgresql  # Mac with Homebrew

# Run server
uvicorn main:app --reload
```

## 🔄 Daily Workflow

**Start working:**
```bash
source venv/bin/activate
uvicorn main:app --reload
```

**Stop working:**
- Press `Ctrl+C` to stop FastAPI
- `brew services stop postgresql` to stop database
- `deactivate` to exit venv (optional)

## 🗺️ Roadmap

- [ ] Database schema & migrations
- [ ] User authentication
- [ ] Color assignment AI
- [ ] Matching algorithm
- [ ] Frontend UI
- [ ] Real-time chat
- [ ] Photo uploads
- [ ] Production deployment

---

Made with ❤️ and 🎨
