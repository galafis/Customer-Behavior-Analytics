# Customer Behavior Analytics with R
# Advanced statistical analysis and modeling using R

# Load required libraries
library(dplyr)
library(ggplot2)
library(cluster)
library(factoextra)
library(corrplot)
library(randomForest)
library(caret)
library(plotly)
library(DT)
library(shiny)
library(shinydashboard)

# Customer Behavior Analysis Functions

# Function to load and preprocess data
load_customer_data <- function(file_path = "customer_data.csv") {
  if (file.exists(file_path)) {
    data <- read.csv(file_path)
  } else {
    # Generate sample data if file doesn't exist
    data <- generate_sample_data()
  }
  return(data)
}

# Generate comprehensive sample data
generate_sample_data <- function(n_customers = 2000) {
  set.seed(123)
  
  # Customer demographics
  customers <- data.frame(
    customer_id = paste0("CUST_", sprintf("%05d", 1:n_customers)),
    age = round(rnorm(n_customers, 40, 15)),
    gender = sample(c("M", "F"), n_customers, replace = TRUE, prob = c(0.48, 0.52)),
    income = round(rnorm(n_customers, 50000, 20000)),
    education = sample(c("High School", "Bachelor", "Master", "PhD"), 
                      n_customers, replace = TRUE, prob = c(0.3, 0.4, 0.25, 0.05)),
    location = sample(c("Urban", "Suburban", "Rural"), 
                     n_customers, replace = TRUE, prob = c(0.5, 0.35, 0.15)),
    stringsAsFactors = FALSE
  )
  
  # Ensure realistic age and income ranges
  customers$age <- pmax(18, pmin(80, customers$age))
  customers$income <- pmax(20000, customers$income)
  
  # Generate transaction metrics
  customers$recency <- round(rexp(n_customers, 1/30))  # Days since last purchase
  customers$frequency <- round(rgamma(n_customers, 2, 0.1))  # Number of purchases
  customers$monetary <- round(rgamma(n_customers, 2, 0.001))  # Total spent
  
  # Calculate derived metrics
  customers$avg_order_value <- ifelse(customers$frequency > 0, 
                                     customers$monetary / customers$frequency, 0)
  customers$customer_lifetime_value <- customers$frequency * customers$avg_order_value * 2.5
  
  # Add behavioral indicators
  customers$category_diversity <- round(runif(n_customers, 1, 7))
  customers$channel_consistency <- runif(n_customers, 0.3, 1.0)
  customers$satisfaction_score <- round(rnorm(n_customers, 7.5, 1.5))
  customers$satisfaction_score <- pmax(1, pmin(10, customers$satisfaction_score))
  
  return(customers)
}

# Perform advanced customer segmentation
perform_segmentation <- function(data) {
  # Prepare data for clustering
  clustering_vars <- c("recency", "frequency", "monetary", "age", "income", 
                      "category_diversity", "customer_lifetime_value")
  
  # Remove any rows with missing values
  clean_data <- data[complete.cases(data[clustering_vars]), ]
  
  # Standardize variables
  scaled_data <- scale(clean_data[clustering_vars])
  
  # Determine optimal number of clusters using elbow method
  wss <- sapply(1:10, function(k) {
    kmeans(scaled_data, k, nstart = 10)$tot.withinss
  })
  
  # Perform K-means clustering with optimal k (let's use 5)
  k_optimal <- 5
  kmeans_result <- kmeans(scaled_data, centers = k_optimal, nstart = 25)
  
  # Add cluster assignments to original data
  clean_data$cluster <- as.factor(kmeans_result$cluster)
  
  # Perform hierarchical clustering for comparison
  dist_matrix <- dist(scaled_data)
  hclust_result <- hclust(dist_matrix, method = "ward.D2")
  clean_data$hcluster <- as.factor(cutree(hclust_result, k = k_optimal))
  
  # RFM Analysis
  clean_data$R_score <- as.numeric(cut(clean_data$recency, 
                                      breaks = quantile(clean_data$recency, probs = 0:5/5),
                                      labels = 5:1, include.lowest = TRUE))
  clean_data$F_score <- as.numeric(cut(clean_data$frequency, 
                                      breaks = quantile(clean_data$frequency, probs = 0:5/5),
                                      labels = 1:5, include.lowest = TRUE))
  clean_data$M_score <- as.numeric(cut(clean_data$monetary, 
                                      breaks = quantile(clean_data$monetary, probs = 0:5/5),
                                      labels = 1:5, include.lowest = TRUE))
  
  clean_data$RFM_score <- paste0(clean_data$R_score, clean_data$F_score, clean_data$M_score)
  
  # Define RFM segments
  clean_data$rfm_segment <- case_when(
    clean_data$RFM_score %in% c("555", "554", "544", "545", "454", "455", "445") ~ "Champions",
    clean_data$RFM_score %in% c("543", "444", "435", "355", "354", "345", "344", "335") ~ "Loyal Customers",
    clean_data$RFM_score %in% c("512", "511", "422", "421", "412", "411", "311") ~ "Potential Loyalists",
    clean_data$RFM_score %in% c("533", "532", "531", "523", "522", "521", "515", "514", "513") ~ "New Customers",
    clean_data$R_score <= 2 & clean_data$F_score >= 3 & clean_data$M_score >= 3 ~ "At Risk",
    clean_data$R_score <= 2 & clean_data$F_score <= 2 & clean_data$M_score >= 4 ~ "Cannot Lose Them",
    TRUE ~ "Others"
  )
  
  return(list(
    data = clean_data,
    kmeans_result = kmeans_result,
    hclust_result = hclust_result,
    scaled_data = scaled_data
  ))
}

