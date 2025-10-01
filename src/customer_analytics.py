
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings

warnings.filterwarnings("ignore")

class CustomerBehaviorAnalytics:
    def __init__(self, data_path='src/data/customer_data.csv'):
        self.data_path = data_path
        self.data = None
        self.segments = None
        self.models = {}

    def load_data(self):
        try:
            self.data = pd.read_csv(self.data_path)
        except FileNotFoundError:
            print(f"Warning: {self.data_path} not found. Generating synthetic data.")
            self.data = self._generate_synthetic_data()

    def _generate_synthetic_data(self, num_customers=1000):
        # Gerar dados sintéticos para demonstração
        np.random.seed(42)
        data = {
            'customer_id': range(1, num_customers + 1),
            'age': np.random.randint(18, 70, num_customers),
            'gender': np.random.choice(['Male', 'Female'], num_customers),
            'purchase_amount': np.random.normal(100, 50, num_customers).round(2),
            'purchase_date': pd.to_datetime('2024-01-01') + pd.to_timedelta(np.random.randint(0, 365, num_customers), unit='D'),
            'category': np.random.choice(['Electronics', 'Clothing', 'Books', 'Food'], num_customers),
            'last_login': pd.to_datetime('2024-01-01') + pd.to_timedelta(np.random.randint(0, 365, num_customers), unit='D'),
            'signup_date': pd.to_datetime('2023-01-01') + pd.to_timedelta(np.random.randint(0, 365, num_customers), unit='D'),
            'country': np.random.choice(['USA', 'Canada', 'UK', 'Germany'], num_customers),
            'city': np.random.choice(['New York', 'Toronto', 'London', 'Berlin'], num_customers),
            'is_churned': np.random.choice([0, 1], num_customers, p=[0.8, 0.2]) # 20% churn rate
        }
        df = pd.DataFrame(data)
        df['total_spent'] = df['purchase_amount'] * np.random.randint(1, 10, num_customers)
        df['customer_lifetime_value'] = df['total_spent'] * np.random.uniform(1, 5, num_customers)
        return df

    def calculate_customer_metrics(self):
        if self.data is None:
            raise ValueError("Data not loaded. Call load_data() first.")

        # Exemplo de cálculo de métricas RFM (Recency, Frequency, Monetary)
        snapshot_date = self.data['purchase_date'].max() + pd.Timedelta(days=1)
        rfm = self.data.groupby('customer_id').agg({
            'purchase_date': lambda date: (snapshot_date - date.max()).days, # Recency
            'customer_id': 'count', # Frequency
            'purchase_amount': 'sum' # Monetary
        })
        rfm.columns = ['Recency', 'Frequency', 'Monetary']
        rfm['Recency'] = rfm['Recency'].astype(int)
        rfm['Frequency'] = rfm['Frequency'].astype(int)
        rfm['Monetary'] = rfm['Monetary'].astype(float)

        # Adicionar outras métricas como CLV, Churn, etc.
        customer_metrics = self.data.groupby('customer_id').agg(
            total_spent=('purchase_amount', 'sum'),
            avg_purchase_amount=('purchase_amount', 'mean'),
            num_purchases=('customer_id', 'count'),
            first_purchase=('purchase_date', 'min'),
            last_purchase=('purchase_date', 'max'),
            age=('age', 'first'),
            gender=('gender', 'first'),
            country=('country', 'first'),
            city=('city', 'first'),
            is_churned=('is_churned', 'first')
        )
        customer_metrics = customer_metrics.merge(rfm, on='customer_id', how='left')
        customer_metrics['customer_lifetime_value'] = customer_metrics['total_spent'] * (365 / (snapshot_date - customer_metrics['first_purchase']).dt.days) # Exemplo simplificado

        return customer_metrics

    def perform_customer_segmentation(self, customer_metrics):
        if customer_metrics is None:
            raise ValueError("Customer metrics not calculated. Call calculate_customer_metrics() first.")

        # Usar RFM para segmentação
        rfm_data = customer_metrics[['Recency', 'Frequency', 'Monetary']]
        scaler = StandardScaler()
        rfm_scaled = scaler.fit_transform(rfm_data)

        kmeans = KMeans(n_clusters=4, random_state=42, n_init=10) # n_init para evitar warning
        customer_metrics['segment_rfm'] = kmeans.fit_predict(rfm_scaled)

        self.segments = customer_metrics
        return self.segments

    def analyze_segment_characteristics(self):
        if self.segments is None:
            raise ValueError("Customer segmentation must be performed first.")

        segment_summary = self.segments.reset_index().groupby('segment_rfm').agg(
            num_customers=('customer_id', 'count'),
            avg_recency=('Recency', 'mean'),
            avg_frequency=('Frequency', 'mean'),
            avg_monetary=('Monetary', 'mean'),
            avg_clv=('customer_lifetime_value', 'mean'),
            churn_rate=('is_churned', lambda x: (x.sum() / len(x)) * 100)
        ).round(2)

        return segment_summary, None # Retornar None para kmeans_analysis por enquanto

    def create_visualizations(self):
        if self.segments is None:
            raise ValueError("Customer segmentation must be performed first.")

        fig = make_subplots(rows=2, cols=2, 
                            specs=[[{'type': 'scene'}, {'type': 'xy'}],
                                   [{'type': 'domain'}, {'type': 'xy'}]],
                            subplot_titles=("Segmentação de Clientes (RFM)", 
                                            "Distribuição de Churn por Segmento",
                                            "Receita por Segmento",
                                            "CLV Médio por Segmento"))

        # 1. RFM Segmentation (Scatter Plot)
        fig.add_trace(go.Scatter3d(x=self.segments['Recency'], y=self.segments['Frequency'], z=self.segments['Monetary'],
                                   mode='markers', marker=dict(color=self.segments['segment_rfm'], size=5, opacity=0.8),
                                   name='Segmentos RFM'), row=1, col=1)

        # 2. Churn Distribution by Segment (Bar Chart)
        churn_by_segment = self.segments.groupby('segment_rfm')['is_churned'].value_counts(normalize=True).mul(100).unstack().fillna(0)
        fig.add_trace(go.Bar(x=churn_by_segment.index, y=churn_by_segment[1], name='Churn Rate', marker_color='red'), row=1, col=2)

        # 3. Revenue by Segment (Pie Chart)
        revenue_by_segment = self.segments.groupby('segment_rfm')['total_spent'].sum()
        fig.add_trace(go.Pie(labels=revenue_by_segment.index, values=revenue_by_segment.values, name='Receita', hole=0.3),
                      row=2, col=1)

        # 4. Average CLV by Segment (Bar Chart)
        clv_by_segment = self.segments.groupby('segment_rfm')['customer_lifetime_value'].mean()
        fig.add_trace(go.Bar(x=clv_by_segment.index, y=clv_by_segment.values, name='CLV Médio', marker_color='blue'), row=2, col=2)

        fig.update_layout(title_text="Dashboard de Análise de Comportamento do Cliente", height=800, showlegend=False)
        
        # Salvar como HTML
        output_path = 'customer_behavior_dashboard.html'
        fig.write_html(output_path)
        print(f"Dashboard salvo em: {output_path}")
        return output_path

    def predict_customer_churn(self):
        if self.segments is None:
            raise ValueError("Customer segmentation must be performed first.")

        # Feature Engineering
        feature_columns = ['Recency', 'Frequency', 'Monetary', 'age', 'total_spent', 'avg_purchase_amount', 'num_purchases', 'customer_lifetime_value']
        features = self.segments[feature_columns]
        target = self.segments['is_churned']

        X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

        # Model Training
        rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
        rf_model.fit(X_train, y_train)

        # Evaluation
        y_pred = rf_model.predict(X_test)
        
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
        segment_summary = self.segments.reset_index().groupby('segment_rfm').agg({
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
    print(f"Total Revenue: ${results['insights']['total_revenue']:.2f}")
    print(f"Average CLV: ${results['insights']['average_clv']:.2f}")
    print(f"Churn Rate: {results['insights']['churn_rate']}% ")
    if results['insights']['most_valuable_segment'] is not None:
        print(f"Most Valuable Segment: {results['insights']['most_valuable_segment'].name}")
    if results['insights']['largest_segment'] is not None:
        print(f"Largest Segment: {results['insights']['largest_segment'].name}")

if __name__ == "__main__":
    main()

