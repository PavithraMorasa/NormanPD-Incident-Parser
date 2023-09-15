import argparse
import functions

def main(url):
    dbName = 'normanpd.db'
    pdfContent = functions.downloadPdfData(url)
    incidents = functions.extractIncidents(pdfContent)
    functions.createDatabase(dbName)
    functions.insertIncidentData(dbName, incidents)
    functions.status(dbName)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--incidents", type=str, required=True, 
                         help="Incident summary url.")
    
    args = parser.parse_args()
    if args.incidents:
        main(args.incidents)