# Analyze segment characteristics
analyze_segments <- function(segmented_data) {
  data <- segmented_data$data
  
  # K-means segment analysis
  kmeans_summary <- data %>%
    group_by(cluster) %>%
    summarise(
      count = n(),
      avg_recency = mean(recency),
      avg_frequency = mean(frequency),
      avg_monetary = mean(monetary),
      avg_age = mean(age),
      avg_income = mean(income),
      avg_clv = mean(customer_lifetime_value),
      avg_satisfaction = mean(satisfaction_score),
      .groups = 'drop'
    )
  
  # RFM segment analysis
  rfm_summary <- data %>%
    group_by(rfm_segment) %>%
    summarise(
      count = n(),
      avg_recency = mean(recency),
      avg_frequency = mean(frequency),
      avg_monetary = mean(monetary),
      avg_clv = mean(customer_lifetime_value),
      total_revenue = sum(monetary),
      .groups = 'drop'
    ) %>%
    mutate(revenue_percentage = round(total_revenue / sum(total_revenue) * 100, 2))
  
  return(list(
    kmeans_summary = kmeans_summary,
    rfm_summary = rfm_summary
  ))
}

# Create comprehensive visualizations
create_visualizations <- function(segmented_data, analysis_results) {
  data <- segmented_data$data
  
  # 1. Cluster visualization (PCA)
  pca_result <- prcomp(segmented_data$scaled_data, scale. = FALSE)
  pca_data <- data.frame(
    PC1 = pca_result$x[,1],
    PC2 = pca_result$x[,2],
    cluster = data$cluster,
    rfm_segment = data$rfm_segment
  )
  
  p1 <- ggplot(pca_data, aes(x = PC1, y = PC2, color = cluster)) +
    geom_point(alpha = 0.6, size = 2) +
    theme_minimal() +
    labs(title = "Customer Segments (K-means Clustering)",
         subtitle = "PCA Visualization") +
    theme(legend.position = "bottom")
  
  # 2. RFM Segment Distribution
  p2 <- ggplot(data, aes(x = rfm_segment, fill = rfm_segment)) +
    geom_bar() +
    theme_minimal() +
    labs(title = "RFM Segment Distribution",
         x = "RFM Segment", y = "Number of Customers") +
    theme(axis.text.x = element_text(angle = 45, hjust = 1),
          legend.position = "none")
  
  # 3. Customer Lifetime Value by Segment
  p3 <- ggplot(data, aes(x = rfm_segment, y = customer_lifetime_value, fill = rfm_segment)) +
    geom_boxplot() +
    theme_minimal() +
    labs(title = "Customer Lifetime Value by RFM Segment",
         x = "RFM Segment", y = "Customer Lifetime Value") +
    theme(axis.text.x = element_text(angle = 45, hjust = 1),
          legend.position = "none")
  
  # 4. Age vs Income by Cluster
  p4 <- ggplot(data, aes(x = age, y = income, color = cluster)) +
    geom_point(alpha = 0.6, size = 2) +
    theme_minimal() +
    labs(title = "Age vs Income by Cluster",
         x = "Age", y = "Income") +
    theme(legend.position = "bottom")
  
  # 5. Correlation matrix
  numeric_vars <- c("recency", "frequency", "monetary", "age", "income", 
                   "customer_lifetime_value", "satisfaction_score")
  cor_matrix <- cor(data[numeric_vars], use = "complete.obs")
  
  return(list(
    cluster_pca = p1,
    rfm_distribution = p2,
    clv_boxplot = p3,
    age_income_scatter = p4,
    correlation_matrix = cor_matrix
  ))
}

