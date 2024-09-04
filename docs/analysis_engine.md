# Analysis Engine

The Analysis Engine module is responsible for performing various statistical and machine learning analyses on the dataset. It includes methods for:

1. **Descriptive Statistics**:
   - Provides an overview of the dataset, including mean, median, mode, variance, and standard deviation.

2. **Linear Regression**:
   - A predictive analysis that models the relationship between the target variable and the other independent variables in the dataset.

3. **K-Means Clustering**:
   - A machine learning algorithm that partitions the dataset into a predefined number of clusters based on similarity.

## API Endpoints

- `POST /descriptive_statistics/`: Returns descriptive statistics.
- `POST /linear_regression/`: Performs linear regression. Requires a `target_column` in the request body.
- `POST /k_means_clustering/`: Performs K-Means clustering. Requires `num_clusters` in the request body.

## Example Usage

To use the analysis engine, send a POST request to the relevant endpoint with the appropriate parameters. The server will return the analysis results as JSON.

```json
{
    "linear_regression": {
        "coefficients": {
            "feature1": 1.0,
            "feature2": 0.5
        },
        "intercept": 0.0,
        "r_squared": 1.0
    }
}

