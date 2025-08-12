import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

class CoffeeShopAnalysis:
    """Complete coffee shop sales analysis in a single class."""
    
    def __init__(self, excel_file_path):
        """Initialize with the path to the Excel file."""
        self.excel_file = Path(excel_file_path)
        self.output_dir = self.excel_file.parent
        self.cleaned_data = None
        self.analysis_results = {}
        
        print(" Coffee Shop Sales Analysis")
        print("=" * 50)
        print(f" Analysis started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
    
    def load_and_clean_data(self):
        """Load and clean the data from Excel file."""
        print(" Loading and cleaning data...")
        
        try:
            # Load data
            print(f" Loading data from: {self.excel_file.name}")
            raw_data = pd.read_excel(self.excel_file, sheet_name='Transactions')
            print(f" Raw data loaded: {raw_data.shape[0]:,} rows × {raw_data.shape[1]} columns")
            
            # Clean data
            cleaned_data = self._clean_data(raw_data)
            
            # Save cleaned dataset
            cleaned_file_path = self.output_dir / 'coffee_shop_sales_cleaned.csv'
            cleaned_data.to_csv(cleaned_file_path, index=False)
            print(f" Cleaned dataset saved: {cleaned_file_path.name}")
            
            self.cleaned_data = cleaned_data
            return cleaned_data
            
        except Exception as e:
            print(f" Error in data loading/cleaning: {str(e)}")
            raise
    
    def _clean_data(self, df):
        """Clean the raw data."""
        print(" Cleaning data...")
        original_rows = len(df)
        
        # Make a copy
        data = df.copy()
        
        # Clean transaction dates and times
        data['transaction_date'] = pd.to_datetime(data['transaction_date'], errors='coerce')
        data['transaction_time'] = pd.to_datetime(data['transaction_time'], format='%H:%M:%S', errors='coerce').dt.time
        
        # Remove rows with invalid dates
        data = data.dropna(subset=['transaction_date'])
        
        # Clean quantities - ensure positive values
        data['transaction_qty'] = pd.to_numeric(data['transaction_qty'], errors='coerce')
        data = data[data['transaction_qty'] > 0]
        
        # Clean unit prices - remove extreme outliers
        data['unit_price'] = pd.to_numeric(data['unit_price'], errors='coerce')
        # Remove prices outside reasonable range ($0.01 - $15.00)
        data = data[(data['unit_price'] >= 0.01) & (data['unit_price'] <= 15.0)]
        
        # Clean store and product info
        data = data.dropna(subset=['store_location', 'product_detail'])
        
        # Add calculated fields
        data['revenue'] = data['transaction_qty'] * data['unit_price']
        data['datetime'] = pd.to_datetime(data['transaction_date'].dt.strftime('%Y-%m-%d') + ' ' + 
                                         data['transaction_time'].astype(str))
        
        # Add time-based features
        data['year'] = data['transaction_date'].dt.year
        data['month'] = data['transaction_date'].dt.month
        data['day_of_week'] = data['transaction_date'].dt.day_name()
        data['hour'] = data['datetime'].dt.hour
        data['is_weekend'] = data['transaction_date'].dt.weekday >= 5
        
        # Remove duplicates
        data = data.drop_duplicates()
        
        final_rows = len(data)
        retention_rate = (final_rows / original_rows) * 100
        
        print(f" Data cleaning completed")
        print(f" Original rows: {original_rows:,}")
        print(f" Final rows: {final_rows:,}")
        print(f" Rows removed: {original_rows - final_rows:,}")
        print(f" Retention rate: {retention_rate:.1f}%")
        
        return data

    def analyze_profitability(self):
        """Perform comprehensive profitability analysis."""
        print("\n Analyzing profitability...")
        
        if self.cleaned_data is None:
            raise ValueError("No cleaned data available. Run load_and_clean_data() first.")
        
        data = self.cleaned_data.copy()
        
        # Estimate costs based on product categories and industry standards
        data = self._estimate_costs(data)
        
        # Calculate profit metrics
        data['estimated_profit'] = data['revenue'] - data['estimated_cost']
        data['profit_margin'] = data['estimated_profit'] / data['revenue']
        
        # Store enhanced data
        self.cleaned_data = data
        
        # Perform various analyses
        results = {
            'financial_summary': self._analyze_financial_summary(data),
            'product_analysis': self._analyze_products(data),
            'category_analysis': self._analyze_categories(data),
            'store_analysis': self._analyze_stores(data),
            'temporal_analysis': self._analyze_temporal_patterns(data),
            'insights_and_recommendations': self._generate_insights(data)
        }
        
        self.analysis_results = results
        print(" Profitability analysis completed")
        return results
    
    def _estimate_costs(self, data):
        """Estimate costs based on product categories."""
        # Define cost estimation rules based on product categories and industry standards
        cost_rules = {
            'Coffee': 0.35,      # 35% of revenue (beans, labor, overhead)
            'Tea': 0.30,         # 30% of revenue (tea leaves, labor)
            'Drinking Chocolate': 0.40,  # 40% of revenue (chocolate, milk)
            'Frappé': 0.45,      # 45% of revenue (ingredients, complexity)
            'Smoothies': 0.50,   # 50% of revenue (fruit, milk, labor)
            'Bakery': 0.60,      # 60% of revenue (ingredients, baking labor)
            'Branded': 0.70,     # 70% of revenue (wholesale cost)
            'Flavours': 0.25     # 25% of revenue (syrup cost)
        }
        
        # Apply cost estimation
        data['estimated_cost_ratio'] = data['product_category'].map(cost_rules).fillna(0.5)  # Default 50%
        data['estimated_cost'] = data['revenue'] * data['estimated_cost_ratio']
        
        return data
    
    def _analyze_financial_summary(self, data):
        """Analyze overall financial performance."""
        total_revenue = data['revenue'].sum()
        total_cost = data['estimated_cost'].sum()
        total_profit = data['estimated_profit'].sum()
        
        return {
            'total_revenue': total_revenue,
            'total_estimated_cost': total_cost,
            'total_estimated_profit': total_profit,
            'overall_profit_margin': total_profit / total_revenue if total_revenue > 0 else 0,
            'total_transactions': len(data),
            'avg_transaction_value': data['revenue'].mean(),
            'avg_transaction_profit': data['estimated_profit'].mean(),
            'analysis_period_days': (data['transaction_date'].max() - data['transaction_date'].min()).days + 1
        }
    
    def _analyze_products(self, data):
        """Analyze product-level performance."""
        product_metrics = data.groupby('product_detail').agg({
            'revenue': 'sum',
            'estimated_cost': 'sum',
            'estimated_profit': 'sum',
            'transaction_qty': 'sum',
            'transaction_id': 'count'
        }).round(2)
        
        product_metrics['profit_margin'] = (product_metrics['estimated_profit'] / 
                                          product_metrics['revenue']).round(3)
        product_metrics['avg_profit_per_unit'] = (product_metrics['estimated_profit'] / 
                                                product_metrics['transaction_qty']).round(2)
        
        # Sort by total profit
        product_metrics = product_metrics.sort_values('estimated_profit', ascending=False)
        
        return {
            'product_metrics': product_metrics,
            'top_performers': product_metrics.head(10),
            'bottom_performers': product_metrics.tail(5),
            'total_products': len(product_metrics),
            'profitable_products': len(product_metrics[product_metrics['estimated_profit'] > 0])
        }
    
    def _analyze_categories(self, data):
       
        category_metrics = data.groupby('product_category').agg({
            'revenue': 'sum',
            'estimated_cost': 'sum',
            'estimated_profit': 'sum',
            'transaction_qty': 'sum',
            'transaction_id': 'count',
            'product_detail': 'nunique'
        }).round(2)
        
        category_metrics['profit_margin'] = (category_metrics['estimated_profit'] / 
                                           category_metrics['revenue']).round(3)
        category_metrics['revenue_share'] = (category_metrics['revenue'] / 
                                           category_metrics['revenue'].sum()).round(3)
        
        # Sort by revenue
        category_metrics = category_metrics.sort_values('revenue', ascending=False)
        
        return {
            'category_metrics': category_metrics,
            'total_categories': len(category_metrics)
        }
    
    def _analyze_stores(self, data):
       
        store_metrics = data.groupby('store_location').agg({
            'revenue': 'sum',
            'estimated_cost': 'sum',
            'estimated_profit': 'sum',
            'transaction_id': 'count',
            'product_detail': 'nunique'
        }).round(2)
        
        store_metrics['profit_margin'] = (store_metrics['estimated_profit'] / 
                                        store_metrics['revenue']).round(3)
        store_metrics['avg_transaction_value'] = (store_metrics['revenue'] / 
                                                store_metrics['transaction_id']).round(2)
        
        # Sort by revenue
        store_metrics = store_metrics.sort_values('revenue', ascending=False)
        
        return {
            'store_metrics': store_metrics,
            'total_stores': len(store_metrics)
        }
    
    def _analyze_temporal_patterns(self, data):
        """Analyze temporal patterns in performance."""
        # Monthly trends
        monthly_data = data.groupby(['year', 'month']).agg({
            'revenue': 'sum',
            'estimated_profit': 'sum',
            'transaction_id': 'count'
        }).round(2)
        monthly_data['profit_margin'] = (monthly_data['estimated_profit'] / 
                                       monthly_data['revenue']).round(3)
        monthly_data = monthly_data.reset_index()
        
        # Daily patterns
        daily_data = data.groupby('day_of_week').agg({
            'revenue': 'mean',
            'estimated_profit': 'mean',
            'transaction_id': 'count'
        }).round(2)
        
        # Hourly patterns
        hourly_data = data.groupby('hour').agg({
            'revenue': 'mean',
            'estimated_profit': 'mean',
            'transaction_id': 'count'
        }).round(2)
        
        return {
            'monthly_trends': monthly_data,
            'daily_patterns': daily_data,
            'hourly_patterns': hourly_data,
            'peak_month': monthly_data.loc[monthly_data['revenue'].idxmax(), 'month'],
            'peak_day': daily_data['revenue'].idxmax(),
            'peak_hour': hourly_data['revenue'].idxmax()
        }
    
    def _generate_insights(self, data):
       
        insights = []
        recommendations = []
        
        # Financial insights
        financial = self.analysis_results.get('financial_summary', self._analyze_financial_summary(data))
        
        if financial['overall_profit_margin'] > 0.5:
            insights.append("Strong profitability with >50% profit margin")
        elif financial['overall_profit_margin'] > 0.3:
            insights.append("Healthy profitability with moderate margins")
        else:
            insights.append("Profitability needs improvement")
            recommendations.append("Review pricing strategy and cost optimization")
        
        # Product insights
        product_analysis = self.analysis_results.get('product_analysis', self._analyze_products(data))
        top_products = product_analysis['top_performers'].head(3)
        
        insights.append(f"Top 3 profit generators: {', '.join(top_products.index[:3])}")
        
        # Low-performing products
        low_performers = product_analysis['product_metrics'][
            product_analysis['product_metrics']['profit_margin'] < 0.2
        ]
        if len(low_performers) > 0:
            recommendations.append(f"Review {len(low_performers)} products with <20% profit margin")
        
        # Category insights
        category_analysis = self.analysis_results.get('category_analysis', self._analyze_categories(data))
        top_category = category_analysis['category_metrics'].index[0]
        insights.append(f"Most profitable category: {top_category}")
        
        # Store insights
        store_analysis = self.analysis_results.get('store_analysis', self._analyze_stores(data))
        if len(store_analysis['store_metrics']) > 1:
            best_store = store_analysis['store_metrics'].index[0]
            insights.append(f"Best performing store: {best_store}")
        
        # Temporal insights
        temporal_analysis = self.analysis_results.get('temporal_analysis', self._analyze_temporal_patterns(data))
        insights.append(f"Peak performance: Month {temporal_analysis['peak_month']}, "
                       f"{temporal_analysis['peak_day']}s, {temporal_analysis['peak_hour']}:00")
        
        return {
            'key_insights': insights,
            'recommendations': recommendations
        }
    
    def report(self):
        
        print("\n making the report...")
        
        if not self.analysis_results:
            raise ValueError("No analysis results available. Run analyze_profitability() first.")
        
        report_path = self.output_dir / 'coffee_shop_analysis_report.txt'
        
        with open(report_path, 'w', encoding='utf-8') as f:
            # Header
            f.write("COFFEE SHOP SALES ANALYSIS\n")
            f.write("COMPREHENSIVE REPORT\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Analysis Period: {self.cleaned_data['transaction_date'].min().strftime('%Y-%m-%d')} to ")
            f.write(f"{self.cleaned_data['transaction_date'].max().strftime('%Y-%m-%d')}\n\n")
            
            # Executive Summary
            self.executive_summary(f)
            
            # Financial Performance
            self.financial_performance(f)
            
            # Product Analysis
            self.product_analysis(f)
            
            # Category Analysis
            self.category_analysis(f)
            
            # Store Analysis
            self.store_analysis(f)
            
            # Temporal Analysis
            self.temporal_analysis(f)
            
            # Insights and Recommendations
            self.insights_and_recommendations(f)
            
            # Data Quality Summary
            self.data_quality_summary(f)
        
        print(f" report saved: {report_path.name}")
        return str(report_path)
    
    def executive_summary(self, f):
     
        financial = self.analysis_results['financial_summary']
        
        f.write("EXECUTIVE SUMMARY\n")
        f.write("-" * 20 + "\n")
        f.write(f"Total Revenue: ${financial['total_revenue']:,.2f}\n")
        f.write(f"Total Estimated Profit: ${financial['total_estimated_profit']:,.2f}\n")
        f.write(f"Overall Profit Margin: {financial['overall_profit_margin']:.1%}\n")
        f.write(f"Total Transactions: {financial['total_transactions']:,}\n")
        f.write(f"Analysis Period: {financial['analysis_period_days']} days\n")
        f.write(f"Average Daily Revenue: ${financial['total_revenue']/financial['analysis_period_days']:,.2f}\n\n")
    
    def financial_performance(self, f):
     
        financial = self.analysis_results['financial_summary']
        
        f.write("FINANCIAL PERFORMANCE\n")
        f.write("-" * 25 + "\n")
        f.write(f"Revenue Metrics:\n")
        f.write(f"  • Total Revenue: ${financial['total_revenue']:,.2f}\n")
        f.write(f"  • Average Transaction Value: ${financial['avg_transaction_value']:.2f}\n")
        f.write(f"  • Total Transactions: {financial['total_transactions']:,}\n\n")
        
        f.write(f"Profitability Metrics:\n")
        f.write(f"  • Total Estimated Profit: ${financial['total_estimated_profit']:,.2f}\n")
        f.write(f"  • Overall Profit Margin: {financial['overall_profit_margin']:.1%}\n")
        f.write(f"  • Average Transaction Profit: ${financial['avg_transaction_profit']:.2f}\n\n")
    
    def product_analysis(self, f):
        
        product_analysis = self.analysis_results['product_analysis']
        
        f.write("PRODUCT ANALYSIS\n")
        f.write("-" * 20 + "\n")
        f.write(f"Total Products: {product_analysis['total_products']}\n")
        f.write(f"Profitable Products: {product_analysis['profitable_products']}\n\n")
        
        f.write("Top 10 Most Profitable Products:\n")
        for i, (product, data) in enumerate(product_analysis['top_performers'].iterrows(), 1):
            f.write(f"{i:2d}. {product[:60]:<60} ${data['estimated_profit']:>8,.0f} ({data['profit_margin']:>5.1%})\n")
        f.write("\n")
        
        if len(product_analysis['bottom_performers']) > 0:
            f.write("Lowest Performing Products:\n")
            for i, (product, data) in enumerate(product_analysis['bottom_performers'].iterrows(), 1):
                f.write(f"{i:2d}. {product[:60]:<60} ${data['estimated_profit']:>8,.0f} ({data['profit_margin']:>5.1%})\n")
            f.write("\n")
    
    def category_analysis(self, f):
    
        category_analysis = self.analysis_results['category_analysis']
        
        f.write("CATEGORY ANALYSIS\n")
        f.write("-" * 20 + "\n")
        f.write("Performance by Category:\n")
        
        for category, data in category_analysis['category_metrics'].iterrows():
            f.write(f"• {category}:\n")
            f.write(f"  Revenue: ${data['revenue']:,.2f} ({data['revenue_share']:.1%} of total)\n")
            f.write(f"  Profit: ${data['estimated_profit']:,.2f} (Margin: {data['profit_margin']:.1%})\n")
            f.write(f"  Products: {data['product_detail']} | Transactions: {data['transaction_id']:,}\n\n")
    
    def store_analysis(self, f):
        
        store_analysis = self.analysis_results['store_analysis']
        
        f.write("STORE ANALYSIS\n")
        f.write("-" * 15 + "\n")
        f.write("Performance by Store:\n")
        
        for store, data in store_analysis['store_metrics'].iterrows():
            f.write(f"• {store}:\n")
            f.write(f"  Revenue: ${data['revenue']:,.2f}\n")
            f.write(f"  Profit: ${data['estimated_profit']:,.2f} (Margin: {data['profit_margin']:.1%})\n")
            f.write(f"  Transactions: {data['transaction_id']:,} | Avg Value: ${data['avg_transaction_value']:.2f}\n")
            f.write(f"  Products Sold: {data['product_detail']} unique items\n\n")
    
    def temporal_analysis(self, f):
        
        temporal_analysis = self.analysis_results['temporal_analysis']
        
        f.write("TEMPORAL ANALYSIS\n")
        f.write("-" * 18 + "\n")
        
        f.write("Peak Performance:\n")
        f.write(f"  • Best Month: Month {temporal_analysis['peak_month']}\n")
        f.write(f"  • Best Day: {temporal_analysis['peak_day']}\n")
        f.write(f"  • Peak Hour: {temporal_analysis['peak_hour']}:00\n\n")
        
        f.write("Monthly Performance:\n")
        monthly_trends = temporal_analysis['monthly_trends']
        for _, month in monthly_trends.iterrows():
            month_name = datetime(int(month['year']), int(month['month']), 1).strftime('%B %Y')
            f.write(f"  {month_name}: ${month['revenue']:>8,.0f} revenue, {month['profit_margin']:>5.1%} margin\n")
        f.write("\n")
        
        f.write("Daily Patterns (Average Performance):\n")
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        daily_patterns = temporal_analysis['daily_patterns']
        for day in day_order:
            if day in daily_patterns.index:
                data = daily_patterns.loc[day]
                f.write(f"  {day:<10}: ${data['revenue']:>6,.0f} avg revenue, {data['transaction_id']:>4,} transactions\n")
        f.write("\n")
    
    def insights_and_recommendations(self, f):
        
        insights = self.analysis_results['insights_and_recommendations']
        
        f.write("KEY INSIGHTS\n")
        f.write("-" * 15 + "\n")
        for i, insight in enumerate(insights['key_insights'], 1):
            f.write(f"{i}. {insight}\n")
        f.write("\n")
        
        if insights['recommendations']:
            f.write("RECOMMENDATIONS\n")
            f.write("-" * 18 + "\n")
            for i, recommendation in enumerate(insights['recommendations'], 1):
                f.write(f"{i}. {recommendation}\n")
            f.write("\n")
    
    def data_quality_summary(self, f):
        
        f.write("DATA QUALITY SUMMARY\n")
        f.write("-" * 23 + "\n")
        f.write(f"Dataset Shape: {self.cleaned_data.shape[0]:,} rows × {self.cleaned_data.shape[1]} columns\n")
        f.write(f"Date Range: {self.cleaned_data['transaction_date'].min().strftime('%Y-%m-%d')} to ")
        f.write(f"{self.cleaned_data['transaction_date'].max().strftime('%Y-%m-%d')}\n")
        f.write(f"Unique Products: {self.cleaned_data['product_detail'].nunique()}\n")
        f.write(f"Unique Stores: {self.cleaned_data['store_location'].nunique()}\n")
        f.write(f"Data Completeness: Good (post-cleaning)\n")
        f.write(f"Cost Estimation: Based on industry-standard ratios by product category\n")
    
    def run_complete_analysis(self):
        """Run the complete analysis pipeline."""
        try:
            # Step 1: Load and clean data
            self.load_and_clean_data()
            
            # Step 2: Analyze profitability
            self.analyze_profitability()
            
            # Step 3: Generate comprehensive report
            report_path = self.report()
            
            # Final summary
            print(f"\n ANALYSIS COMPLETED SUCCESSFULLY!")
            print("=" * 50)
            print(" Outputs :")
            print(f"  • Cleaned Dataset: coffee_shop_sales_cleaned.csv")
            print(f"  • Comprehensive Report: coffee_shop_analysis_report.txt")
            print()
            print(" Report includes:")
            print("  • Executive Summary")
            print("  • Financial Performance Analysis")
            print("  • Product & Category Performance")
            print("  • Store Performance Comparison")
            print("  • Temporal Analysis & Trends")
            print("  • Key Insights & Recommendations")
            print()
            
            return True
            
        except Exception as e:
            print(f"\n ANALYSIS FAILED!")
            print(f"Error: {str(e)}")
            return False


def main():
    
    # Path to your Excel file
    excel_file_path = r"C:\Users\my pc\Downloads\Coffee Shop Sales Analysis\Coffee Shop Sales (1).xlsx"
    
    try:
        # Create analyzer instance
        analyzer = CoffeeShopAnalysis(excel_file_path)
        
        # Run complete analysis
        success = analyzer.run_complete_analysis()
        
        if success:
            print(" All outputs saved successfully!")
        else:
            print(" Analysis failed!")
            
    except Exception as e:
        print(f" Error: {str(e)}")


if __name__ == "__main__":
    main()
