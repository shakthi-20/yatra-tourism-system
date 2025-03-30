# YATRA - Unified Traveler Registration and Tracking System

## Project Overview
**YATRA** is a Python-based registration system designed for mass traveler management during large gatherings such as melas, pilgrimages, and festivals. The system is built using Tkinter for the user interface and MySQL for database management. It provides:
- Secure traveler registration
- Real-time crowd tracking
- Unique ID generation
- Database-backed record keeping

## Key Features
### 1. Dual Authentication
- New traveler enrollment (Sign Up)
- Returning traveler login (Sign In)

### 2. Comprehensive Registration
- Personal details (Aadhar, contact information)
- Travel specifics (destination, dates)
- Group composition (adults/children)
- Health status (vaccination tracking)

### 3. Smart Tracking System
- Auto-generated unique registration IDs
- MySQL database for permanent records
- Data validation at every step

## Quick Setup
### 1. Prerequisites
- Python 3.6+
- MySQL Server

### 2. Installation
```bash
pip install tkcalendar mysql-connector-python
```

### 3. Database Configuration
Update credentials in `yatra.py` if needed:
```python
import os
import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd=os.getenv("MYSQL_PASSWORD")  # Environment variable for security
)
```
Set the environment variable in the system:
```bash
export MYSQL_PASSWORD="your_password"
```

Alternatively, use a `.env` file with `dotenv`:
```bash
pip install python-dotenv
```
Create a `.env` file and add:
```
MYSQL_PASSWORD=your_password
```
Modify `yatra.py` to load credentials securely:
```python
from dotenv import load_dotenv
load_dotenv()
```

### 4. Launch Application
```bash
python yatra.py
```

## Database Schema
The system automatically creates and manages the following tables:

### 1. `travelers` Table (User Credentials)
| Column         | Type         | Description       |
|--------------|------------|-----------------|
| Name          | VARCHAR(18) | Full name       |
| Aadhar_Number | VARCHAR(12) | Government ID   |
| Phone_Number  | VARCHAR(10) | Contact info    |
| Gender        | VARCHAR(10) | Demographic data |
| Username      | VARCHAR(50) | Login credential |
| Password      | VARCHAR(50) | Encrypted access |
| DOB           | VARCHAR(10) | Date of Birth   |

### 2. `registrations` Table (Travel Details)
| Column             | Type         | Description       |
|-------------------|------------|-----------------|
| Name              | VARCHAR(18) | Traveler name   |
| Aadhar_Number     | VARCHAR(12) | Government ID   |
| Phone_Number      | VARCHAR(10) | Contact info    |
| Number_of_persons | INT         | Adult count     |
| Number_of_children | INT        | Child count     |
| Mode_of_transport | VARCHAR(18) | Public/Private  |
| Type_of_transport | VARCHAR(18) | Vehicle type    |
| Vaccination_status | VARCHAR(20) | Health status   |
| Date_of_arrival   | VARCHAR(10) | Event date      |
| Place_of_visit    | VARCHAR(50) | Destination     |

### 3. `tracking_ids` Table (Unique Identifiers)
| Column         | Type         | Description       |
|--------------|------------|-----------------|
| Name          | VARCHAR(18) | Traveler name   |
| Aadhar_Number | VARCHAR(12) | Government ID   |
| Phone_Number  | VARCHAR(10) | Contact info    |
| Registration_number | INT | Unique tracking ID |

## Operational Flow
1. The administrator launches the system.
2. The traveler selects one of the following options:
   - New registration (Sign Up)
   - Existing user login (Sign In)
3. The system collects:
   - Personal identification details
   - Travel itinerary information
   - Group demographics
   - Health status
4. The application generates:
   - Unique tracking ID
   - Database record
5. The management team can:
   - Monitor crowd size in real-time
   - Verify traveler authenticity
   - Track movement patterns


## Author
Shakthi S
