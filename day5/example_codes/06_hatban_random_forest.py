import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import numpy as np
from datetime import timedelta, datetime

# Read the data from the CSV file
df = pd.read_csv('hatban_prices_by_datetime.csv')

# Ensure there are no null values in the necessary columns
df.dropna(subset=['price'], inplace=True)

# Drop the 'date' column since it's not suitable for direct use in the model
df.drop(['date'], axis=1, inplace=True)

# Prepare the final DataFrame for training
X = df.drop(['price'], axis=1)
Y = df['price']

# Train the Random Forest Regressor
model = RandomForestRegressor(n_estimators=500, random_state=42)
model.fit(X, Y)

# Generate future dates
start_date = datetime(2024, 8, 1)
end_date = datetime(2024, 10, 31)
date_range = pd.date_range(start=start_date, end=end_date, freq='5D')

# Prepare a DataFrame for future predictions
future_data = pd.DataFrame(date_range, columns=['date'])

# Assume the last known values for lag features
last_known_values = df.iloc[-1][['lag_1', 'lag_2', 'lag_3']].values

# Create lag features for future predictions
future_data['lag_1'] = last_known_values[0]
future_data['lag_2'] = last_known_values[1]
future_data['lag_3'] = last_known_values[2]

# Add other features if needed (e.g., day_of_week, month, is_weekend)
future_data['day_of_week'] = future_data['date'].dt.dayofweek
future_data['month'] = future_data['date'].dt.month
future_data['is_weekend'] = future_data['day_of_week'].apply(lambda x: 1 if x >= 5 else 0)

# Drop the 'date' column for prediction
X_future = future_data.drop(['date'], axis=1)

# Make predictions for the future dates
future_predictions = model.predict(X_future)

# Save predictions along with dates to a CSV file
predictions_df = pd.DataFrame({'Date': date_range, 'Predicted Price': future_predictions})
predictions_df.to_csv('future_predictions.csv', index=False)
print('Future predictions saved successfully.')