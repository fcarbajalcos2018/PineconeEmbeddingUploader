import pandas as pd

def loadFiles(oaFile: str, pcFile: str, csv: pd.DataFrame, pcServFile):
    oaAPI = loadAPIFile(oaFile)
    pcAPI = loadAPIFile(pcFile)
    csvData = loadCSV(csv)
    pcServer = loadAPIFile(pcServFile)
    return oaAPI, pcAPI, csvData, pcServer

def loadAPIFile(fileName: str):
    api = ''
    try:
        with open(fileName, 'r') as file:
            api = file.read()
    except FileNotFoundError:
        print('File not found')
        return ''
    return api

def loadCSV(fileName: str):
    data = pd.read_csv(fileName)
    parsedData = []
    for i, row in data.iterrows():
        rowData = {
            'id': row['id'],
            'type': row['type'],
            'title': row['title'],
            'content': row['content'],
            'envId': row['envId'],
            'refId': row['refId']
        }
        parsedData.append(rowData)
    return parsedData

def main():
    print('Start project straightforward')
    print('Load files')
    oaFile = 'inputFiles/APIKey.txt'
    pcFile = 'inputFiles/pcAPIKey.txt'
    csv = 'inputFiles/testVectors-csv-2024-10-14.csv'
    pcServFile = 'inputFiles/pcServer.txt'
    oaAPI, pcAPI, csvData, pcServ = loadFiles(oaFile, pcFile, csv, pcServFile)
    print('OpenAI API:', oaAPI)
    print('Pinecone API:', pcAPI)
    print('CSV:')
    print([row['id'] for row in csvData])
    print('Pinecone Server:', pcServ)

main()