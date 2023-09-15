import os
from functions import downloadPdfData, extractIncidents, createDatabase, insertIncidentData, status

tmpFile = None
incident_data = None
dbName = 'normanpd.db'

def test_downloadPdfData():
    url = 'https://www.normanok.gov/sites/default/files/documents/2023-01/2023-01-01_daily_incident_summary.pdf';
    global tmpFile
    tmpFile = downloadPdfData(url)
    assert os.path.exists(tmpFile.name) and os.path.getsize(tmpFile.name) > 0


def test_extractIncidents():
    global incident_data
    incident_data = extractIncidents(tmpFile)
    assert len(incident_data) > 0 

def test_createDatabase():
    assert createDatabase(dbName)

def test_insertIncidentData():
    assert insertIncidentData(dbName, incident_data)

def test_status():
    assert status(dbName)


test_downloadPdfData()
test_extractIncidents()
test_createDatabase()
test_insertIncidentData()
test_status()
