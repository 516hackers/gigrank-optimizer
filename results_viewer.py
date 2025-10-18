
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import json
import pandas as pd
import os
from pathlib import Path

class ResultsViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("🚀 GigRank Optimizer - Results Viewer")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f8ff')
        
        # Set up the main frame
        self.setup_gui()
        
        # Check for output files and load them
        self.load_results()
    
    def setup_gui(self):
        """Set up the GUI layout"""
        # Header
        header_frame = tk.Frame(self.root, bg='#2c3e50', height=80)
        header_frame.pack(fill='x', padx=10, pady=10)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame, 
            text="🎯 GigRank Optimizer - Analysis Results", 
            font=('Arial', 20, 'bold'),
            fg='white',
            bg='#2c3e50'
        )
        title_label.pack(expand=True)
        
        subtitle_label = tk.Label(
            header_frame,
            text="Your Complete Fiverr Gig Optimization Results",
            font=('Arial', 12),
            fg='#ecf0f1',
            bg='#2c3e50'
        )
        subtitle_label.pack(expand=True)
        
        # Main content frame
        main_frame = tk.Frame(self.root, bg='#f0f8ff')
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Left sidebar for navigation
        self.setup_sidebar(main_frame)
        
        # Right content area
        self.setup_content_area(main_frame)
    
    def setup_sidebar(self, parent):
        """Set up the navigation sidebar"""
        sidebar_frame = tk.Frame(parent, bg='#34495e', width=250)
        sidebar_frame.pack(side='left', fill='y', padx=(0, 10))
        sidebar_frame.pack_propagate(False)
        
        # Navigation title
        nav_title = tk.Label(
            sidebar_frame,
            text="📊 Results Sections",
            font=('Arial', 14, 'bold'),
            fg='white',
            bg='#34495e',
            pady=15
        )
        nav_title.pack(fill='x')
        
        # Navigation buttons
        nav_buttons = [
            ("📈 Keyword Analysis", self.show_keyword_analysis),
            ("🎯 Gig Content", self.show_gig_content),
            ("💰 Pricing Strategy", self.show_pricing),
            ("🏆 Competitor Insights", self.show_competitor_insights),
            ("📋 Implementation Guide", self.show_implementation),
            ("🚀 Quick Start", self.show_quick_start),
            ("📊 Summary Report", self.show_summary)
        ]
        
        for text, command in nav_buttons:
            btn = tk.Button(
                sidebar_frame,
                text=text,
                font=('Arial', 11),
                fg='#2c3e50',
                bg='#ecf0f1',
                relief='flat',
                padx=10,
                pady=8,
                width=20,
                command=command
            )
            btn.pack(pady=5, padx=10)
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg='#3498db', fg='white'))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg='#ecf0f1', fg='#2c3e50'))
        
        # Refresh button
        refresh_btn = tk.Button(
            sidebar_frame,
            text="🔄 Refresh Results",
            font=('Arial', 11, 'bold'),
            fg='white',
            bg='#e74c3c',
            relief='flat',
            padx=10,
            pady=10,
            command=self.load_results
        )
        refresh_btn.pack(side='bottom', pady=20, padx=10)
    
    def setup_content_area(self, parent):
        """Set up the main content area"""
        content_frame = tk.Frame(parent, bg='white')
        content_frame.pack(side='left', fill='both', expand=True)
        
        # Title for content area
        self.content_title = tk.Label(
            content_frame,
            text="Welcome to GigRank Optimizer Results",
            font=('Arial', 16, 'bold'),
            fg='#2c3e50',
            bg='white',
            pady=10
        )
        self.content_title.pack(fill='x')
        
        # Text area for content
        self.content_text = scrolledtext.ScrolledText(
            content_frame,
            wrap=tk.WORD,
            font=('Arial', 11),
            bg='#f8f9fa',
            fg='#2c3e50',
            padx=15,
            pady=15,
            relief='flat'
        )
        self.content_text.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Status bar
        self.status_bar = tk.Label(
            content_frame,
            text="Ready to display analysis results...",
            font=('Arial', 10),
            fg='#7f8c8d',
            bg='#ecf0f1',
            relief='sunken',
            anchor='w'
        )
        self.status_bar.pack(fill='x', side='bottom')
    
    def load_results(self):
        """Load all result files"""
        self.results = {}
        files_loaded = 0
        
        # Define files to load
        files_to_load = {
            'keyword_analysis': 'comprehensive_keyword_analysis.csv',
            'gig_content': 'complete_gig_content.json',
            'competitor_analysis': 'competitor_analysis.json',
            'summary': 'analysis_summary.json'
        }
        
        for key, filename in files_to_load.items():
            if os.path.exists(filename):
                try:
                    if filename.endswith('.csv'):
                        self.results[key] = pd.read_csv(filename)
                    elif filename.endswith('.json'):
                        with open(filename, 'r', encoding='utf-8') as f:
                            self.results[key] = json.load(f)
                    files_loaded += 1
                except Exception as e:
                    print(f"Error loading {filename}: {e}")
        
        # Load individual text files
        text_files = ['gig_titles.txt', 'gig_description.txt', 'gig_tags.txt', 'gig_packages.txt']
        for file in text_files:
            if os.path.exists(file):
                try:
                    with open(file, 'r', encoding='utf-8') as f:
                        self.results[file.replace('.txt', '')] = f.read()
                    files_loaded += 1
                except Exception as e:
                    print(f"Error loading {file}: {e}")
        
        self.update_status(f"Loaded {files_loaded} result files")
        
        if files_loaded > 0:
            self.show_welcome_message()
        else:
            self.show_no_results_message()
    
    def update_status(self, message):
        """Update status bar"""
        self.status_bar.config(text=message)
    
    def clear_content(self):
        """Clear content area"""
        self.content_text.delete(1.0, tk.END)
    
    def insert_header(self, text, level=1):
        """Insert a header into content"""
        if level == 1:
            self.content_text.insert(tk.END, f"\n{text}\n", 'header1')
            self.content_text.insert(tk.END, "=" * len(text) + "\n\n", 'header1')
        elif level == 2:
            self.content_text.insert(tk.END, f"\n{text}\n", 'header2')
            self.content_text.insert(tk.END, "-" * len(text) + "\n\n", 'header2')
    
    def insert_content(self, text, tag='normal'):
        """Insert content with specified tag"""
        self.content_text.insert(tk.END, text, tag)
    
    def configure_text_tags(self):
        """Configure text styling tags"""
        self.content_text.tag_configure('header1', font=('Arial', 16, 'bold'), foreground='#2c3e50')
        self.content_text.tag_configure('header2', font=('Arial', 14, 'bold'), foreground='#34495e')
        self.content_text.tag_configure('normal', font=('Arial', 11))
        self.content_text.tag_configure('highlight', font=('Arial', 11, 'bold'), foreground='#e74c3c')
        self.content_text.tag_configure('success', font=('Arial', 11), foreground='#27ae60')
        self.content_text.tag_configure('warning', font=('Arial', 11), foreground='#f39c12')
    
    def show_welcome_message(self):
        """Show welcome message with results overview"""
        self.clear_content()
        self.content_title.config(text="🎉 Analysis Complete - Results Overview")
        self.configure_text_tags()
        
        self.insert_header("Welcome to Your Fiverr Gig Optimization Results!", 1)
        
        self.insert_content("Your comprehensive analysis is complete! Here's what we've prepared for you:\n\n")
        
        sections = [
            ("📈 Keyword Analysis", "Top-performing keywords with market data"),
            ("🎯 Gig Content", "Complete gig structure with titles, description, and tags"),
            ("💰 Pricing Strategy", "Competitive pricing based on market analysis"),
            ("🏆 Competitor Insights", "Analysis of top competitors and their strategies"),
            ("📋 Implementation Guide", "Step-by-step setup instructions"),
            ("🚀 Quick Start", "Get your gig live in minutes"),
            ("📊 Summary Report", "Executive summary and key recommendations")
        ]
        
        for title, description in sections:
            self.insert_content(f"• {title}: ", 'highlight')
            self.insert_content(f"{description}\n")
        
        self.insert_content("\n" + "="*50 + "\n\n")
        self.insert_content("💡 ", 'highlight')
        self.insert_content("Use the navigation menu on the left to explore each section.\n\n")
        
        self.insert_content("🚀 ", 'highlight')
        self.insert_content("Ready to launch your optimized Fiverr gig? Start with the 'Quick Start' section!\n")
    
    def show_no_results_message(self):
        """Show message when no results are found"""
        self.clear_content()
        self.content_title.config(text="📊 No Results Found")
        
        self.insert_header("No Analysis Results Found", 1)
        self.insert_content("\nWe couldn't find any analysis results files.\n\n")
        self.insert_content("Please run the main analysis first:\n\n")
        self.insert_content("1. Open your command prompt/terminal\n")
        self.insert_content("2. Navigate to the project directory\n")
        self.insert_content("3. Run: ", 'highlight')
        self.insert_content("python main.py\n\n")
        self.insert_content("4. Complete the analysis process\n")
        self.insert_content("5. Return here to view your results\n")
    
    def show_keyword_analysis(self):
        """Display keyword analysis results"""
        self.clear_content()
        self.content_title.config(text="📈 Keyword Analysis")
        self.configure_text_tags()
        
        if 'keyword_analysis' not in self.results:
            self.insert_content("Keyword analysis data not available.\n")
            return
        
        df = self.results['keyword_analysis']
        
        self.insert_header("Top Performing Keywords", 1)
        self.insert_content("These keywords have the highest potential for your Fiverr gig:\n\n")
        
        # Display top 10 keywords
        top_keywords = df.head(10)
        
        for i, (_, row) in enumerate(top_keywords.iterrows(), 1):
            self.insert_content(f"{i}. ", 'highlight')
            self.insert_content(f"{row['keyword']}\n")
            self.insert_content(f"   📊 Score: {row.get('comprehensive_score', 'N/A'):.2f}/10 | ")
            self.insert_content(f"💰 Avg Price: ${row.get('avg_price', 'N/A'):.2f} | ")
            self.insert_content(f"🎯 Competition: {row.get('competition_score', 'N/A')}/10\n")
            self.insert_content(f"   📈 Search Volume: {int(row.get('search_volume_estimate', 0))} | ")
            self.insert_content(f"🔄 Conversion: {row.get('conversion_potential', 'N/A')}/10\n\n")
        
        self.insert_header("Keyword Strategy Recommendations", 2)
        
        recommendations = [
            "Focus on keywords with high comprehensive scores (7+)",
            "Use a mix of high-competition and low-competition keywords",
            "Include long-tail keywords in your gig description",
            "Monitor performance and adjust keywords regularly"
        ]
        
        for rec in recommendations:
            self.insert_content(f"• {rec}\n")
    
    def show_gig_content(self):
        """Display gig content results"""
        self.clear_content()
        self.content_title.config(text="🎯 Complete Gig Content")
        self.configure_text_tags()
        
        # Show titles
        if 'gig_titles' in self.results:
            self.insert_header("Recommended Gig Titles", 1)
            self.insert_content(self.results['gig_titles'] + "\n\n")
        
        # Show description
        if 'gig_description' in self.results:
            self.insert_header("Optimized Gig Description", 1)
            self.insert_content(self.results['gig_description'] + "\n\n")
        
        # Show tags
        if 'gig_tags' in self.results:
            self.insert_header("Recommended Tags", 1)
            self.insert_content(self.results['gig_tags'] + "\n\n")
        
        if 'gig_content' in self.results:
            gig_data = self.results['gig_content']
            
            # Show FAQ if available
            if 'faq' in gig_data:
                self.insert_header("Frequently Asked Questions", 1)
                for i, faq in enumerate(gig_data['faq'], 1):
                    self.insert_content(f"Q{i}: ", 'highlight')
                    self.insert_content(f"{faq['question']}\n")
                    self.insert_content(f"A: {faq['answer']}\n\n")
            
            # Show requirements if available
            if 'requirements' in gig_data:
                self.insert_header("Customer Requirements", 1)
                for req in gig_data['requirements']:
                    self.insert_content(f"• {req}\n")
                self.insert_content("\n")
    
    def show_pricing(self):
        """Display pricing strategy"""
        self.clear_content()
        self.content_title.config(text="💰 Pricing Strategy")
        self.configure_text_tags()
        
        if 'gig_packages' in self.results:
            self.insert_header("Recommended Pricing Packages", 1)
            self.insert_content(self.results['gig_packages'] + "\n\n")
        
        elif 'gig_content' in self.results and 'packages' in self.results['gig_content']:
            packages = self.results['gig_content']['packages']
            
            for package_name, details in packages.items():
                self.insert_header(f"{details.get('name', package_name.title())} Package", 2)
                self.insert_content(f"Price: ${details['price']}\n")
                self.insert_content(f"Delivery: {details['delivery_time']}\n")
                self.insert_content(f"Description: {details['description']}\n\n")
                
                self.insert_content("Features:\n")
                for feature in details['features']:
                    self.insert_content(f"• {feature}\n")
                
                self.insert_content(f"\nRecommended for: {details.get('recommended_for', 'Various projects')}\n\n")
                self.insert_content("-" * 50 + "\n\n")
        
        self.insert_header("Pricing Strategy Tips", 1)
        tips = [
            "Start with competitive pricing to get initial reviews",
            "Offer clear value differentiation between packages",
            "Consider offering a premium package for complex projects",
            "Adjust pricing based on demand and competition"
        ]
        
        for tip in tips:
            self.insert_content(f"💡 {tip}\n")
    
    def show_competitor_insights(self):
        """Display competitor analysis"""
        self.clear_content()
        self.content_title.config(text="🏆 Competitor Insights")
        self.configure_text_tags()
        
        if 'competitor_analysis' in self.results:
            insights = self.results['competitor_analysis']
            
            self.insert_header("Market Pricing Analysis", 1)
            if 'pricing_benchmarks' in insights:
                pricing = insights['pricing_benchmarks']
                self.insert_content(f"• Minimum Price: ${pricing.get('min_price', 'N/A')}\n")
                self.insert_content(f"• Maximum Price: ${pricing.get('max_price', 'N/A')}\n")
                self.insert_content(f"• Average Price: ${pricing.get('avg_price', 'N/A'):.2f}\n")
                self.insert_content(f"• Median Price: ${pricing.get('median_price', 'N/A')}\n\n")
            
            self.insert_header("Recommended Price Range", 1)
            if 'recommended_price_range' in insights:
                rec = insights['recommended_price_range']
                self.insert_content(f"• Low Tier: ${rec.get('low', 'N/A')}\n")
                self.insert_content(f"• Medium Tier: ${rec.get('medium', 'N/A')}\n")
                self.insert_content(f"• High Tier: ${rec.get('high', 'N/A')}\n\n")
            
            self.insert_header("Common Title Patterns", 1)
            if 'common_title_words' in insights:
                words = insights['common_title_words']
                if words:
                    self.insert_content("Top words used by successful competitors:\n")
                    for word, count in list(words.items())[:10]:
                        self.insert_content(f"• {word} (used {count} times)\n")
                else:
                    self.insert_content("No common title patterns identified.\n")
        
        else:
            self.insert_content("Competitor insights data not available.\n")
    
    def show_implementation(self):
        """Display implementation guide"""
        self.clear_content()
        self.content_title.config(text="📋 Step-by-Step Implementation")
        self.configure_text_tags()
        
        self.insert_header("Complete Gig Setup Guide", 1)
        
        steps = [
            ("1. Choose Your Gig Title", "Select the best title from the recommendations in the 'Gig Content' section"),
            ("2. Set Up Packages", "Create three packages (Basic, Standard, Premium) with the recommended pricing"),
            ("3. Write Your Description", "Copy and paste the optimized description from the 'Gig Content' section"),
            ("4. Add Tags", "Use all 5 recommended tags for maximum visibility"),
            ("5. Create Gig Images", "Design professional images that showcase your service"),
            ("6. Set Delivery Times", "Use the recommended delivery times for each package"),
            ("7. Add FAQ Section", "Include the provided frequently asked questions"),
            ("8. Set Requirements", "List what information you need from buyers"),
            ("9. Review and Publish", "Double-check everything and publish your gig"),
            ("10. Promote Your Gig", "Share your new gig on social media and relevant platforms")
        ]
        
        for step, description in steps:
            self.insert_content(f"{step}\n", 'highlight')
            self.insert_content(f"   {description}\n\n")
        
        self.insert_header("Pro Tips for Success", 1)
        tips = [
            "Respond to messages within 2 hours",
            "Offer exceptional service to get 5-star reviews",
            "Ask satisfied customers for testimonials",
            "Update your portfolio regularly",
            "Monitor your gig analytics and adjust as needed"
        ]
        
        for tip in tips:
            self.insert_content(f"⭐ {tip}\n")
    
    def show_quick_start(self):
        """Display quick start guide"""
        self.clear_content()
        self.content_title.config(text="🚀 Quick Start Guide")
        self.configure_text_tags()
        
        self.insert_header("Get Your Gig Live in 15 Minutes", 1)
        
        self.insert_content("Follow these 5 quick steps to launch your optimized Fiverr gig:\n\n")
        
        quick_steps = [
            "1. 📝 COPY your chosen title from 'Gig Content' section",
            "2. 💰 SET UP three packages with recommended pricing",
            "3. 📄 PASTE the optimized description template", 
            "4. 🏷️ ADD all 5 recommended tags",
            "5. 🎯 PUBLISH and start promoting!"
        ]
        
        for step in quick_steps:
            self.insert_content(f"{step}\n", 'success')
        
        self.insert_content("\n" + "="*50 + "\n\n")
        
        self.insert_header("Immediate Actions After Launch", 2)
        actions = [
            "Enable notifications for new messages",
            "Prepare quick response templates",
            "Share your gig on social media",
            "Tell your network about your new service",
            "Check your gig analytics daily"
        ]
        
        for action in actions:
            self.insert_content(f"✅ {action}\n")
    
    def show_summary(self):
        """Display summary report"""
        self.clear_content()
        self.content_title.config(text="📊 Executive Summary")
        self.configure_text_tags()
        
        if 'summary' in self.results:
            summary = self.results['summary']
            
            if 'analysis_summary' in summary:
                analysis = summary['analysis_summary']
                self.insert_header("Analysis Summary", 1)
                self.insert_content(f"• Service Analyzed: {analysis.get('service_analyzed', 'N/A')}\n")
                self.insert_content(f"• Total Keywords Researched: {analysis.get('total_keywords_researched', 'N/A')}\n")
                self.insert_content(f"• Top Keyword: {analysis.get('top_keyword', 'N/A')}\n")
                self.insert_content(f"• Top Keyword Score: {analysis.get('top_keyword_score', 'N/A')}/10\n")
                self.insert_content(f"• Competition Level: {analysis.get('competition_level', 'N/A')}\n")
                self.insert_content(f"• Market Opportunity Score: {analysis.get('market_opportunity_score', 'N/A')}/10\n\n")
            
            if 'key_recommendations' in summary:
                self.insert_header("Key Recommendations", 1)
                for rec in summary['key_recommendations']:
                    self.insert_content(f"• {rec}\n")
                self.insert_content("\n")
            
            if 'success_metrics' in summary:
                self.insert_header("Expected Performance", 1)
                metrics = summary['success_metrics']
                for key, value in metrics.items():
                    self.insert_content(f"• {key.replace('_', ' ').title()}: {value}\n")
        
        else:
            self.insert_content("Summary report not available.\n")

def main():
    """Main function to run the results viewer"""
    root = tk.Tk()
    app = ResultsViewer(root)
    
    # Configure text tags after the text widget is created
    app.configure_text_tags()
    
    root.mainloop()

if __name__ == "__main__":
    main()
