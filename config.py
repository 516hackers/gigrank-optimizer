import os
from dotenv import load_dotenv

load_dotenv()

# Analysis parameters
KEYWORD_METRICS = {
    'search_volume': 0.25,
    'competition': 0.20,
    'conversion_rate': 0.20,
    'price_potential': 0.20,
    'trend_score': 0.15
}

# Gig optimization settings
MAX_TITLE_LENGTH = 80
MAX_TAGS = 5
DESCRIPTION_WORD_RANGE = (300, 800)
BEST_PRACTICES = {
    'title_power_words': ['Professional', 'Expert', 'Premium', 'Quality', 'Fast', 'Guaranteed'],
    'description_cta': ['Order Now', 'Contact Me', 'Get Started', 'Hire Me'],
    'urgency_phrases': ['Limited Time', 'Special Offer', 'Book Now'],
    'trust_indicators': ['24/7 Support', 'Money Back', 'Satisfaction Guaranteed']
}
