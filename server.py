#!/usr/bin/env python3
"""
Flask REST API Server for Customer Behavior Analytics
Provides minimal RESTful endpoints for customer data analysis
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import os
from datetime import datetime
import json

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing

# Configuration
DATA_FILE = 'data/customer_data.csv'

def load_customer_data():
    """Load customer data from CSV file"""
    try:
        if os.path.exists(DATA_FILE):
            return pd.read_csv(DATA_FILE)
        else:
            return pd.DataFrame()  # Return empty DataFrame if file doesn't exist
    except Exception as e:
        print(f"Error loading data: {e}")
        return pd.DataFrame()

@app.route('/')
def home():
    """API Information endpoint"""
    return jsonify({
        'message': 'Customer Behavior Analytics API',
        'version': '1.0',
        'endpoints': {
            '/api/customers': 'GET - List all customers',
            '/api/customers/<id>': 'GET - Get specific customer',
            '/api/analytics/summary': 'GET - Customer analytics summary',
            '/api/analytics/demographics': 'GET - Demographics analysis',
            '/api/analytics/purchases': 'GET - Purchase behavior analysis'
        }
    })

@app.route('/api/customers', methods=['GET'])
def get_customers():
    """Get all customers with optional filtering"""
    try:
        df = load_customer_data()
        if df.empty:
            return jsonify({'error': 'No customer data available'}), 404
        
        # Optional filtering by query parameters
        country = request.args.get('country')
        category = request.args.get('category')
        
        if country:
            df = df[df['country'].str.lower() == country.lower()]
        if category:
            df = df[df['category'].str.lower() == category.lower()]
        
        return jsonify({
            'customers': df.to_dict('records'),
            'total_count': len(df)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/customers/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    """Get specific customer by ID"""
    try:
        df = load_customer_data()
        if df.empty:
            return jsonify({'error': 'No customer data available'}), 404
        
        customer = df[df['customer_id'] == customer_id]
        if customer.empty:
            return jsonify({'error': 'Customer not found'}), 404
        
        return jsonify(customer.iloc[0].to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analytics/summary', methods=['GET'])
def analytics_summary():
    """Provide basic analytics summary"""
    try:
        df = load_customer_data()
        if df.empty:
            return jsonify({'error': 'No customer data available'}), 404
        
        summary = {
            'total_customers': len(df),
            'total_revenue': float(df['purchase_amount'].sum()),
            'average_purchase': float(df['purchase_amount'].mean()),
            'countries': df['country'].nunique(),
            'categories': df['category'].nunique(),
            'gender_distribution': df['gender'].value_counts().to_dict(),
            'top_categories': df['category'].value_counts().head(5).to_dict(),
            'top_countries': df['country'].value_counts().head(5).to_dict()
        }
        return jsonify(summary)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analytics/demographics', methods=['GET'])
def demographics_analysis():
    """Analyze customer demographics"""
    try:
        df = load_customer_data()
        if df.empty:
            return jsonify({'error': 'No customer data available'}), 404
        
        demographics = {
            'age_statistics': {
                'average_age': float(df['age'].mean()),
                'min_age': int(df['age'].min()),
                'max_age': int(df['age'].max()),
                'median_age': float(df['age'].median())
            },
            'gender_breakdown': df['gender'].value_counts().to_dict(),
            'geographic_distribution': df.groupby('country')['customer_id'].count().to_dict(),
            'city_distribution': df.groupby('city')['customer_id'].count().to_dict()
        }
        return jsonify(demographics)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analytics/purchases', methods=['GET'])
def purchase_analysis():
    """Analyze purchase behavior"""
    try:
        df = load_customer_data()
        if df.empty:
            return jsonify({'error': 'No customer data available'}), 404
        
        purchase_data = {
            'revenue_by_category': df.groupby('category')['purchase_amount'].sum().to_dict(),
            'purchases_by_category': df['category'].value_counts().to_dict(),
            'average_by_category': df.groupby('category')['purchase_amount'].mean().to_dict(),
            'revenue_by_gender': df.groupby('gender')['purchase_amount'].sum().to_dict(),
            'revenue_by_country': df.groupby('country')['purchase_amount'].sum().to_dict(),
            'total_revenue': float(df['purchase_amount'].sum()),
            'transaction_count': len(df)
        }
        return jsonify(purchase_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'data_available': os.path.exists(DATA_FILE)
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    print(f"Starting Flask server on port {port}")
    print(f"Debug mode: {debug}")
    print(f"Data file: {DATA_FILE}")
    
    app.run(host='0.0.0.0', port=port, debug=debug)
