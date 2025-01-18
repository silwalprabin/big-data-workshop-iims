from kafka import KafkaProducer
import random
import time

# Sample data to choose from
diseases = ["Pneumonia", "Hypertension", "Asthma"]
hospitals = ["Greenfield Healthcare", "Lakeside Medical Center"]

# Create a KafkaProducer
producer = KafkaProducer(bootstrap_servers=['kafka:9093'])

# Function to generate a random healthcare record
def generate_random_data():
    patient_id = random.randint(1, 1000)  # Random patient ID between 1 and 1000
    age = random.randint(18, 90)  # Random age between 18 and 90
    gender = random.choice(["Male", "Female"])  # Random gender
    disease = random.choice(diseases)  # Random disease from the list
    treatment_cost = round(random.uniform(500, 5000), 2)  # Random treatment cost between 500 and 5000
    hospital_name = random.choice(hospitals)  # Random hospital name from the list
    
    # Create a dictionary with the generated values
    data = {
        "patient_id": patient_id,
        "age": age,
        "gender": gender,
        "disease": disease,
        "treatment_cost": treatment_cost,
        "hospital_name": hospital_name
    }
    
    return data

# Function to continuously stream data
def stream_data():
    while True:
        # Generate random healthcare data
        data = generate_random_data()
        
        # Send the data to the Kafka topic
        producer.send('healthcare_topic', value=str(data).encode('utf-8'))
        
        # Print the generated data (for debugging or logging)
        print(data)
        
        # Wait for 1 second before sending the next record
        time.sleep(1)

if __name__ == "__main__":
    stream_data()

# from kafka import KafkaProducer
# import csv

# producer = KafkaProducer(bootstrap_servers=['localhost:9092'])

# def stream_data():
#     with open('healthcare_data.csv', 'r') as file:
#         reader = csv.DictReader(file)
#         for row in reader:
#             producer.send('healthcare_topic', value=str(row).encode('utf-8'))

# if __name__ == "__main__":
#     stream_data()