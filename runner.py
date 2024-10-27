
def loadFiles(oaFile, pcFile, csv, pcServFile):
    oaAPI = loadAPIFile(oaFile)
    pcAPI = loadAPIFile(pcFile)
    csvData = ''
    pcServer = loadAPIFile(pcServFile)
    return oaAPI, pcAPI, csvData, pcServer

def loadAPIFile(fileName):
    api = ''
    try:
        with open(fileName, 'r') as file:
            api = file.read()
    except FileNotFoundError:
        print('File not found')
        return ''
    return api

def main():
    print('Start project straightforward')
    print('Load files')
    oaFile = 'inputFiles/APIKey.txt'
    pcFile = 'inputFiles/pcAPIKey.txt'
    csv = 'inputFiles/testVectors-csv-2024-10-14.txt'
    pcServFile = 'inputFiles/pcServer.txt'
    oaAPI, pcAPI, csvData, pcServ = loadFiles(oaFile, pcFile, csv, pcServFile)
    print('OpenAI API:', oaAPI, pcAPI, pcServ)

main()