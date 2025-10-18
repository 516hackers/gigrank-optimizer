
import json
import re
from textblob import TextBlob
import numpy as np
import pandas as pd
from datetime import datetime

class AdvancedGigOptimizer:
    def __init__(self):
        self.optimized_content = {}
    
    def create_high_converting_gig(self, keyword_data, service_details, competitor_insights):
        """Create complete high-converting gig content"""
        
        # Extract best keywords
        keyword_clusters = self.extract_keyword_clusters(keyword_data)
        
        # Generate all gig components
        gig_content = {
            'metadata': {
                'created_date': datetime.now().isoformat(),
                'service_type': service_details['service_type'],
                'target_audience': service_details.get('target_audience', 'general'),
                'competition_level': self.assess_competition_level(keyword_data)
            },
            'titles': self.generate_seo_titles(keyword_clusters, service_details, competitor_insights),
            'description': self.generate_high_converting_description(keyword_clusters, service_details, competitor_insights),
            'tags': self.generate_optimized_tags(keyword_clusters),
            'packages': self.generate_competitive_packages(service_details, competitor_insights),
            'faq': self.generate_faq_section(service_details),
            'requirements': self.generate_requirements_section(service_details),
            'seo_optimization': self.generate_seo_recommendations(keyword_clusters),
            'conversion_tips': self.generate_conversion_optimization_tips()
        }
        
        self.optimized_content = gig_content
        return gig_content
    
    def extract_keyword_clusters(self, keyword_data):
        """Extract and categorize keywords"""
        top_keywords = keyword_data.nlargest(10, 'comprehensive_score')
        
        return {
            'primary': top_keywords.iloc[0]['keyword'],
            'secondary': top_keywords.iloc[1:3]['keyword'].tolist(),
            'supporting': top_keywords.iloc[3:6]['keyword'].tolist(),
            'long_tail': top_keywords.iloc[6:]['keyword'].tolist()
        }
    
    def generate_seo_titles(self, keywords, service_details, competitor_insights):
        """Generate SEO-optimized title variations"""
        primary = keywords['primary']
        secondary = keywords['secondary']
        
        titles = []
        
        # Pattern 1: Professional + Primary Keyword
        titles.append(f"Professional {primary} Service | Expert {service_details['service_type']}")
        
        # Pattern 2: I will + Primary + Secondary
        if secondary:
            titles.append(f"I will {primary} and {secondary[0]} | {service_details['service_type']} Expert")
        
        # Pattern 3: Premium + Primary
        titles.append(f"Premium {primary} | Fast Delivery | 100% Satisfaction")
        
        # Pattern 4: Based on competitor analysis
        if competitor_insights.get('common_title_words'):
            common_words = list(competitor_insights['common_title_words'].keys())[:3]
            title_words = ' '.join(common_words[:2])
            titles.append(f"I will {title_words} {primary} professionally")
        
        # Pattern 5: Problem-solution format
        titles.append(f"Expert {primary} Service - Get Professional {service_details['service_type']} Solutions")
        
        # Ensure titles are within Fiverr limits
        titles = [title[:79] for title in titles]
        
        return titles
    
    def generate_high_converting_description(self, keywords, service_details, competitor_insights):
        """Generate high-converting gig description"""
        
        description = f"""
🌟 **PROFESSIONAL {service_details['service_type'].upper()} SERVICES** 🌟

<strong>Looking for expert {service_details['service_type']} services? You've found the perfect solution!</strong>

I specialize in <strong>{keywords['primary']}</strong> and provide top-quality {service_details['service_type'].lower()} services that deliver real results. With years of experience and hundreds of satisfied clients, I understand what it takes to succeed in today's competitive market.

🎯 <strong>WHAT I OFFER:</strong>
✅ Professional {keywords['primary']}
✅ Expert {keywords['secondary'][0] if keywords['secondary'] else service_details['service_type']}
✅ Quality {keywords['secondary'][1] if len(keywords['secondary']) > 1 else 'solutions'}
✅ Fast {keywords['supporting'][0] if keywords['supporting'] else 'delivery'}
✅ Premium {keywords['supporting'][1] if len(keywords['supporting']) > 1 else 'service'}

🔥 <strong>WHY CHOOSE ME OVER OTHER FREELANCERS?</strong>
• <strong>Proven Track Record:</strong> 100+ successful projects completed
• <strong>Rapid Delivery:</strong> Most projects completed within 24-48 hours
• <strong>24/7 Availability:</strong> Always here when you need me
• <strong>Unlimited Revisions:</strong> Your satisfaction is guaranteed
• <strong>Professional Quality:</strong> Industry-best standards and practices

📊 <strong>MY {service_details['service_type'].upper()} PROCESS:</strong>
1. <strong>Consultation:</strong> We discuss your specific needs and goals
2. <strong>Planning:</strong> I create a customized strategy for your project
3. <strong>Execution:</strong> Professional implementation with regular updates
4. <strong>Delivery:</strong> High-quality results delivered on time
5. <strong>Support:</strong> Ongoing assistance and revisions if needed

💼 <strong>SERVICES INCLUDE:</strong>
• {keywords['primary']}
• {keywords['secondary'][0] if keywords['secondary'] else 'Professional Service'}
• {keywords['supporting'][0] if keywords['supporting'] else 'Quality Work'}
• {keywords['long_tail'][0] if keywords['long_tail'] else 'Expert Solutions'}
• And much more!

🚀 <strong>READY TO GET STARTED?</strong>

<strong>Click "Order Now" to begin your project!</strong>

I'm excited to help you achieve your goals with professional {service_details['service_type'].lower()} services. Don't hesitate to message me with any questions - I'm here to help!

<strong>Why wait? Let's create something amazing together! 🎉</strong>

<em>Note: Contact me before ordering to discuss your specific requirements and get a customized quote.</em>
"""
        return description
    
    def generate_optimized_tags(self, keywords):
        """Generate optimized tags for maximum visibility"""
        tags = []
        
        # Primary keyword
        tags.append(keywords['primary'].replace(' ', ''))
        
        # Secondary keywords
        for keyword in keywords['secondary'][:2]:
            tags.append(keyword.replace(' ', ''))
        
        # Supporting keywords
        for keyword in keywords['supporting'][:2]:
            tags.append(keyword.replace(' ', ''))
        
        # Ensure we have 5 tags
        while len(tags) < 5:
            tags.append(f"service{len(tags)+1}")
        
        return tags[:5]
    
    def generate_competitive_packages(self, service_details, competitor_insights):
        """Generate competitive pricing packages"""
        
        # Get pricing benchmarks
        pricing = competitor_insights.get('recommended_price_range', {})
        
        packages = {
            'basic': {
                'name': 'Starter Package',
                'price': pricing.get('low', 25),
                'delivery_time': '3 days',
                'description': 'Perfect for small projects and basic needs',
                'features': [
                    'Basic service delivery',
                    'Standard quality',
                    '1 revision',
                    'Source files included',
                    'Email support'
                ],
                'recommended_for': 'Small projects, testing services'
            },
            'standard': {
                'name': 'Professional Package',
                'price': pricing.get('medium', 50),
                'delivery_time': '2 days',
                'description': 'Most popular choice for professional results',
                'features': [
                    'Enhanced service delivery',
                    'High quality standards',
                    '3 revisions',
                    'Source files included',
                    'Priority support',
                    'Commercial use license'
                ],
                'recommended_for': 'Business projects, professional needs'
            },
            'premium': {
                'name': 'Enterprise Package',
                'price': pricing.get('high', 100),
                'delivery_time': '1 day',
                'description': 'Complete solution for complex requirements',
                'features': [
                    'Full service delivery',
                    'Premium quality guarantee',
                    'Unlimited revisions',
                    'Source files included',
                    '24/7 priority support',
                    'Commercial use license',
                    'Rush delivery',
                    'Dedicated project manager'
                ],
                'recommended_for': 'Complex projects, enterprise solutions'
            }
        }
        
        return packages
    
    def generate_faq_section(self, service_details):
        """Generate FAQ section"""
        faqs = [
            {
                'question': f"What do I need to provide to get started with your {service_details['service_type']} service?",
                'answer': f"Please provide detailed requirements, any relevant files or information, and your specific goals for the project. The more information you share, the better I can meet your expectations."
            },
            {
                'question': "How long does delivery typically take?",
                'answer': "Delivery times vary by package: Basic (3 days), Standard (2 days), Premium (1 day). Rush delivery is available for urgent projects."
            },
            {
                'question': "Do you offer revisions?",
                'answer': "Yes! I offer 1 revision for Basic, 3 revisions for Standard, and unlimited revisions for Premium packages. Your satisfaction is guaranteed."
            },
            {
                'question': "What if I'm not satisfied with the work?",
                'answer': "Your satisfaction is my top priority. I offer unlimited revisions on Premium packages and will work with you until you're completely happy with the results."
            },
            {
                'question': "Can I contact you before placing an order?",
                'answer': "Absolutely! I highly recommend messaging me first to discuss your project details and ensure I'm the right fit for your needs."
            }
        ]
        
        return faqs
    
    def generate_requirements_section(self, service_details):
        """Generate requirements section"""
        return [
            "Detailed project requirements and specifications",
            "Any relevant files, documents, or reference materials",
            "Your preferred timeline and delivery expectations",
            "Specific goals or outcomes you want to achieve",
            "Any branding guidelines or style preferences"
        ]
    
    def assess_competition_level(self, keyword_data):
        """Assess overall competition level"""
        avg_competition = keyword_data['competition_score'].mean()
        
        if avg_competition <= 3:
            return "Low"
        elif avg_competition <= 6:
            return "Medium"
        else:
            return "High"
    
    def generate_seo_recommendations(self, keywords):
        """Generate SEO optimization recommendations"""
        return {
            'primary_keyword': keywords['primary'],
            'secondary_keywords': keywords['secondary'],
            'title_optimization': f"Include '{keywords['primary']}' in title",
            'description_optimization': f"Use '{keywords['primary']}' 2-3 times in description",
            'tag_strategy': "Use mix of broad and specific tags",
            'content_suggestions': [
                f"Create portfolio items featuring {keywords['primary']}",
                f"Use '{keywords['secondary'][0]}' in gig images",
                f"Highlight experience with {keywords['supporting'][0]}"
            ]
        }
    
    def generate_conversion_optimization_tips(self):
        """Generate conversion rate optimization tips"""
        return [
            "Use high-quality, professional gig images",
            "Add video introduction to increase trust",
            "Showcase portfolio with before/after examples",
            "Highlight client testimonials and reviews",
            "Use clear call-to-action buttons",
            "Offer multiple package options",
            "Include urgency elements (limited time offers)",
            "Provide quick response time to messages"
        ]
    
    def save_complete_gig_content(self, filename):
        """Save complete gig content to file"""
        serializable_content = self._convert_to_serializable(self.optimized_content)
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(serializable_content, f, indent=2, ensure_ascii=False)
    
    def _convert_to_serializable(self, obj):
        """Convert numpy/pandas types to native Python types"""
        if isinstance(obj, (np.integer, np.int64)):
            return int(obj)
        elif isinstance(obj, (np.floating, np.float64)):
            return float(obj)
        elif isinstance(obj, np.bool_):
            return bool(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, pd.DataFrame):
            return obj.to_dict('records')
        elif isinstance(obj, pd.Series):
            return obj.to_dict()
        elif isinstance(obj, dict):
            return {key: self._convert_to_serializable(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [self._convert_to_serializable(item) for item in obj]
        else:
            return obj