# Build predictive models
build_predictive_models <- function(data) {
  # Predict customer churn (customers with recency > 90 days)
  data$is_churned <- ifelse(data$recency > 90, 1, 0)
  
  # Prepare features for modeling
  feature_vars <- c("frequency", "monetary", "avg_order_value", "age", "income", 
                   "category_diversity", "satisfaction_score")
  
  # Remove rows with missing values
  model_data <- data[complete.cases(data[c(feature_vars, "is_churned")]), ]
  
  # Split data into training and testing sets
  set.seed(123)
  train_index <- createDataPartition(model_data$is_churned, p = 0.8, list = FALSE)
  train_data <- model_data[train_index, ]
  test_data <- model_data[-train_index, ]
  
  # Train Random Forest model for churn prediction
  rf_model <- randomForest(
    as.factor(is_churned) ~ .,
    data = train_data[c(feature_vars, "is_churned")],
    ntree = 100,
    importance = TRUE
  )
  
  # Make predictions
  predictions <- predict(rf_model, test_data[feature_vars])
  
  # Calculate model performance
  confusion_matrix <- table(Predicted = predictions, Actual = test_data$is_churned)
  accuracy <- sum(diag(confusion_matrix)) / sum(confusion_matrix)
  
  # Feature importance
  importance_df <- data.frame(
    feature = rownames(importance(rf_model)),
    importance = importance(rf_model)[, "MeanDecreaseGini"]
  ) %>%
    arrange(desc(importance))
  
  return(list(
    model = rf_model,
    predictions = predictions,
    confusion_matrix = confusion_matrix,
    accuracy = accuracy,
    feature_importance = importance_df
  ))
}

# Generate comprehensive insights report
generate_insights_report <- function(data, analysis_results, model_results) {
  # Key metrics
  total_customers <- nrow(data)
  total_revenue <- sum(data$monetary)
  avg_clv <- mean(data$customer_lifetime_value)
  churn_rate <- mean(data$is_churned) * 100
  
  # Segment insights
  best_segment <- analysis_results$rfm_summary %>%
    arrange(desc(avg_clv)) %>%
    slice(1)
  
  largest_segment <- analysis_results$rfm_summary %>%
    arrange(desc(count)) %>%
    slice(1)
  
  # Model insights
  top_churn_features <- head(model_results$feature_importance, 3)
  
  insights <- list(
    total_customers = total_customers,
    total_revenue = total_revenue,
    avg_clv = avg_clv,
    churn_rate = churn_rate,
    best_segment = best_segment$rfm_segment,
    largest_segment = largest_segment$rfm_segment,
    model_accuracy = model_results$accuracy,
    top_churn_predictors = top_churn_features$feature
  )
  
  return(insights)
}

# Main analysis function
run_customer_analysis <- function() {
  cat("Starting Customer Behavior Analytics with R...\n")
  
  # Load data
  cat("1. Loading customer data...\n")
  customer_data <- load_customer_data()
  
  # Perform segmentation
  cat("2. Performing customer segmentation...\n")
  segmented_data <- perform_segmentation(customer_data)
  
  # Analyze segments
  cat("3. Analyzing segment characteristics...\n")
  analysis_results <- analyze_segments(segmented_data)
  
  # Create visualizations
  cat("4. Creating visualizations...\n")
  visualizations <- create_visualizations(segmented_data, analysis_results)
  
  # Build predictive models
  cat("5. Building predictive models...\n")
  model_results <- build_predictive_models(segmented_data$data)
  
  # Generate insights
  cat("6. Generating insights report...\n")
  insights <- generate_insights_report(segmented_data$data, analysis_results, model_results)
  
  cat("Analysis completed successfully!\n")
  
  # Print key insights
  cat("\n", rep("=", 50), "\n")
  cat("KEY INSIGHTS\n")
  cat(rep("=", 50), "\n")
  cat("Total Customers:", insights$total_customers, "\n")
  cat("Total Revenue: $", format(insights$total_revenue, big.mark = ","), "\n")
  cat("Average CLV: $", round(insights$avg_clv, 2), "\n")
  cat("Churn Rate:", round(insights$churn_rate, 2), "%\n")
  cat("Best Segment:", insights$best_segment, "\n")
  cat("Largest Segment:", insights$largest_segment, "\n")
  cat("Model Accuracy:", round(insights$model_accuracy * 100, 2), "%\n")
  
  return(list(
    data = segmented_data$data,
    analysis = analysis_results,
    visualizations = visualizations,
    models = model_results,
    insights = insights
  ))
}

# Run the analysis
if (!interactive()) {
  results <- run_customer_analysis()
}

