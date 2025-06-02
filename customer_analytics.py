#!/usr/bin/env python3
"""
Customer Behavior Analytics Platform
Advanced analytics system combining Python and R for comprehensive customer behavior analysis,
segmentation, and predictive modeling.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sqlite3
from datetime import datetime, timedelta
import json
import warnings
warnings.filterwarnings('ignore')

class CustomerBehaviorAnalytics:
    def __init__(self):
        """Initialize the customer behavior analytics platform."""
        self.customer_data = None
        self.transaction_data = None
        self.segments = None
        self.models = {}
        
    def generate_sample_data(self):
        """Generate comprehensive sample customer and transaction data."""
        np.random.seed(42)
        
        # Generate customer data
        n_customers = 5000
        customer_data = []
        
        for i in range(n_customers):
            # Customer demographics
            age = np.random.normal(40, 15)
            age = max(18, min(80, age))  # Constrain age
            
            # Income based on age (simplified model)
            base_income = 30000 + (age - 25) * 1000 + np.random.normal(0, 15000)
            income = max(20000, base_income)
            
            customer_data.append({
                'customer_id': f'CUST_{i:05d}',
                'age': int(age),
                'gender': np.random.choice(['M', 'F'], p=[0.48, 0.52]),
                'income': round(income, 2),
                'education': np.random.choice(['High School', 'Bachelor', 'Master', 'PhD'], 
                                            p=[0.3, 0.4, 0.25, 0.05]),
                'location': np.random.choice(['Urban', 'Suburban', 'Rural'], p=[0.5, 0.35, 0.15]),
                'registration_date': (datetime.now() - timedelta(days=np.random.randint(1, 1095))).strftime('%Y-%m-%d'),
                'preferred_channel': np.random.choice(['Online', 'Mobile', 'Store'], p=[0.4, 0.35, 0.25])
            })
        
        self.customer_data = pd.DataFrame(customer_data)
        
        # Generate transaction data
        transaction_data = []
        transaction_id = 1
        
        for _, customer in self.customer_data.iterrows():
            # Number of transactions based on customer profile
            base_transactions = 5
            if customer['income'] > 60000:
                base_transactions += 10
            if customer['age'] < 35:
                base_transactions += 5
            if customer['preferred_channel'] == 'Mobile':
                base_transactions += 3
                
            n_transactions = np.random.poisson(base_transactions)
            
            for _ in range(n_transactions):
                # Transaction amount based on income
                base_amount = customer['income'] * 0.001
                amount = np.random.exponential(base_amount)
                amount = max(10, min(5000, amount))  # Constrain amount
                
                # Transaction date
                days_ago = np.random.randint(1, 365)
                transaction_date = datetime.now() - timedelta(days=days_ago)
                
                # Product category preferences
                categories = ['Electronics', 'Clothing', 'Books', 'Home', 'Sports', 'Beauty', 'Food']
                if customer['age'] < 30:
                    category_probs = [0.25, 0.20, 0.10, 0.15, 0.15, 0.10, 0.05]
                elif customer['age'] < 50:
                    category_probs = [0.20, 0.15, 0.15, 0.25, 0.10, 0.10, 0.05]
                else:
                    category_probs = [0.15, 0.10, 0.20, 0.30, 0.05, 0.15, 0.05]
                
                transaction_data.append({
                    'transaction_id': transaction_id,
                    'customer_id': customer['customer_id'],
                    'amount': round(amount, 2),
                    'category': np.random.choice(categories, p=category_probs),
                    'channel': customer['preferred_channel'],
                    'date': transaction_date.strftime('%Y-%m-%d'),
                    'time': transaction_date.strftime('%H:%M:%S'),
                    'payment_method': np.random.choice(['Credit Card', 'Debit Card', 'PayPal', 'Cash'], 
                                                     p=[0.4, 0.3, 0.2, 0.1])
                })
                transaction_id += 1
        
        self.transaction_data = pd.DataFrame(transaction_data)
        
    def calculate_customer_metrics(self):
        """Calculate comprehensive customer behavior metrics."""
        # Merge customer and transaction data
        merged_data = self.transaction_data.merge(self.customer_data, on='customer_id')
        
        # Calculate RFM metrics (Recency, Frequency, Monetary)
        current_date = datetime.now()
        
        customer_metrics = merged_data.groupby('customer_id').agg({
            'date': lambda x: (current_date - pd.to_datetime(x.max())).days,  # Recency
            'transaction_id': 'count',  # Frequency
            'amount': ['sum', 'mean', 'std']  # Monetary
        }).round(2)
        
        customer_metrics.columns = ['recency', 'frequency', 'total_spent', 'avg_order_value', 'spending_variance']
        customer_metrics['spending_variance'] = customer_metrics['spending_variance'].fillna(0)
        
        # Add customer lifetime value
        customer_metrics['customer_lifetime_value'] = (
            customer_metrics['frequency'] * customer_metrics['avg_order_value'] * 2.5
        )
        
        # Add customer demographics
        customer_metrics = customer_metrics.merge(
            self.customer_data.set_index('customer_id')[['age', 'gender', 'income', 'education', 'location']],
            left_index=True, right_index=True
        )
        
        # Calculate additional behavioral metrics
        category_diversity = merged_data.groupby('customer_id')['category'].nunique()
        customer_metrics['category_diversity'] = category_diversity
        
        # Channel preference strength
        channel_consistency = merged_data.groupby('customer_id')['channel'].apply(
            lambda x: x.value_counts().iloc[0] / len(x)
        )
        customer_metrics['channel_consistency'] = channel_consistency
        
        return customer_metrics
    
    def perform_customer_segmentation(self, customer_metrics):
        """Perform advanced customer segmentation using multiple algorithms."""
        # Prepare data for clustering
        features_for_clustering = [
            'recency', 'frequency', 'total_spent', 'avg_order_value',
            'customer_lifetime_value', 'age', 'income', 'category_diversity'
        ]
        
        X = customer_metrics[features_for_clustering].copy()
        
        # Handle missing values
        X = X.fillna(X.median())
        
        # Standardize features
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        # K-Means clustering
        kmeans = KMeans(n_clusters=5, random_state=42, n_init=10)
        customer_metrics['segment_kmeans'] = kmeans.fit_predict(X_scaled)
        
        # RFM-based segmentation
        customer_metrics['R_score'] = pd.qcut(customer_metrics['recency'], 5, labels=[5,4,3,2,1])
        customer_metrics['F_score'] = pd.qcut(customer_metrics['frequency'].rank(method='first'), 5, labels=[1,2,3,4,5])
        customer_metrics['M_score'] = pd.qcut(customer_metrics['total_spent'], 5, labels=[1,2,3,4,5])
        
        customer_metrics['RFM_score'] = (
            customer_metrics['R_score'].astype(str) + 
            customer_metrics['F_score'].astype(str) + 
            customer_metrics['M_score'].astype(str)
        )
        
        # Define segment names based on RFM
        def categorize_rfm(row):
            if row['RFM_score'] in ['555', '554', '544', '545', '454', '455', '445']:
                return 'Champions'
            elif row['RFM_score'] in ['543', '444', '435', '355', '354', '345', '344', '335']:
                return 'Loyal Customers'
            elif row['RFM_score'] in ['512', '511', '422', '421', '412', '411', '311']:
                return 'Potential Loyalists'
            elif row['RFM_score'] in ['533', '532', '531', '523', '522', '521', '515', '514', '513', '425', '424', '413', '414', '415', '315', '314', '313']:
                return 'New Customers'
            elif row['RFM_score'] in ['155', '154', '144', '214', '215', '115', '114']:
                return 'At Risk'
            elif row['RFM_score'] in ['155', '154', '144', '214', '215', '115', '114']:
                return 'Cannot Lose Them'
            else:
                return 'Others'
        
        customer_metrics['segment_rfm'] = customer_metrics.apply(categorize_rfm, axis=1)
        
        self.segments = customer_metrics
        return customer_metrics
    
    def analyze_segment_characteristics(self):
        """Analyze characteristics of different customer segments."""
        if self.segments is None:
            raise ValueError("Customer segmentation must be performed first")
        
        # Analyze K-Means segments
        kmeans_analysis = self.segments.groupby('segment_kmeans').agg({
            'recency': 'mean',
            'frequency': 'mean',
            'total_spent': 'mean',
            'avg_order_value': 'mean',
            'customer_lifetime_value': 'mean',
            'age': 'mean',
            'income': 'mean',
            'category_diversity': 'mean'
        }).round(2)
        
        # Analyze RFM segments
        rfm_analysis = self.segments.groupby('segment_rfm').agg({
            'recency': 'mean',
            'frequency': 'mean',
            'total_spent': 'mean',
            'customer_lifetime_value': 'mean',
            'customer_id': 'count'
        }).round(2)
        rfm_analysis.columns = ['avg_recency', 'avg_frequency', 'avg_total_spent', 'avg_clv', 'customer_count']
        
        return kmeans_analysis, rfm_analysis
    
    def create_visualizations(self):
        """Create comprehensive visualizations for customer behavior analysis."""
        if self.segments is None:
            raise ValueError("Customer segmentation must be performed first")
        
        # Create subplots
        fig = make_subplots(
            rows=3, cols=2,
            subplot_titles=(
                'Customer Segments (K-Means)', 'RFM Segments Distribution',
                'Customer Lifetime Value by Segment', 'Age vs Income by Segment',
                'Purchase Frequency Distribution', 'Category Preferences by Segment'
            ),
            specs=[[{"type": "scatter3d"}, {"type": "pie"}],
                   [{"type": "box"}, {"type": "scatter"}],
                   [{"type": "histogram"}, {"type": "bar"}]]
        )
        
        # 3D scatter plot for K-Means segments
        fig.add_trace(
            go.Scatter3d(
                x=self.segments['recency'],
                y=self.segments['frequency'],
                z=self.segments['total_spent'],
                mode='markers',
                marker=dict(
                    size=5,
                    color=self.segments['segment_kmeans'],
                    colorscale='Viridis',
                    showscale=True
                ),
                text=self.segments.index,
                name='K-Means Segments'
            ),
            row=1, col=1
        )
        
        # RFM segments pie chart
        rfm_counts = self.segments['segment_rfm'].value_counts()
        fig.add_trace(
            go.Pie(
                labels=rfm_counts.index,
                values=rfm_counts.values,
                name="RFM Segments"
            ),
            row=1, col=2
        )
        
        # CLV by segment box plot
        for segment in self.segments['segment_rfm'].unique():
            segment_data = self.segments[self.segments['segment_rfm'] == segment]
            fig.add_trace(
                go.Box(
                    y=segment_data['customer_lifetime_value'],
                    name=segment,
                    showlegend=False
                ),
                row=2, col=1
            )
        
        # Age vs Income scatter
        fig.add_trace(
            go.Scatter(
                x=self.segments['age'],
                y=self.segments['income'],
                mode='markers',
                marker=dict(
                    size=8,
                    color=self.segments['segment_kmeans'],
                    colorscale='Plasma',
                    opacity=0.6
                ),
                name='Age vs Income',
                showlegend=False
            ),
            row=2, col=2
        )
        
        # Purchase frequency histogram
        fig.add_trace(
            go.Histogram(
                x=self.segments['frequency'],
                nbinsx=30,
                name='Purchase Frequency',
                showlegend=False
            ),
            row=3, col=1
        )
        
        # Category preferences by segment
        category_by_segment = self.transaction_data.merge(
            self.segments[['segment_rfm']], left_on='customer_id', right_index=True
        ).groupby(['segment_rfm', 'category']).size().unstack(fill_value=0)
        
        for category in category_by_segment.columns:
            fig.add_trace(
                go.Bar(
                    x=category_by_segment.index,
                    y=category_by_segment[category],
                    name=category,
                    showlegend=False
                ),
                row=3, col=2
            )
        
        fig.update_layout(height=1200, title_text="Customer Behavior Analytics Dashboard")
        
        # Save visualization
        fig.write_html('customer_behavior_dashboard.html')
        
        return fig
    
    def predict_customer_churn(self):
        """Build a predictive model for customer churn."""
        if self.segments is None:
            raise ValueError("Customer segmentation must be performed first")
        
        # Define churn (customers who haven't purchased in last 90 days)
        self.segments['is_churned'] = (self.segments['recency'] > 90).astype(int)
        
        # Prepare features for modeling
        feature_columns = [
            'frequency', 'total_spent', 'avg_order_value', 'customer_lifetime_value',
            'age', 'income', 'category_diversity', 'channel_consistency'
        ]
        
        X = self.segments[feature_columns].fillna(self.segments[feature_columns].median())
        y = self.segments['is_churned']
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Train Random Forest model
        rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
        rf_model.fit(X_train, y_train)
        
        # Make predictions
        y_pred = rf_model.predict(X_test)
        
        # Store model and results
        self.models['churn_prediction'] = {
            'model': rf_model,
            'feature_importance': dict(zip(feature_columns, rf_model.feature_importances_)),
            'classification_report': classification_report(y_test, y_pred),
            'confusion_matrix': confusion_matrix(y_test, y_pred)
        }
        
        return self.models['churn_prediction']
    
    def generate_insights_report(self):
        """Generate comprehensive insights report."""
        if self.segments is None:
            raise ValueError("Customer segmentation must be performed first")
        
        # Calculate key insights
        total_customers = len(self.segments)
        total_revenue = self.segments['total_spent'].sum()
        avg_clv = self.segments['customer_lifetime_value'].mean()
        
        # Segment insights
        segment_summary = self.segments.groupby('segment_rfm').agg({
            'customer_id': 'count',
            'total_spent': 'sum',
            'customer_lifetime_value': 'mean'
        })
        segment_summary.columns = ['customer_count', 'total_revenue', 'avg_clv']
        segment_summary['revenue_percentage'] = (segment_summary['total_revenue'] / total_revenue * 100).round(2)
        
        # Top insights
        insights = {
            'total_customers': total_customers,
            'total_revenue': total_revenue,
            'average_clv': avg_clv,
            'most_valuable_segment': segment_summary.loc[segment_summary['avg_clv'].idxmax()],
            'largest_segment': segment_summary.loc[segment_summary['customer_count'].idxmax()],
            'churn_rate': (self.segments['is_churned'].sum() / total_customers * 100).round(2),
            'segment_summary': segment_summary
        }
        
        return insights
    
    def run_complete_analysis(self):
        """Run the complete customer behavior analysis pipeline."""
        print("Starting Customer Behavior Analytics...")
        
        # Generate data
        print("1. Generating sample data...")
        self.generate_sample_data()
        
        # Calculate metrics
        print("2. Calculating customer metrics...")
        customer_metrics = self.calculate_customer_metrics()
        
        # Perform segmentation
        print("3. Performing customer segmentation...")
        self.perform_customer_segmentation(customer_metrics)
        
        # Analyze segments
        print("4. Analyzing segment characteristics...")
        kmeans_analysis, rfm_analysis = self.analyze_segment_characteristics()
        
        # Create visualizations
        print("5. Creating visualizations...")
        dashboard = self.create_visualizations()
        
        # Predict churn
        print("6. Building churn prediction model...")
        churn_model = self.predict_customer_churn()
        
        # Generate insights
        print("7. Generating insights report...")
        insights = self.generate_insights_report()
        
        print("Analysis completed successfully!")
        
        return {
            'customer_metrics': customer_metrics,
            'segments': self.segments,
            'kmeans_analysis': kmeans_analysis,
            'rfm_analysis': rfm_analysis,
            'churn_model': churn_model,
            'insights': insights,
            'dashboard': dashboard
        }

def main():
    """Main function to run customer behavior analytics."""
    analytics = CustomerBehaviorAnalytics()
    results = analytics.run_complete_analysis()
    
    # Print key insights
    print("\n" + "="*50)
    print("KEY INSIGHTS")
    print("="*50)
    print(f"Total Customers: {results['insights']['total_customers']:,}")
    print(f"Total Revenue: ${results['insights']['total_revenue']:,.2f}")
    print(f"Average CLV: ${results['insights']['average_clv']:.2f}")
    print(f"Churn Rate: {results['insights']['churn_rate']}%")
    print(f"Most Valuable Segment: {results['insights']['most_valuable_segment'].name}")
    print(f"Largest Segment: {results['insights']['largest_segment'].name}")

if __name__ == "__main__":
    main()

