from models.inputFiles import InputFiles
from models.pineconeService import PineconeService

def userWelcome():
    print('Welcome to the Pinecone Embedding and Vector Uploader!')
    print('Press 1 to start a new upload')
    print('Press 2 to continue an upload from saved file')
    res = int(input('Your response: '))
    if res == 1:
        print('You selected (1) to start a new upload job')
        _userInputNew()
    elif res == 2:
        print('You selected (2) to load an existing save file and continue upload job')
        _userInputLoad()
    else:
        print('Your selection was INVALID. Please reattempt.')
        userWelcome()

def _userInputNew():
    inFile = InputFiles()
    print('Please enter the name of the file containing the Open AI API Key')
    oaFileName = input('OpenAI API Key File: ')
    inFile.set_oaAPIfilename(oaFileName)
    print('Please enter the name of the file containing the Pinecone API Key')
    pcFileName = input('Pinecone API Key File: ')
    inFile.set_pcAPIfilename(pcFileName)
    print('Please enter the name of the CSV file containing the Embeddings')
    csvFileName = input('CSV File:')
    inFile.set_csvFilename(csvFileName)
    print('Proceeding to access contents of files...')
    oaAPI = inFile.get_oaAPI()
    pcAPI = inFile.get_pcAPI()
    csv = inFile.get_csv()
    if len(oaAPI) == 0 or len(pcAPI) == 0 or len(csv) == 0:
        print('Unable to access file contents.')
        print('The names you entered do not match with existing files in this directory. Please reattempt.')
        _userInputNew()
        return
    # Start Pinecone Service

def _userInputLoad():
    inFile = InputFiles()
    print('Please enter the name of the JSON file containing the SAVED embeddings')
    embFileName = input('JSON File: ')
    inFile.set_embFilename(embFileName)
    print('Loading file...')
    emb = inFile.get_emb()
    if len(emb) == 0:
        print('Unable to access file contents.')
        print('The names you entered do not match with existing files in this directory. Please reattempt.')
        emb = _userInputLoad()
    return emb

def main():
    print('Start project OOP')

main()