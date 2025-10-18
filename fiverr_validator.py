import re
import json

class FiverrValidator:
    def __init__(self):
        self.rules = {
            'title': {
                'max_length': 80,
                'min_length': 10,
                'forbidden_words': ['free', 'cheap', 'best', 'guaranteed', '100%'],
                'required_elements': ['service_verb', 'service_noun']
            },
            'description': {
                'max_length': 1200,
                'min_length': 100,
                'required_sections': ['introduction', 'services', 'process', 'cta'],
                'forbidden_content': ['external_links', 'contact_info', 'other_platforms']
            },
            'tags': {
                'max_count': 5,
                'min_count': 3,
                'max_length_per_tag': 20,
                'recommended_types': ['service_type', 'skill', 'delivery', 'quality', 'niche']
            },
            'packages': {
                'max_count': 3,
                'min_price': 5,
                'max_price': 995,
                'delivery_time_limits': {
                    'min': 1,
                    'max': 30
                }
            }
        }
    
    def validate_gig_content(self, gig_content):
        """Validate complete gig content against Fiverr rules"""
        validation_report = {
            'is_valid': True,
            'warnings': [],
            'errors': [],
            'suggestions': []
        }
        
        # Validate titles
        title_validation = self.validate_titles(gig_content.get('titles', []))
        validation_report['warnings'].extend(title_validation['warnings'])
        validation_report['errors'].extend(title_validation['errors'])
        
        # Validate description
        desc_validation = self.validate_description(gig_content.get('description', ''))
        validation_report['warnings'].extend(desc_validation['warnings'])
        validation_report['errors'].extend(desc_validation['errors'])
        
        # Validate tags
        tags_validation = self.validate_tags(gig_content.get('tags', []))
        validation_report['warnings'].extend(tags_validation['warnings'])
        validation_report['errors'].extend(tags_validation['errors'])
        
        # Validate packages
        packages_validation = self.validate_packages(gig_content.get('packages', {}))
        validation_report['warnings'].extend(packages_validation['warnings'])
        validation_report['errors'].extend(packages_validation['errors'])
        
        # Overall validity
        if validation_report['errors']:
            validation_report['is_valid'] = False
        
        # Generate suggestions
        validation_report['suggestions'] = self.generate_suggestions(gig_content)
        
        return validation_report
    
    def validate_titles(self, titles):
        """Validate gig titles"""
        validation = {'warnings': [], 'errors': []}
        
        if not titles:
            validation['errors'].append("No titles provided")
            return validation
        
        for i, title in enumerate(titles, 1):
            # Length validation
            if len(title) > self.rules['title']['max_length']:
                validation['errors'].append(f"Title {i} exceeds {self.rules['title']['max_length']} characters")
            elif len(title) < self.rules['title']['min_length']:
                validation['warnings'].append(f"Title {i} is very short ({len(title)} chars)")
            
            # Content validation
            for word in self.rules['title']['forbidden_words']:
                if word.lower() in title.lower():
                    validation['warnings'].append(f"Title {i} contains discouraged word: '{word}'")
        
        return validation
    
    def validate_description(self, description):
        """Validate gig description"""
        validation = {'warnings': [], 'errors': []}
        
        # Length validation
        if len(description) > self.rules['description']['max_length']:
            validation['errors'].append(f"Description exceeds {self.rules['description']['max_length']} characters")
        elif len(description) < self.rules['description']['min_length']:
            validation['warnings'].append(f"Description is very short ({len(description)} chars)")
        
        # Content validation
        if re.search(r'http[s]?://', description):
            validation['errors'].append("Description contains external links")
        
        if re.search(r'@\w+\.\w+', description) or re.search(r'\b\d{10,}\b', description):
            validation['errors'].append("Description contains contact information")
        
        # Section validation
        required_sections = self.rules['description']['required_sections']
        missing_sections = []
        for section in required_sections:
            if section not in description.lower():
                missing_sections.append(section)
        
        if missing_sections:
            validation['warnings'].append(f"Description missing sections: {', '.join(missing_sections)}")
        
        return validation
    
    def validate_tags(self, tags):
        """Validate gig tags"""
        validation = {'warnings': [], 'errors': []}
        
        # Count validation
        if len(tags) > self.rules['tags']['max_count']:
            validation['errors'].append(f"Too many tags ({len(tags)}), maximum is {self.rules['tags']['max_count']}")
        elif len(tags) < self.rules['tags']['min_count']:
            validation['warnings'].append(f"Only {len(tags)} tags used, recommend using all {self.rules['tags']['max_count']}")
        
        # Length validation
        for tag in tags:
            if len(tag) > self.rules['tags']['max_length_per_tag']:
                validation['warnings'].append(f"Tag '{tag}' is too long ({len(tag)} chars)")
        
        return validation
    
    def validate_packages(self, packages):
        """Validate gig packages"""
        validation = {'warnings': [], 'errors': []}
        
        if len(packages) > self.rules['packages']['max_count']:
            validation['errors'].append(f"Too many packages ({len(packages)}), maximum is {self.rules['packages']['max_count']}")
        
        for package_name, package_data in packages.items():
            price = package_data.get('price', 0)
            delivery = package_data.get('delivery_time', '')
            
            # Price validation
            if price < self.rules['packages']['min_price']:
                validation['errors'].append(f"Package '{package_name}' price (${price}) below minimum ${self.rules['packages']['min_price']}")
            elif price > self.rules['packages']['max_price']:
                validation['warnings'].append(f"Package '{package_name}' price (${price}) is very high")
            
            # Delivery time validation
            delivery_days = self.extract_delivery_days(delivery)
            if delivery_days:
                if delivery_days < self.rules['packages']['delivery_time_limits']['min']:
                    validation['warnings'].append(f"Package '{package_name}' delivery time ({delivery_days} days) is very short")
                elif delivery_days > self.rules['packages']['delivery_time_limits']['max']:
                    validation['warnings'].append(f"Package '{package_name}' delivery time ({delivery_days} days) is very long")
        
        return validation
    
    def extract_delivery_days(self, delivery_text):
        """Extract number of days from delivery text"""
        match = re.search(r'(\d+)\s*day', delivery_text.lower())
        return int(match.group(1)) if match else None
    
    def generate_suggestions(self, gig_content):
        """Generate improvement suggestions"""
        suggestions = []
        
        # Title suggestions
        titles = gig_content.get('titles', [])
        if titles:
            primary_title = titles[0]
            if 'i will' not in primary_title.lower():
                suggestions.append("Consider starting your title with 'I will' for better clarity")
        
        # Description suggestions
        description = gig_content.get('description', '')
        if '⭐' not in description and '✅' not in description:
            suggestions.append("Add emojis (⭐✅) to make your description more engaging")
        
        if 'contact me' not in description.lower():
            suggestions.append("Add a clear 'Contact me before ordering' message")
        
        # Package suggestions
        packages = gig_content.get('packages', {})
        if len(packages) < 3:
            suggestions.append("Consider offering 3 packages for better conversion")
        
        # Tag suggestions
        tags = gig_content.get('tags', [])
        if len(tags) < 5:
            suggestions.append(f"Use all 5 available tags (currently using {len(tags)})")
        
        return suggestions

# Update your fiverr_analyzer.py to include validation
def add_validation_to_analyzer():
    """Add validation to the existing analyzer"""
    # This would be integrated into your existing fiverr_analyzer.py
    pass
