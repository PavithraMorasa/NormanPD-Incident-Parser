# NormanPD Incident Parser

This project is a Python-based data extraction tool that processes publicly available PDF files from the Norman Police Department. It extracts key information from each reported incident, stores it in a structured SQLite database, and provides a summary of the types of incidents recorded.

---

## 🧠 What the Project Does

The NormanPD Incident Parser performs the following steps:

1. **Downloads a PDF report** from a provided URL (hosted on the Norman, OK government website).
2. **Extracts structured data** such as:
   - Date and time of the incident  
   - Incident number  
   - Location  
   - Nature of the incident (e.g., THEFT, ASSAULT)  
   - ORI (Originating Agency Identifier)
3. **Stores this data in an SQLite database** for easy querying and future analysis.
4. **Displays a summary** of how many incidents occurred under each type (e.g., how many THEFT cases were recorded).

---

## 🔧 How It Works

### 1. **PDF Download**
The `downloadPdfData()` function fetches a daily incident summary PDF from a given URL and stores it temporarily.

### 2. **Text Extraction & Parsing**
The `extractIncidents()` function uses `PyPDF` to extract text from each page of the PDF. Regular expressions clean and format the data into individual incidents.

### 3. **Database Creation**
The `createDatabase()` function sets up an SQLite database named `normanpd.db` with a table to store incident data.

### 4. **Data Insertion**
The `insertIncidentData()` function adds all parsed incidents into the database.

### 5. **Summary Display**
The `status()` function prints a grouped summary of incidents by their "nature" (e.g., THEFT | 3).

---

## ▶️ How to Run the Project

Make sure you have Python 3.10+ installed.

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/NormanPD-IncidentParser.git
cd NormanPD-IncidentParser
```
### 2. Install Dependencies
```bash
pip install requests pypdf pytest
```
### 3. Run the Parser
```bash
python main.py --incidents "https://www.normanok.gov/sites/default/files/documents/2023-01/2023-01-01_daily_incident_summary.pdf"
```
This will:

* Download the PDF

* Extract incident data

* Create the database

* Insert data into the database

* Print a summary of incidents by type

### How to test:

To run simple tests that validate each function works correctly:
```bash
python test_functions.py
```
This script will:
* Download a test PDF

* Extract incidents

* Create and populate the database

* Display a summary

* Confirm each step is successful using assert checks

### Files in this project:

* __main.py__: CLI entry point to run the parser
* __functions.py__: All core logic for download, parse, and database operations
* __test_functions.py__: Functional tests for end-to-end verification
* __setup.py__: Python package setup file (for PyPI or installable use)
* __normanpd.db__: Generated SQLite database after running the script
