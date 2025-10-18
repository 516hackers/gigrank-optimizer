from fiverr_analyzer import DeepFiverrAnalyzer
import pandas as pd
import json

def main():
    print("🚀 ADVANCED FIVERR GIG OPTIMIZER")
    print("=" * 60)
    print("This tool will perform deep market analysis and create")
    print("high-converting gig content for maximum visibility & sales!")
    print("=" * 60)
    
    # Initialize analyzer
    analyzer = DeepFiverrAnalyzer()
    
    # Get comprehensive service details
    service_details = get_service_details()
    
    # Run comprehensive analysis
    try:
        print(f"\n🎯 Analyzing market for: {service_details['service_type']}")
        print("This may take 2-3 minutes...")
        
        results = analyzer.comprehensive_analysis(service_details)
        
        # Display comprehensive results
        display_comprehensive_results(results)
        
    except Exception as e:
        print(f"\n❌ Analysis failed: {e}")
        print("\n🔧 Attempting fallback analysis...")
        
        # Try fallback analysis
        try:
            results = fallback_analysis(service_details)
            display_comprehensive_results(results)
        except Exception as fallback_error:
            print(f"❌ Fallback also failed: {fallback_error}")
            print("Please check your internet connection and try again.")
            print("You can also try using fewer keywords.")

def get_service_details():
    """Get comprehensive service details from user"""
    print("\n📝 SERVICE INFORMATION")
    print("-" * 30)
    
    service_type = input("What is your main service type? (e.g., 'WordPress Bug Fixing', 'Logo Design'): ").strip()
    if not service_type:
        service_type = "Web Development"
    
    target_audience = input("Who is your target audience? (e.g., 'small businesses', 'startups', 'individuals'): ").strip()
    if not target_audience:
        target_audience = "businesses and individuals"
    
    print("\n💡 KEYWORD SUGGESTIONS")
    print("Enter related keywords or services (one per line, empty to finish):")
    additional_keywords = []
    while True:
        keyword = input().strip()
        if not keyword:
            break
        additional_keywords.append(keyword)
    
    # Add common related keywords if none provided
    if not additional_keywords:
        additional_keywords = get_default_keywords(service_type)
        print("Using default keywords for analysis...")
    
    unique_selling_points = input("\nWhat makes your service unique? (e.g., 'fast delivery', '24/7 support'): ").strip()
    
    return {
        'service_type': service_type,
        'target_audience': target_audience,
        'additional_keywords': additional_keywords,
        'unique_selling_points': unique_selling_points,
        'experience_level': 'professional'
    }

def get_default_keywords(service_type):
    """Get default keywords based on service type"""
    service_keywords = {
        'web development': ['website bug fixing', 'error resolution', 'code debugging', 'performance optimization', 'website maintenance'],
        'graphic design': ['logo design', 'brand identity', 'business card', 'social media graphics', 'vector illustration'],
        'digital marketing': ['seo optimization', 'social media marketing', 'content strategy', 'email marketing', 'google ads'],
        'writing': ['content writing', 'article writing', 'blog posts', 'copywriting', 'proofreading'],
        'video editing': ['video production', 'video editing', 'motion graphics', 'youtube videos', 'commercial videos']
    }
    
    for key, keywords in service_keywords.items():
        if key in service_type.lower():
            return keywords
    
    return ['professional service', 'expert work', 'quality delivery', 'fast service', 'affordable pricing']

