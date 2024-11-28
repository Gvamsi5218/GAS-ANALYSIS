import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib

try:
    # Load dataset
    data = pd.read_csv(r"C:\Users\gvams\OneDrive\Documents\PlatformIO\Projects\Gas Analysis\project\model\training_data.csv")
    
    # Split data into features and labels
    X = data[['ammonia', 'phosphorus', 'temperature', 'humidity']]  # Features
    y = data['freshness_status']  # Target variable

    # Split data into training and testing sets for evaluation
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Initialize and train the model
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)

    # Evaluate the model
    y_pred = model.predict(X_test)
    print("Model Accuracy:", accuracy_score(y_test, y_pred))
    print("Classification Report:\n", classification_report(y_test, y_pred))

    # Save the trained model
    joblib.dump(model, "freshness_model.pkl")
    print("Model training complete and saved as freshness_model.pkl")

except FileNotFoundError:
    print("Error: The file 'training_data.csv' was not found.")
except KeyError:
    print("Error: Ensure the dataset contains the columns 'ammonia', 'phosphorus', 'temperature', 'humidity', and 'freshness_status'.")
except Exception as e:
    print("An error occurred:", str(e))
