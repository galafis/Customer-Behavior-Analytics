        self.models['churn_prediction'] = {
            'model': rf_model,
            'feature_importance': dict(zip(feature_columns, rf_model.feature_importances_)),
            'classification_report': classification_report(y_test, y_pred),
            'confusion_matrix': confusion_matrix(y_test, y_pred)
        }
        return self.models['churn_prediction']

    def generate_insights_report(self):
        if self.segments is None:
            raise ValueError("Customer segmentation must be performed first")
        total_customers = len(self.segments)
        total_revenue = self.segments['total_spent'].sum()
        avg_clv = self.segments['customer_lifetime_value'].mean()
        segment_summary = self.segments.groupby('segment_rfm').agg({
            'customer_id': 'count', 'total_spent': 'sum', 'customer_lifetime_value': 'mean'
        })
        segment_summary.columns = ['customer_count', 'total_revenue', 'avg_clv']
        if total_revenue > 0:
            segment_summary['revenue_percentage'] = (segment_summary['total_revenue'] / total_revenue * 100).round(2)
        else:
            segment_summary['revenue_percentage'] = 0.0
        insights = {
            'total_customers': total_customers,
            'total_revenue': total_revenue,
            'average_clv': avg_clv,
            'most_valuable_segment': segment_summary.loc[segment_summary['avg_clv'].idxmax()] if len(segment_summary) else None,
            'largest_segment': segment_summary.loc[segment_summary['customer_count'].idxmax()] if len(segment_summary) else None,
            'churn_rate': (self.segments['is_churned'].sum() / total_customers * 100).round(2) if total_customers else 0.0,
            'segment_summary': segment_summary
        }
        return insights

    def run_complete_analysis(self):
        print("Starting Customer Behavior Analytics...")
        print("1. Loading data (real if available)...")
        self.load_data()
        print("2. Calculating customer metrics...")
        customer_metrics = self.calculate_customer_metrics()
        print("3. Performing customer segmentation...")
        self.perform_customer_segmentation(customer_metrics)
        print("4. Analyzing segment characteristics...")
        kmeans_analysis, rfm_analysis = self.analyze_segment_characteristics()
        print("5. Creating visualizations...")
        dashboard = self.create_visualizations()
        print("6. Building churn prediction model...")
        churn_model = self.predict_customer_churn()
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
    """
    How to use:
    - Place your real CSV at data/customer_data.csv using columns like:
      customer_id, name, email, age, gender, purchase_amount, purchase_date,
      category, last_login, signup_date, country, city.
    - Run: python customer_analytics.py
    - The script will automatically prefer the real dataset and only generate synthetic
      data if the CSV is missing or invalid. Visualizations will be written to
      customer_behavior_dashboard.html.

    Example:
      $ python customer_analytics.py
    """
    analytics = CustomerBehaviorAnalytics()
    results = analytics.run_complete_analysis()

    print("\n" + "=" * 50)
    print("KEY INSIGHTS")
    print("=" * 50)
    print(f"Total Customers: {results['insights']['total_customers']:,}")
    print(f"Total Revenue: ${results['insights']['total_revenue']:,.2f}")
    print(f"Average CLV: ${results['insights']['average_clv']:.2f}")
    print(f"Churn Rate: {results['insights']['churn_rate']}%")
    if results['insights']['most_valuable_segment'] is not None:
        print(f"Most Valuable Segment: {results['insights']['most_valuable_segment'].name}")
    if results['insights']['largest_segment'] is not None:
        print(f"Largest Segment: {results['insights']['largest_segment'].name}")

if __name__ == "__main__":
    main()
