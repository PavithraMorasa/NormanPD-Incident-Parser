import requests
from pypdf import PdfReader
import re
import sqlite3
import tempfile
import os

def add_space_before_last_capital(string):
    first_word = re.findall(r'\b\w+\b', string)[0] 
    index = max([i for i, c in enumerate(first_word) if c.isupper()])
    first_word_with_space = first_word[:index] + ' ' + first_word[index:] 
    new_string = string.replace(first_word, first_word_with_space, 1) 
    return new_string

def downloadPdfData(url):
    tmp_file = tempfile.NamedTemporaryFile(delete=False) 
    response = requests.get(url)
    tmp_file.write(response.content) 
    tmp_file.flush()
    return tmp_file

def extractIncidents(tmpFile):
    tmpFile.seek(0);
    pdf_file = open(tmpFile.name, 'rb')
    reader = PdfReader(pdf_file)
    pdfPages = reader.pages
    incidents_data =[]
    num_of_pages = len(pdfPages)
    
    for i in range(num_of_pages):
        text = pdfPages[i].extract_text()
        remove = ['NORMAN POLICE DEPARTMENT', 'Daily Incident Summary (Public)']
        text = text.replace(remove[0], "");
        text = text.replace(remove[1], "");
        text = re.sub(r'(\d{4}-\d{8})', r' \1 ', text)
        lines = text.split('\n')
        date_time_pattern1 = r'[0-9]{1,2}/[0-9]{1,2}/[0-9]{4}\s[0-9]{1,2}:[0-9]{2}';
        new_lines = []
        for i, line in enumerate(lines):
            if i == 0 or re.match(date_time_pattern1, line):
                new_lines.append(line)
            else:
                prev_line = new_lines.pop()
                if len(line) > 0:
                    line = add_space_before_last_capital(line)
                if not re.match(date_time_pattern1, prev_line):
                    prev_line += ' '
                new_lines.append(prev_line + line + ' ')
        lines = new_lines        
        for line in lines:
            date_time = ''
            incident_number = ''
            location = ''
            nature = ''
            incident_roi = ''
            date_time_pattern = r'[0-9]{1,2}/[0-9]{1,2}/[0-9]{4}\s[0-9]{1,2}:[0-9]{2}';
            date_time_match = re.search(date_time_pattern, line)
            incident_number_pattern = r'\d{4}-\d{8}';
            incident_number_match = re.search(incident_number_pattern, line)
            roi_expression = r'\b\w{5,9}\b(?:(?!\b\w{5,9}\b).)*$';
            incident_roi_match = re.search(roi_expression, line)
            if date_time_match and incident_number_match and incident_roi_match:              
                date_time = date_time_match.group()
                incident_number = incident_number_match.group()
                incident_roi = incident_roi_match.group(0)                
                index = line.find(incident_number)
                start_index = index + len(incident_number)
                end_index = line.find(incident_roi)          
                sub_line = line[start_index:end_index]                
                if len(sub_line.strip()) > 0: 
                    pattern = r'\b[A-Z][a-z]+\b'
                    match = re.search(pattern, sub_line)
                    if match:
                        index = match.start()
                    else:
                        index = len(sub_line)
                    location = sub_line[:index].strip()
                    nature = sub_line[index:].strip()
                    if not nature:
                        last_word = location.rsplit(None, 1)[-1]
                        location = location[:len(location) - len(last_word)].strip()
                        nature = last_word
                    incident_fields = [date_time, incident_number, location, nature, incident_roi]
                    incident = "|".join(incident_fields)
                    incidents_data.append(incident)
    pdf_file.close()
    tmpFile.close()
    os.unlink(tmpFile.name)
    return incidents_data                
            
def createDatabase(dbName):
    try:
        # Connect to database & It will creates database file if it doesn't exist
        conn = sqlite3.connect(dbName)

        # It is Cursor object to execute SQL commands
        c = conn.cursor()

        # Execute the DROP TABLE statement
        c.execute('DROP TABLE IF EXISTS incidents')

        # Create Table if doesn't exist
        c.execute('''CREATE TABLE incidents 
                    (incident_time TEXT, `incident_number` TEXT, incident_location TEXT, nature TEXT, `incident_ori` TEXT)''')

        # Commit changes made and close connection
        conn.commit()
        conn.close()
        print("Database creation successful")
        return True
    except Exception as e:
        print("Database creation failed: ", e)
        return False

def insertIncidentData(dbName, incidents_data):
    try: 
        # Connect to the database
        conn = sqlite3.connect(dbName)
        c = conn.cursor()

        # Delete previously inserted data
        c.execute("DELETE FROM incidents")

        for incident in incidents_data:
            # Separate field values by splitting
            value = incident.split('|')

            # Convert the list of values to a tuple
            values_tuple = tuple(value)

            c.execute('INSERT INTO incidents VALUES (?, ?, ?, ?, ?)', values_tuple)

        # Commit all the changes and close the connection
        conn.commit()
        conn.close()
        print("Insertion successful")
        return True
    except Exception as e:
        print("Insertion failed: ", e)
        return False

def status(dbName):
    try:
        # Connect to the database
        conn = sqlite3.connect(dbName)
        c = conn.cursor()

        # Query to Select number of incidents occured in each Nature of incident
        c.execute('SELECT nature, COUNT(*) FROM incidents GROUP BY nature')

        # Fetching all the rows of of previous query
        rows = c.fetchall()

        # Print the results
        for row in rows:
            print(row[0], '|', row[1])

        # Close the connection
        conn.close()
        print("Fetching data successful")
        return True
    except Exception as e:
        print("Fetching data failed: ", e)
        return False
