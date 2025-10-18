import requests
from bs4 import BeautifulSoup
import re
import time
from fake_useragent import UserAgent
from collections import Counter

class CompetitorAnalyzer:
    def __init__(self):
        self.ua = UserAgent()
        self.session = requests.Session()
    
    def analyze_top_competitors(self, keyword, count=5):
        """Analyze top ranking gigs for a keyword"""
        print(f"🔍 Analyzing top competitors for: {keyword}")
        
        try:
            headers = {'User-Agent': self.ua.random}
            url = f"https://www.fiverr.com/search/gigs?query={keyword.replace(' ', '+')}"
            response = self.session.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            competitors = []
            gig_cards = soup.find_all('article')[:count]
            
            for i, card in enumerate(gig_cards):
                competitor_data = self.extract_gig_data(card, i+1)
                if competitor_data:
                    competitors.append(competitor_data)
            
            return competitors if competitors else self.get_fallback_competitors(keyword)
            
        except Exception as e:
            print(f"Error analyzing competitors for {keyword}: {e}")
            return self.get_fallback_competitors(keyword)
    
    def extract_gig_data(self, card, position):
        """Extract data from a gig card"""
        try:
            # Extract title - multiple possible selectors
            title = "N/A"
            for selector in ['h3', 'a', 'span']:
                title_elements = card.find_all(selector, string=True)
                for element in title_elements:
                    text = element.get_text().strip()
                    if text and len(text) > 10 and len(text) < 100:
                        title = text
                        break
                if title != "N/A":
                    break
            
            # Extract price
            price = 0
            price_elements = card.find_all(string=re.compile(r'\$'))
            for element in price_elements:
                price_match = re.search(r'\$(\d+)', element)
                if price_match:
                    price = int(price_match.group(1))
                    if 5 <= price <= 1000:
                        break
            
            # If no price found, use reasonable default
            if price == 0:
                price = 50  # Reasonable default
            
            return {
                'position': position,
                'title': title,
                'price': price,
                'seller_level': "New Seller",  # Default
                'delivery_time': "2 days"  # Default
            }
            
        except Exception as e:
            print(f"Error extracting gig data: {e}")
            return None
    
    def get_fallback_competitors(self, keyword):
        """Provide fallback competitor data when analysis fails"""
        return [
            {
                'position': 1,
                'title': f"Professional {keyword} service",
                'price': 50,
                'seller_level': "Top Rated",
                'delivery_time': "1 day"
            },
            {
                'position': 2,
                'title': f"Expert {keyword} with fast delivery",
                'price': 35,
                'seller_level': "Level 2",
                'delivery_time': "2 days"
            },
            {
                'position': 3,
                'title': f"Quality {keyword} guaranteed",
                'price': 25,
                'seller_level': "Level 1",
                'delivery_time': "3 days"
            }
        ]
    
    def analyze_title_patterns(self, competitors):
        """Analyze common patterns in competitor titles"""
        if not competitors:
            return {}
            
        titles = [comp['title'] for comp in competitors if comp['title'] != 'N/A']
        
        if not titles:
            return {}
        
        # Analyze word frequency
        all_words = []
        for title in titles:
            words = re.findall(r'\b\w+\b', title.lower())
            all_words.extend(words)
        
        if not all_words:
            return {}
            
        word_freq = Counter(all_words)
        
        # Remove common stop words
        stop_words = {'i', 'will', 'and', 'the', 'for', 'you', 'your', 'with', 'from', 'service'}
        filtered_freq = {word: count for word, count in word_freq.items() 
                        if word not in stop_words and len(word) > 2}
        
        # Convert to regular dict and get top items
        sorted_items = sorted(filtered_freq.items(), key=lambda x: x[1], reverse=True)
        return dict(sorted_items[:10])
    
    def analyze_pricing_strategy(self, competitors):
        """Analyze competitor pricing patterns"""
        if not competitors:
            return {
                'min_price': 20,
                'max_price': 100,
                'avg_price': 50,
                'median_price': 45
            }
        
        prices = [comp['price'] for comp in competitors if comp['price'] > 0]
        
        if not prices:
            return {
                'min_price': 20,
                'max_price': 100,
                'avg_price': 50,
                'median_price': 45
            }
        
        sorted_prices = sorted(prices)
        return {
            'min_price': min(prices),
            'max_price': max(prices),
            'avg_price': sum(prices) / len(prices),
            'median_price': sorted_prices[len(sorted_prices) // 2]
        }
    
    def get_optimization_insights(self, competitors, keyword):
        """Generate optimization insights from competitor analysis"""
        title_patterns = self.analyze_title_patterns(competitors)
        pricing = self.analyze_pricing_strategy(competitors)
        
        insights = {
            'common_title_words': title_patterns,
            'pricing_benchmarks': pricing,
            'recommended_price_range': {
                'low': max(5, pricing.get('min_price', 20) * 0.8),
                'medium': pricing.get('avg_price', 50),
                'high': min(995, pricing.get('max_price', 100) * 1.2)
            },
            'top_performer_characteristics': self.analyze_top_performers(competitors)
        }
        
        return insights
    
    def analyze_top_performers(self, competitors):
        """Analyze characteristics of top performers"""
        if not competitors:
            return {
                'avg_title_length': 45,
                'common_seller_levels': {'Top Rated': 1},
                'delivery_times': ['1 day', '2 days', '3 days'],
                'price_range': {'min': 20, 'max': 100}
            }
        
        top_3 = [comp for comp in competitors if comp['position'] <= 3]
        
        if not top_3:
            top_3 = competitors[:3] if len(competitors) >= 3 else competitors
        
        characteristics = {
            'avg_title_length': sum(len(comp['title']) for comp in top_3) / len(top_3) if top_3 else 45,
            'common_seller_levels': dict(Counter(comp['seller_level'] for comp in top_3)),
            'delivery_times': [comp['delivery_time'] for comp in top_3],
            'price_range': {
                'min': min(comp['price'] for comp in top_3) if top_3 else 20,
                'max': max(comp['price'] for comp in top_3) if top_3 else 100
            }
        }
        
        return characteristics
