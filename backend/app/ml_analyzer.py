from sentence_transformers import SentenceTransformer
import numpy as np
from typing import Dict, List, Tuple
import re

# Load the ML model (lightweight version)
model = SentenceTransformer('all-MiniLM-L6-v2')

# Color personality definitions with keywords
COLOR_PROFILES = {
    'Ruby Red': {
        'keywords': ['ambitious', 'driven', 'compete', 'lead', 'challenge', 'goals', 'win', 'achieve', 'success', 'power', 'determined', 'assertive', 'confident'],
        'description': 'The Passionate Driver'
    },
    'Ocean Blue': {
        'keywords': ['people', 'understand', 'help', 'connect', 'emotional', 'care', 'empathy', 'listen', 'support', 'feelings', 'compassion', 'sensitive'],
        'description': 'The Deep Connector'
    },
    'Sunlight Yellow': {
        'keywords': ['adventure', 'explore', 'fun', 'travel', 'new', 'exciting', 'spontaneous', 'freedom', 'happy', 'optimistic', 'energy', 'creative'],
        'description': 'The Joyful Explorer'
    },
    'Forest Green': {
        'keywords': ['growing', 'balance', 'peace', 'nature', 'sustainable', 'mindful', 'harmony', 'calm', 'stability', 'grounded', 'patient', 'nurture'],
        'description': 'The Steady Builder'
    },
    'Amber Gold': {
        'keywords': ['teach', 'mentor', 'share', 'wisdom', 'guide', 'support', 'inspire', 'knowledge', 'experience', 'generous', 'warm', 'advise'],
        'description': 'The Warm Mentor'
    },
    'Lavender Purple': {
        'keywords': ['create', 'art', 'imagine', 'design', 'express', 'beauty', 'intuitive', 'artistic', 'vision', 'inspiration', 'original', 'innovative'],
        'description': 'The Creative Dreamer'
    },
    'Coral Pink': {
        'keywords': ['friends', 'laugh', 'positive', 'social', 'energy', 'vibrant', 'enthusiastic', 'playful', 'joy', 'connection', 'upbeat', 'cheerful'],
        'description': 'The Playful Optimist'
    },
    'Earth Brown': {
        'keywords': ['real', 'honest', 'loyal', 'practical', 'roots', 'family', 'traditional', 'authentic', 'reliable', 'trustworthy', 'down-to-earth', 'genuine'],
        'description': 'The Grounded Realist'
    }
}

def preprocess_text(text: str) -> str:
    """Clean and normalize text"""
    text = text.lower()
    text = re.sub(r'[^\w\s]', ' ', text)  # Remove punctuation
    text = re.sub(r'\s+', ' ', text)  # Remove extra spaces
    return text.strip()

def keyword_scoring(text: str) -> Dict[str, float]:
    """Score colors based on keyword matching"""
    text = preprocess_text(text)
    words = set(text.split())
    
    scores = {}
    for color, profile in COLOR_PROFILES.items():
        keyword_matches = sum(1 for keyword in profile['keywords'] if keyword in text)
        scores[color] = keyword_matches / len(profile['keywords'])
    
    return scores

def semantic_scoring(text: str) -> Dict[str, float]:
    """Score colors using semantic similarity (ML)"""
    # Create embeddings
    text_embedding = model.encode(text, convert_to_tensor=False)
    
    scores = {}
    for color, profile in COLOR_PROFILES.items():
        # Create color profile text from keywords
        profile_text = ' '.join(profile['keywords'])
        profile_embedding = model.encode(profile_text, convert_to_tensor=False)
        
        # Calculate cosine similarity
        similarity = np.dot(text_embedding, profile_embedding) / (
            np.linalg.norm(text_embedding) * np.linalg.norm(profile_embedding)
        )
        scores[color] = float(similarity)
    
    return scores

def normalize_scores(scores: Dict[str, float]) -> Dict[str, float]:
    """Normalize scores to sum to 1.0"""
    total = sum(scores.values())
    if total == 0:
        return {color: 1/len(scores) for color in scores}
    return {color: score/total for color, score in scores.items()}

def analyze_personality(life_story: str) -> Dict:
    """
    Analyze a user's life story and return color personality results
    
    Returns:
        {
            'primary_color': str,
            'color_scores': Dict[str, float],
            'personality_vector': List[float],
            'confidence': float
        }
    """
    if not life_story or len(life_story.strip()) < 20:
        # Default to balanced if story is too short
        return {
            'primary_color': 'Ocean Blue',
            'color_scores': {color: 0.125 for color in COLOR_PROFILES.keys()},
            'personality_vector': [0.125] * 8,
            'confidence': 0.3
        }
    
    # Get both keyword and semantic scores
    keyword_scores = keyword_scoring(life_story)
    semantic_scores = semantic_scoring(life_story)
    
    # Combine scores (60% keywords, 40% semantic)
    combined_scores = {}
    for color in COLOR_PROFILES.keys():
        combined_scores[color] = (
            0.6 * keyword_scores[color] + 
            0.4 * semantic_scores[color]
        )
    
    # Normalize
    final_scores = normalize_scores(combined_scores)
    
    # Get primary color (highest score)
    primary_color = max(final_scores, key=final_scores.get)
    
    # Calculate confidence (how much primary color stands out)
    sorted_scores = sorted(final_scores.values(), reverse=True)
    confidence = sorted_scores[0] - sorted_scores[1] if len(sorted_scores) > 1 else sorted_scores[0]
    
    # Create personality vector (for similarity matching)
    personality_vector = [final_scores[color] for color in sorted(COLOR_PROFILES.keys())]
    
    return {
        'primary_color': primary_color,
        'color_scores': final_scores,
        'personality_vector': personality_vector,
        'confidence': float(confidence)
    }

def calculate_compatibility(vector1: List[float], vector2: List[float]) -> float:
    """
    Calculate compatibility score between two personality vectors
    Returns a score between 0 and 1
    """
    if not vector1 or not vector2:
        return 0.5
    
    # Cosine similarity
    v1 = np.array(vector1)
    v2 = np.array(vector2)
    
    similarity = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
    
    # Convert from [-1, 1] to [0, 1]
    compatibility = (similarity + 1) / 2
    
    return float(compatibility)

# Test function
if __name__ == "__main__":
    test_story = """
    I'm an ambitious person who loves to compete and achieve my goals. 
    I thrive on challenges and always strive to be the best at what I do.
    Leadership comes naturally to me, and I'm driven to succeed in everything.
    """
    
    result = analyze_personality(test_story)
    print(f"Primary Color: {result['primary_color']}")
    print(f"Confidence: {result['confidence']:.2f}")
    print("\nColor Scores:")
    for color, score in sorted(result['color_scores'].items(), key=lambda x: x[1], reverse=True):
        print(f"  {color}: {score:.3f}")