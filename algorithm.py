import csv
from datetime import datetime, timedelta

class Doctor:
    def __init__(self, name, availability):
        self.name = name
        self.availability = availability
        self.appointments = []

class Patient:
    def __init__(self, name, duration):
        self.name = name
        self.duration = duration

def read_doctor_data(file_path):
    doctors = []
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            availability = [
                (
                    datetime.strptime(row['availability_start'], '%d-%m-%Y %H:%M'),
                    datetime.strptime(row['availability_end'], '%d-%m-%Y %H:%M')
                )
            ]
            doctors.append(Doctor(row['name'], availability))
    return doctors


def read_patient_data(file_path):
    patients = []
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            patients.append(Patient(row['name'], int(row['duration'])))
    return patients

def schedule_appointment(doctors, patients):
    for patient in patients:
        scheduled = False
        for doctor in doctors:
            for start_time, end_time in doctor.availability:
                current_time = start_time
                while current_time + timedelta(minutes=patient.duration) <= end_time:
                    if all(current_time + timedelta(minutes=d) not in doctor.appointments for d in range(patient.duration)):
                        doctor.appointments.extend([current_time + timedelta(minutes=d) for d in range(patient.duration)])
                        print(f"Appointment scheduled for {patient.name} with {doctor.name} from {current_time} to {current_time + timedelta(minutes=patient.duration)}")
                        scheduled = True
                        break
                    current_time += timedelta(minutes=1)
                if scheduled:
                    break  # Break out of doctor loop once appointment is scheduled
            if scheduled:
                break  # Break out of patient loop once appointment is scheduled
        if not scheduled:
            print(f"No suitable time slot found for {patient.name}.")


# Read data from files
doctors = read_doctor_data(r'C:\Users\palag\OneDrive\Desktop\Scheduling Algorithm\doctors.csv')
patients = read_patient_data(r'C:\Users\palag\OneDrive\Desktop\Scheduling Algorithm\patients.csv')

# Schedule appointments
schedule_appointment(doctors, patients)
