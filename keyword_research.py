
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re
from fake_useragent import UserAgent
from competitor_analysis import CompetitorAnalyzer

class AdvancedKeywordResearch:
    def __init__(self):
        self.ua = UserAgent()
        self.session = requests.Session()
        self.competitor_analyzer = CompetitorAnalyzer()
    
    def deep_keyword_analysis(self, primary_service, additional_keywords=[]):
        """Perform deep keyword analysis for a service"""
        print("🎯 Starting deep keyword analysis...")
        
        # Generate related keywords
        all_keywords = self.generate_related_keywords(primary_service, additional_keywords)
        
        # Analyze each keyword
        keyword_data = []
        successful_analyses = 0
        
        for keyword in all_keywords:
            print(f"🔍 Analyzing: {keyword}")
            data = self.analyze_keyword_depth(keyword)
            if data and data.get('gig_count', 0) >= 0:  # Valid data
                keyword_data.append(data)
                successful_analyses += 1
                print(f"   ✅ Found: {data['gig_count']} gigs, Score: {data.get('comprehensive_score', 0):.2f}")
            else:
                print(f"   ⚠️  Using fallback data for: {keyword}")
                # Add fallback data
                fallback_data = self.get_fallback_keyword_data(keyword)
                keyword_data.append(fallback_data)
            
            time.sleep(1.5)  # Be respectful
        
        # Check if we have any valid data
        if not keyword_data:
            print("❌ No keyword data collected. Using comprehensive fallback data.")
            return self.get_comprehensive_fallback_data(primary_service, additional_keywords)
        
        df = pd.DataFrame(keyword_data)
        
        # Calculate comprehensive scores
        df['comprehensive_score'] = self.calculate_comprehensive_score(df)
        
        return df.sort_values('comprehensive_score', ascending=False)
    
    def generate_related_keywords(self, primary_service, additional_keywords):
        """Generate comprehensive list of related keywords"""
        base_keywords = [primary_service.lower()]
        
        # Add user provided keywords
        base_keywords.extend([kw.lower() for kw in additional_keywords])
        
        # Generate common variations
        variations = []
        for keyword in base_keywords:
            variations.extend([
                keyword,
                f"professional {keyword}",
                f"expert {keyword}",
                f"quality {keyword}",
                f"fast {keyword}",
                f"affordable {keyword}",
                f"premium {keyword}",
                keyword.replace(' ', ''),
                keyword + " service",
                keyword + " expert"
            ])
        
        # Remove duplicates and limit
        unique_variations = list(set(variations))
        return unique_variations[:15]  # Limit to 15 keywords
    
    def analyze_keyword_depth(self, keyword):
        """Perform deep analysis of a single keyword"""
        try:
            headers = {'User-Agent': self.ua.random}
            url = f"https://www.fiverr.com/search/gigs?query={keyword.replace(' ', '+')}"
            response = self.session.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Basic metrics
            gig_count = self.extract_gig_count(soup)
            avg_price = self.extract_avg_price(soup)
            
            # If no gigs found, use fallback
            if gig_count == 0:
                return self.get_fallback_keyword_data(keyword)
            
            competition_score = self.calculate_competition_score(gig_count)
            
            # Advanced metrics
            search_volume_estimate = self.estimate_search_volume(keyword, gig_count)
            conversion_potential = self.estimate_conversion_potential(keyword, avg_price)
            trend_score = self.analyze_trend_potential(keyword)
            
            # Competitor analysis with error handling
            try:
                competitors = self.competitor_analyzer.analyze_top_competitors(keyword, 3)
                competitor_insights = self.competitor_analyzer.get_optimization_insights(competitors, keyword)
            except Exception as e:
                print(f"   ⚠️  Competitor analysis failed: {e}")
                competitors = []
                competitor_insights = {}
            
            return {
                'keyword': keyword,
                'gig_count': gig_count,
                'avg_price': avg_price,
                'search_volume_estimate': search_volume_estimate,
                'competition_score': competition_score,
                'conversion_potential': conversion_potential,
                'trend_score': trend_score,
                'comprehensive_score': 0,  # Will be calculated later
                'competitor_data': competitors,
                'market_insights': competitor_insights
            }
            
        except Exception as e:
            print(f"   ❌ Error in deep analysis: {e}")
            return self.get_fallback_keyword_data(keyword)
    
    def get_fallback_keyword_data(self, keyword):
        """Provide fallback data when keyword analysis fails"""
        base_score = len(keyword) * 0.5  # Simple scoring based on keyword length
        
        return {
            'keyword': keyword,
            'gig_count': 50,  # Reasonable default
            'avg_price': 45.0,
            'search_volume_estimate': 200,
            'competition_score': 5,
            'conversion_potential': 6.0,
            'trend_score': 1.5,
            'comprehensive_score': base_score,
            'competitor_data': [],
            'market_insights': {}
        }
    
    def get_comprehensive_fallback_data(self, primary_service, additional_keywords):
        """Provide comprehensive fallback data when all analyses fail"""
        all_keywords = self.generate_related_keywords(primary_service, additional_keywords)
        keyword_data = []
        
        for i, keyword in enumerate(all_keywords):
            data = self.get_fallback_keyword_data(keyword)
            # Add some variation to scores
            data['comprehensive_score'] = 8.0 - (i * 0.3)
            data['gig_count'] = 40 + (i * 10)
            data['avg_price'] = 35.0 + (i * 5)
            keyword_data.append(data)
        
        return pd.DataFrame(keyword_data)
    
    def extract_gig_count(self, soup):
        """Extract number of gigs with multiple methods"""
        try:
            # Method 1: Count gig cards (articles)
            gig_cards = soup.find_all('article')
            if gig_cards:
                return len(gig_cards)
            
            # Method 2: Look for divs with gig-related classes
            gig_divs = soup.find_all('div', class_=re.compile(r'gig|card|item'))
            if gig_divs:
                return len(gig_divs)
            
            # Method 3: Search result count text
            count_texts = soup.find_all(string=re.compile(r'\d+ results?'))
            for text in count_texts:
                numbers = re.findall(r'\d+', text)
                if numbers:
                    return int(numbers[0])
            
            return 0
            
        except:
            return 0
    
    def extract_avg_price(self, soup):
        """Extract average price with better logic"""
        try:
            prices = []
            # Look for price elements
            price_elements = soup.find_all(string=re.compile(r'\$'))
            
            for element in price_elements:
                price_match = re.search(r'\$(\d+)', element)
                if price_match:
                    price = int(price_match.group(1))
                    if 5 <= price <= 1000:  # Reasonable Fiverr price range
                        prices.append(price)
            
            return sum(prices) / len(prices) if prices else 45.0
            
        except:
            return 45.0
    
    def calculate_competition_score(self, gig_count):
        """Calculate competition score (lower is better)"""
        if gig_count == 0:
            return 0
        
        # Logarithmic scale to normalize
        if gig_count <= 50:
            return 3  # Low competition
        elif gig_count <= 200:
            return 6  # Medium competition
        else:
            return 8  # High competition
    
    def estimate_search_volume(self, keyword, gig_count):
        """Estimate search volume based on gig count and keyword characteristics"""
        base_volume = min(gig_count * 15, 1500)  # Rough estimate
        
        # Adjust based on keyword characteristics
        modifiers = {
            'length': max(0.5, 1 - (len(keyword.split()) / 10)),  # Shorter keywords better
            'specificity': 1.2 if len(keyword.split()) > 1 else 0.8,  # More specific better
            'commercial_intent': 1.3 if any(word in keyword for word in ['fix', 'solve', 'create', 'build']) else 0.9
        }
        
        return base_volume * (sum(modifiers.values()) / len(modifiers))
    
    def estimate_conversion_potential(self, keyword, avg_price):
        """Estimate conversion potential"""
        # Higher price + specific intent = better conversion
        price_factor = min(avg_price / 100, 1.0)
        
        intent_keywords = ['fix', 'solve', 'create', 'build', 'make', 'design', 'debug']
        intent_score = 1.2 if any(word in keyword.lower() for word in intent_keywords) else 0.8
        
        return (price_factor + intent_score) / 2 * 10
    
    def analyze_trend_potential(self, keyword):
        """Analyze trend potential of keyword"""
        trending_terms = ['2024', 'ai', 'chatgpt', 'automation', 'responsive', 'seo', 'bug', 'fix']
        trend_score = 1.8 if any(term in keyword.lower() for term in trending_terms) else 1.0
        
        return trend_score
    
    def calculate_comprehensive_score(self, df):
        """Calculate comprehensive keyword score"""
        scores = []
        
        for _, row in df.iterrows():
            score = (
                (row['search_volume_estimate'] / 200) * 0.25 +
                (10 - row['competition_score']) * 0.20 +
                row['conversion_potential'] * 0.20 +
                (row['avg_price'] / 50) * 0.20 +
                row['trend_score'] * 0.15
            )
            scores.append(min(score, 10))
        
        return scores
    
    def get_best_keyword_clusters(self, keyword_data):
        """Group keywords into clusters for content strategy"""
        if len(keyword_data) == 0:
            return {
                'primary_keywords': ['website bug fixing'],
                'secondary_keywords': ['error fixing', 'bug solve'],
                'long_tail_keywords': ['professional bug fixing', 'expert error fix']
            }
        
        df = keyword_data.nlargest(10, 'comprehensive_score')
        
        clusters = {
            'primary_keywords': df.head(3)['keyword'].tolist(),
            'secondary_keywords': df[3:6]['keyword'].tolist() if len(df) > 3 else [],
            'long_tail_keywords': df[6:]['keyword'].tolist() if len(df) > 6 else []
        }
        
        return clusters
