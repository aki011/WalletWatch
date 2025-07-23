import pandas as pd
import os

def preprocess_uploaded_file(uploaded_file, output_file: str = "data/cleaned_expense_data.csv"):
    try:
        # Read uploaded file
        df = pd.read_csv(uploaded_file)

        # Convert 'Date' column to datetime format
        if 'Date' in df.columns:
            df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        else:
            raise ValueError("Missing 'Date' column")

        # Handle missing values in Date, Amount, and Category
        df = df.dropna(subset=['Date', 'Amount', 'Category'])

        # Convert Amount to numeric
        df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')
        df = df.dropna(subset=['Amount'])

        # Create Month column for filtering (used in current month spend)
        df['Month'] = df['Date'].dt.to_period('M').astype(str)

        # Save the cleaned data
        os.makedirs('data', exist_ok=True)
        df.to_csv(output_file, index=False)

        print(f"✅ Cleaned uploaded data saved to {output_file}")
        return df

    except Exception as e:
        print(f"❌ Error processing uploaded file: {e}")
        return None
