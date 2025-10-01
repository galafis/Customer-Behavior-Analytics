# Customer Behavior Analytics

## Description
This project aims to analyze customer behavior using purchase data to identify patterns, segment customers, and predict churn. It utilizes RFM (Recency, Frequency, Monetary) analysis and machine learning techniques to provide actionable insights.

## Features
- **Synthetic Data Generation**: If no data file is provided, the project can generate synthetic data for demonstration purposes.
- **Customer Metrics Calculation**: Calculates important metrics such as Recency, Frequency, Monetary (RFM), and Customer Lifetime Value (CLV).
- **Customer Segmentation**: Uses the K-Means algorithm to segment customers based on their RFM metrics.
- **Segment Characteristics Analysis**: Provides a summary of the characteristics of each customer segment.
- **Interactive Visualizations**: Generates an interactive HTML dashboard with 3D segmentation plots, churn distribution, revenue by segment, and average CLV by segment.
- **Churn Prediction**: Builds and evaluates a Random Forest model to predict customer churn.
- **Insights Report**: Generates a consolidated report with key insights from the analysis.

## Installation
To set up the development environment, follow the steps below:

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/Customer-Behavior-Analytics.git
   cd Customer-Behavior-Analytics
   ```

2. Create and activate a virtual environment (optional, but recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r config/requirements.txt
   ```

## Usage
To run the complete analysis, execute the main script:

```bash
python3 src/customer_analytics.py
```

- If you have your own customer data in CSV format, place it in `src/data/customer_data.csv`. The script will use this data. Otherwise, synthetic data will be automatically generated.
- An interactive dashboard (`customer_behavior_dashboard.html`) will be generated in the project's root directory.

## Project Structure
```
Customer-Behavior-Analytics/
├── config/
│   └── requirements.txt
├── docs/
│   └── notebooks/
├── src/
│   ├── data/
│   │   └── customer_data.csv (optional, for your data)
│   └── customer_analytics.py
├── tests/
│   └── test_customer_analytics.py
├── .gitignore
└── README.md
```

## Technologies Used
- Python 3.x
- Pandas
- NumPy
- Scikit-learn
- Plotly

## License
This project is licensed under the MIT License. See the `LICENSE` file for more details.

## Contribution
Contributions are welcome! Please follow these guidelines:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Make your changes and commit them (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a Pull Request.
