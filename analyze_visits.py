import pandas as pd
import numpy as np

## 1. Load and structure the data:
processed_file = "ms_data.csv"  
insurance_file = "insurance.lst"

def load_data(data_file):
    # Read the data from the CSV file
    data = pd.read_csv(data_file)
    
    # Convert visit_date to datetime
    data['visit_date'] = pd.to_datetime(data['visit_date'])
    
    # Sort by patient_id and visit_date
    data = data.sort_values(by=['patient_id', 'visit_date']).reset_index(drop=True)
    
    return data

df = load_data(processed_file)
print(df.head()) 

## 2. Add insurance information: 
# Generate visit costs based on insurance type
def calculate_cost(insurance_type):
        base_cost = {
            "Private": 200,
            "Medicaid": 100,
            "Uninsured": 300
        }[insurance_type]
        variation = np.random.uniform(-20, 20)  
        return base_cost + variation

# Adding insurance info and visit cost to dataframe
def add_insurance_info(data, insurance_file):
    # Read insurance types from `insurance.lst`
    insurance_types = pd.read_csv(insurance_file)['insurance_type'].tolist()
    
    # Randomly assign insurance types consistently for each patient_id
    np.random.seed(44)  
    patient_insurance_map = {pid: np.random.choice(insurance_types) for pid in data['patient_id'].unique()}
    data['insurance_type'] = data['patient_id'].map(patient_insurance_map)
    
    # Creating visit cost column
    data['visit_cost'] = data['insurance_type'].apply(calculate_cost)
    return data

df = add_insurance_info(df, insurance_file) 
print(df.head())


## 3. Calculate summary statistics:
#Calculate summary statistics:
   #Mean walking speed by education level
Mean_speed_edu = df.groupby('education_level')['walking_speed'].mean()
print('The mean of walking speed by education level is the following:', Mean_speed_edu)

   #Mean costs by insurance type
Mean_cost_insurance = df.groupby('insurance_type')['visit_cost'].mean()
print('The mean of visit cost by insurance type is the following:', Mean_cost_insurance)

   #Age effects on walking speed
Age_corr_speed = df['age'].corr(df['walking_speed'])
print('Age and walking speed have the correlation of: ', Age_corr_speed)

df.to_csv("ms_data_export.csv", index=False)
