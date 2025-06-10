## Interpretation of Results and Model Selection

| Model                           | Accuracy | Recall | Precision | F1 Score | ROC AUC | Key Insight                                                 |
|--------------------------------|----------|--------|-----------|----------|---------|-------------------------------------------------------------|
| Logistic Regression (tuned)    | 59.7%    | **63.9%** | 26.0%    | **0.369** | 0.657   | Highest sensitivity to delayed flights                      |
| Voting Classifier              | **71.3%**| 45.1%  | 31.0%    | **0.368** | **0.660** | Balanced and robust ensemble performance                    |
| Logistic Regression (default)  | 63.0%    | 58.3%  | 26.9%    | **0.368** | 0.657   | Transparent and effective without threshold tuning          |
| Random Forest                  | 70.0%    | 41.9%  | 28.7%    | 0.341    | 0.634   | Interpretable and stable under different scenarios          |
| XGBoost                        | 82.3%    | 11.0%  | **62.3%** | 0.186    | **0.705** | High AUC, but impractical for delay detection due to low recall |


In the context of commercial airline operations, anticipating flight delays is not merely a statistical exercise—it has direct consequences for resource allocation, passenger experience, operational costs, and tactical scheduling. Being able to predict a delay in advance enables proactive measures such as adjusting gates, reallocating ground staff, notifying passengers, and preventing cascading disruptions across the flight network.

From this operational standpoint, we evaluated five predictive models with a strong emphasis on recall, which indicates the ability to correctly identify flights that will actually be delayed. High recall is crucial because failing to anticipate a delay is typically more costly than triggering a false alert.

Among all models, the Logistic Regression with a tuned decision threshold (0.48) delivered the highest recall (63.9%), making it the most sensitive to delayed flights. This threshold adjustment allowed the model to capture more true delays at the cost of lower precision—a trade-off that is acceptable in scenarios where the priority is to act early and mitigate impact. For airline operations, especially during peak seasons or congested schedules, this model serves as a valuable early warning tool to reduce passenger dissatisfaction and logistical bottlenecks.

The Voting Classifier, which combines Logistic Regression and Random Forest, demonstrated the best balance between precision and recall, achieving a recall of 45.1% and an F1 Score nearly identical to the tuned logistic model. It leverages the sensitivity of logistic regression and the robustness of Random Forest, making it particularly well-suited for real-time systems that require both resilience and consistency under varying flight conditions like national holidays or labor strikes.

The default Logistic Regression model (threshold = 0.5) maintained excellent performance, reaching a recall of 58.3% and an F1 Score of 36.8%, only slightly below the tuned version. It stands out for its simplicity and interpretability, making it a strong candidate for immediate deployment without threshold calibration, especially where ease of explanation and operational traceability are critical.

Random Forest, while slightly weaker in terms of recall (41.9%), proved to be a stable and interpretable model. Its tree-based structure provides transparency about how variables like flight type, time of day, and destination city influence the prediction. It is a valuable fallback option or even a co-pilot model in a decision support system.

Lastly, XGBoost delivered the highest accuracy (82.3%) and ROC AUC (70.5%), but had a recall of only 11.0%. This makes it highly conservative—very precise, but missing the vast majority of actual delays. For day-to-day operations where early detection of disruptions is critical, this model is not recommended, unless the specific use case demands extremely low false-positive rates.

A key insight from this analysis is the impact of feature engineering. Contextual variables like is_holiday, is_strike_day, and the inclusion of historical weather data significantly enhanced model performance. These features improved the model’s ability to generalize under non-standard operational conditions such as holidays, strikes, and adverse weather. This validates the importance of integrating external operational data sources to boost predictive accuracy and reliability in real-world airline scenarios.

______________________________
