import pandas as pd
from keyword_research import AdvancedKeywordResearch
from gig_optimizer import AdvancedGigOptimizer
from competitor_analysis import CompetitorAnalyzer
import json

class DeepFiverrAnalyzer:
    def __init__(self):
        self.keyword_researcher = AdvancedKeywordResearch()
        self.gig_optimizer = AdvancedGigOptimizer()
        self.competitor_analyzer = CompetitorAnalyzer()
    
    def comprehensive_analysis(self, service_details):
        """Perform comprehensive analysis and gig creation"""
        
        print("🚀 Starting comprehensive Fiverr analysis...")
        print("=" * 60)
        
        # Step 1: Deep keyword research
        print("\n📊 STEP 1: Keyword Research & Market Analysis")
        keyword_data = self.keyword_researcher.deep_keyword_analysis(
            service_details['service_type'],
            service_details.get('additional_keywords', [])
        )
        
        # Step 2: Competitor analysis for top keyword
        top_keyword = keyword_data.iloc[0]['keyword']
        print(f"\n🔍 STEP 2: Competitor Analysis for '{top_keyword}'")
        competitors = self.competitor_analyzer.analyze_top_competitors(top_keyword, 5)
        competitor_insights = self.competitor_analyzer.get_optimization_insights(competitors, top_keyword)
        
        # Step 3: Create optimized gig content
        print("\n🎯 STEP 3: Creating High-Converting Gig Content")
        gig_content = self.gig_optimizer.create_high_converting_gig(
            keyword_data, service_details, competitor_insights
        )
        
        # Step 4: Generate reports and save
        print("\n💾 STEP 4: Generating Reports & Files")
        self.save_comprehensive_results(keyword_data, gig_content, competitor_insights, service_details)
        
        return {
            'keyword_analysis': keyword_data,
            'gig_content': gig_content,
            'competitor_insights': competitor_insights,
            'service_details': service_details
        }
    
    def save_comprehensive_results(self, keyword_data, gig_content, competitor_insights, service_details):
        """Save all analysis results"""
        try:
            # Save keyword analysis
            keyword_data.to_csv('comprehensive_keyword_analysis.csv', index=False)
            
            # Save gig content
            self.gig_optimizer.save_complete_gig_content('complete_gig_content.json')
            
            # Save competitor insights
            with open('competitor_analysis.json', 'w', encoding='utf-8') as f:
                json.dump(competitor_insights, f, indent=2, ensure_ascii=False)
            
            # Save individual gig components
            self.save_individual_gig_files(gig_content)
            
            # Save summary report
            self.generate_summary_report(keyword_data, gig_content, competitor_insights, service_details)
            
            print("✅ All files saved successfully!")
            
        except Exception as e:
            print(f"⚠️ Error saving files: {e}")
    
    def save_individual_gig_files(self, gig_content):
        """Save individual gig component files"""
        # Titles
        with open('gig_titles.txt', 'w', encoding='utf-8') as f:
            f.write("RECOMMENDED GIG TITLES:\n")
            f.write("=" * 50 + "\n")
            for i, title in enumerate(gig_content['titles'], 1):
                f.write(f"{i}. {title}\n")
        
        # Description
        with open('gig_description.txt', 'w', encoding='utf-8') as f:
            f.write(gig_content['description'])
        
        # Tags
        with open('gig_tags.txt', 'w', encoding='utf-8') as f:
            f.write(", ".join(gig_content['tags']))
        
        # Packages
        with open('gig_packages.txt', 'w', encoding='utf-8') as f:
            f.write("RECOMMENDED PACKAGES:\n")
            f.write("=" * 50 + "\n")
            for package, details in gig_content['packages'].items():
                f.write(f"\n{details['name'].upper()} - ${details['price']}\n")
                f.write(f"Delivery: {details['delivery_time']}\n")
                f.write(f"Description: {details['description']}\n")
                f.write("Features:\n")
                for feature in details['features']:
                    f.write(f"  • {feature}\n")
        
        # FAQ
        with open('gig_faq.txt', 'w', encoding='utf-8') as f:
            f.write("FREQUENTLY ASKED QUESTIONS:\n")
            f.write("=" * 50 + "\n")
            for i, faq in enumerate(gig_content['faq'], 1):
                f.write(f"\nQ{i}: {faq['question']}\n")
                f.write(f"A: {faq['answer']}\n")
    
    def generate_summary_report(self, keyword_data, gig_content, competitor_insights, service_details):
        """Generate comprehensive summary report"""
        report = {
            'analysis_summary': {
                'service_analyzed': service_details['service_type'],
                'total_keywords_researched': len(keyword_data),
                'top_keyword': keyword_data.iloc[0]['keyword'],
                'top_keyword_score': float(keyword_data.iloc[0]['comprehensive_score']),
                'competition_level': gig_content['metadata']['competition_level'],
                'recommended_starting_price': gig_content['packages']['basic']['price'],
                'market_opportunity_score': self.calculate_market_opportunity(keyword_data)
            },
            'key_recommendations': self.generate_key_recommendations(keyword_data, competitor_insights),
            'success_metrics': self.calculate_success_metrics(keyword_data, competitor_insights),
            'implementation_checklist': self.create_implementation_checklist()
        }
        
        with open('analysis_summary.json', 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
    
    def calculate_market_opportunity(self, keyword_data):
        """Calculate overall market opportunity score"""
        top_5 = keyword_data.head(5)
        avg_score = top_5['comprehensive_score'].mean()
        avg_competition = top_5['competition_score'].mean()
        
        # Higher score + lower competition = better opportunity
        opportunity = (avg_score * 0.7) + ((10 - avg_competition) * 0.3)
        return round(opportunity, 2)
    
    def generate_key_recommendations(self, keyword_data, competitor_insights):
        """Generate key recommendations"""
        recommendations = []
        
        # Keyword recommendations
        top_keyword = keyword_data.iloc[0]
        recommendations.append(f"Focus on '{top_keyword['keyword']}' - Highest potential (Score: {top_keyword['comprehensive_score']:.2f})")
        
        # Pricing recommendations
        pricing = competitor_insights.get('pricing_benchmarks', {})
        if pricing:
            recommendations.append(f"Price competitively: ${pricing.get('min_price', 20)}-${pricing.get('max_price', 100)} range")
        
        # Competition recommendations
        avg_competition = keyword_data['competition_score'].mean()
        if avg_competition > 7:
            recommendations.append("High competition market - Differentiate with unique selling propositions")
        elif avg_competition < 4:
            recommendations.append("Low competition - Great opportunity for quick ranking")
        
        # General best practices
        recommendations.extend([
            "Use all 5 tag slots with relevant keywords",
            "Include professional gig images and video",
            "Offer multiple package options",
            "Respond to messages within 2 hours",
            "Ask satisfied clients for reviews"
        ])
        
        return recommendations
    
    def calculate_success_metrics(self, keyword_data, competitor_insights):
        """Calculate potential success metrics"""
        top_keyword = keyword_data.iloc[0]
        
        return {
            'estimated_impressions_per_month': int(top_keyword['search_volume_estimate'] * 0.1),
            'potential_clicks_per_month': int(top_keyword['search_volume_estimate'] * 0.02),
            'expected_conversion_rate': "2-5%",
            'average_order_value': f"${top_keyword['avg_price']:.2f}",
            'time_to_first_order': "1-2 weeks with proper optimization"
        }
    
    def create_implementation_checklist(self):
        """Create implementation checklist"""
        return [
            "Choose best title from recommendations",
            "Use optimized description template",
            "Set up all 3 package tiers",
            "Add professional gig images",
            "Create portfolio items",
            "Set competitive pricing",
            "Use all 5 recommended tags",
            "Prepare quick response templates",
            "Enable notifications for messages",
            "Promote gig on social media initially"
        ]