def display_comprehensive_results(results):
    """Display comprehensive analysis results"""
    print("\n" + "=" * 60)
    print("🎉 COMPREHENSIVE ANALYSIS COMPLETE!")
    print("=" * 60)
    
    keyword_data = results['keyword_analysis']
    gig_content = results['gig_content']
    competitor_insights = results['competitor_insights']
    
    # Display top keywords
    print("\n🏆 TOP 5 HIGH-POTENTIAL KEYWORDS:")
    print("-" * 50)
    top_keywords = keyword_data.head(5)
    for i, (_, row) in enumerate(top_keywords.iterrows(), 1):
        print(f"{i}. {row['keyword']}")
        print(f"   📊 Score: {row['comprehensive_score']:.2f}/10 | ")
        print(f"   💰 Avg Price: ${row['avg_price']:.2f} | ")
        print(f"   🎯 Competition: {row['competition_score']}/10")
        print(f"   📈 Search Volume: {int(row['search_volume_estimate'])}")
        print()
    
    # Display recommended titles
    print("\n💡 OPTIMIZED GIG TITLES (Choose one):")
    print("-" * 50)
    for i, title in enumerate(gig_content['titles'][:3], 1):
        print(f"{i}. {title}")
        print(f"   Length: {len(title)}/80 characters")
        print()
    
    # Display pricing strategy
    print("\n💰 COMPETITIVE PRICING STRATEGY:")
    print("-" * 50)
    packages = gig_content['packages']
    for package, details in packages.items():
        print(f"   {details['name']}: ${details['price']} - {details['delivery_time']}")
        print(f"   Best for: {details['recommended_for']}")
        print()
    
    # Display tags
    print("\n🏷️ OPTIMIZED TAGS:")
    print("-" * 50)
    print(f"   {', '.join(gig_content['tags'])}")
    
    # Display market insights
    print("\n📈 MARKET INSIGHTS:")
    print("-" * 50)
    pricing_benchmarks = competitor_insights.get('pricing_benchmarks', {})
    if pricing_benchmarks:
        print(f"   Market Price Range: ${pricing_benchmarks.get('min_price', 0)} - ${pricing_benchmarks.get('max_price', 0)}")
        print(f"   Average Market Price: ${pricing_benchmarks.get('avg_price', 0):.2f}")
    
    # Display success predictions
    print("\n🎯 SUCCESS PREDICTIONS:")
    print("-" * 50)
    print("   With proper implementation, you can expect:")
    print("   • First order within 1-2 weeks")
    print("   • Steady growth in impressions and clicks")
    print("   • 2-5% conversion rate from clicks to orders")
    print("   • Rising seller level within 2-3 months")
    
    # Display next steps
    print("\n🚀 IMMEDIATE NEXT STEPS:")
    print("-" * 50)
    print("   1. Review 'complete_gig_content.json' for full gig structure")
    print("   2. Choose your favorite title from 'gig_titles.txt'")
    print("   3. Use the description from 'gig_description.txt'")
    print("   4. Set up packages as shown in 'gig_packages.txt'")
    print("   5. Add professional images and portfolio examples")
    print("   6. Use all 5 recommended tags")
    print("   7. Enable notifications and respond quickly to messages")
    
    # Display files created
    print("\n💾 FILES CREATED FOR YOU:")
    print("-" * 50)
    files = [
        "comprehensive_keyword_analysis.csv - Detailed keyword data",
        "complete_gig_content.json - Complete gig structure", 
        "competitor_analysis.json - Market insights",
        "analysis_summary.json - Executive summary",
        "gig_titles.txt - Title recommendations",
        "gig_description.txt - Optimized description",
        "gig_tags.txt - Recommended tags",
        "gig_packages.txt - Package details",
        "gig_faq.txt - FAQ section"
    ]
    for file in files:
        print(f"   📄 {file}")
    
    print("\n" + "=" * 60)
    print("🌟 YOUR FIVERR SUCCESS JOURNEY STARTS NOW!")
    print("=" * 60)
    print("\nImplement these recommendations and watch your gig grow!")
    print("Remember: Consistency and quality service are key to long-term success.")

def fallback_analysis(service_details):
    """Provide fallback analysis when main analysis fails"""
    from gig_optimizer import AdvancedGigOptimizer
    
    print("🔄 Running fallback analysis with template data...")
    
    # Create template keyword data
    keyword_data = [
        {
            'keyword': service_details['service_type'],
            'gig_count': 75,
            'avg_price': 55.0,
            'search_volume_estimate': 350,
            'competition_score': 6,
            'conversion_potential': 7.5,
            'trend_score': 1.5,
            'comprehensive_score': 8.2
        },
        {
            'keyword': f"professional {service_details['service_type']}",
            'gig_count': 45,
            'avg_price': 75.0,
            'search_volume_estimate': 280,
            'competition_score': 4,
            'conversion_potential': 8.0,
            'trend_score': 1.8,
            'comprehensive_score': 8.5
        },
        {
            'keyword': f"expert {service_details['service_type']}",
            'gig_count': 35,
            'avg_price': 85.0,
            'search_volume_estimate': 220,
            'competition_score': 3,
            'conversion_potential': 8.5,
            'trend_score': 1.6,
            'comprehensive_score': 8.8
        }
    ]
    
    df = pd.DataFrame(keyword_data)
    
    # Create gig content
    gig_optimizer = AdvancedGigOptimizer()
    gig_content = gig_optimizer.create_high_converting_gig(
        df, 
        service_details, 
        {}  # Empty competitor insights
    )
    
    return {
        'keyword_analysis': df,
        'gig_content': gig_content,
        'competitor_insights': {},
        'service_details': service_details
    }

def open_results_viewer():
    """Open the results viewer GUI"""
    try:
        from results_viewer import main as viewer_main
        viewer_main()
    except ImportError:
        print("Results viewer not available. Make sure results_viewer.py is in the same directory.")
    except Exception as e:
        print(f"Error opening results viewer: {e}")

if __name__ == "__main__":
    # Run main analysis first
    main()
    
    # After analysis, ask if user wants to view in GUI
    print("\n" + "=" * 60)
    view_gui = input("Would you like to view the results in a GUI? (y/n): ").lower().strip()
    
    if view_gui == 'y':
        open_results_viewer()
