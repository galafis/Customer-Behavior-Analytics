
import unittest
import pandas as pd
import numpy as np
from src.customer_analytics import CustomerBehaviorAnalytics

class TestCustomerBehaviorAnalytics(unittest.TestCase):

    def setUp(self):
        self.analytics = CustomerBehaviorAnalytics(data_path='non_existent_path.csv')
        self.analytics.load_data() # Isso deve gerar dados sintéticos

    def test_load_data_synthetic(self):
        self.assertIsNotNone(self.analytics.data)
        self.assertGreater(len(self.analytics.data), 0)
        self.assertIn('customer_id', self.analytics.data.columns)

    def test_calculate_customer_metrics(self):
        metrics = self.analytics.calculate_customer_metrics()
        self.assertIsNotNone(metrics)
        self.assertIn('Recency', metrics.columns)
        self.assertIn('Frequency', metrics.columns)
        self.assertIn('Monetary', metrics.columns)
        self.assertIn('customer_lifetime_value', metrics.columns)

    def test_perform_customer_segmentation(self):
        metrics = self.analytics.calculate_customer_metrics()
        segments = self.analytics.perform_customer_segmentation(metrics)
        self.assertIsNotNone(segments)
        self.assertIn('segment_rfm', segments.columns)
        self.assertGreater(segments['segment_rfm'].nunique(), 1)

    def test_analyze_segment_characteristics(self):
        metrics = self.analytics.calculate_customer_metrics()
        self.analytics.perform_customer_segmentation(metrics)
        summary, _ = self.analytics.analyze_segment_characteristics()
        self.assertIsNotNone(summary)
        self.assertIn('num_customers', summary.columns)
        self.assertIn('avg_recency', summary.columns)

    def test_create_visualizations(self):
        metrics = self.analytics.calculate_customer_metrics()
        self.analytics.perform_customer_segmentation(metrics)
        output_path = self.analytics.create_visualizations()
        self.assertTrue(output_path.endswith('.html'))
        # Verificar se o arquivo foi criado (pode ser necessário um mock para isso em um ambiente real)
        # import os
        # self.assertTrue(os.path.exists(output_path))

    def test_predict_customer_churn(self):
        metrics = self.analytics.calculate_customer_metrics()
        self.analytics.perform_customer_segmentation(metrics)
        churn_model_results = self.analytics.predict_customer_churn()
        self.assertIsNotNone(churn_model_results)
        self.assertIn('model', churn_model_results)
        self.assertIn('feature_importance', churn_model_results)

    def test_generate_insights_report(self):
        metrics = self.analytics.calculate_customer_metrics()
        self.analytics.perform_customer_segmentation(metrics)
        insights = self.analytics.generate_insights_report()
        self.assertIsNotNone(insights)
        self.assertIn('total_customers', insights)
        self.assertIn('total_revenue', insights)

    def test_run_complete_analysis(self):
        results = self.analytics.run_complete_analysis()
        self.assertIsNotNone(results)
        self.assertIn('customer_metrics', results)
        self.assertIn('segments', results)
        self.assertIn('churn_model', results)
        self.assertIn('insights', results)
        self.assertIn('dashboard', results)

if __name__ == '__main__':
    unittest.main()

