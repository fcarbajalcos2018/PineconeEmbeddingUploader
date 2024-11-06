from typing import Any
from models.inputFiles import InputFiles
from models.pineconeService import PineconeService

def userWelcome():
    print('Welcome to the Pinecone Embedding and Vector Uploader!')
    print('Press 1 to start a new upload')
    print('Press 2 to continue an upload from saved file')
    res = int(input('Your response: '))
    bundle = None
    if res == 1:
        print('You selected (1) to start a new upload job')
        bundle = _userInputNew()
    elif res == 2:
        print('You selected (2) to load an existing save file and continue upload job')
        bundle = _userInputLoad()
    else:
        print('Your selection was INVALID. Please reattempt.')
        userWelcome()
        return
    oaAPI, pcAPI, embeddingSet = bundle
    print('Initializing Pinecone service....')
    pc = PineconeService(oaAPI=oaAPI, pcAPI=pcAPI)
    _userDefineIndex(pinecone=pc, embeddings=embeddingSet)

def __insertOaPc(inFile: InputFiles):
    print('Please enter the name of the file containing the Open AI API Key')
    oaFileName = input('OpenAI API Key File: ')
    inFile.set_oaAPIfilename(oaFileName)
    print('Please enter the name of the file containing the Pinecone API Key')
    pcFileName = input('Pinecone API Key File: ')
    inFile.set_pcAPIfilename(pcFileName)
    return inFile.get_oaAPI(), inFile.get_pcAPI()

def _userInputNew():
    inFile = InputFiles()
    oaAPI, pcAPI = __insertOaPc(inFile=inFile)
    print('Please enter the name of the CSV file containing the Embeddings')
    csvFileName = input('CSV File:')
    inFile.set_csvFilename(csvFileName)
    print('Proceeding to access contents of files...')
    csv = inFile.get_csv()
    bundle = oaAPI, pcAPI, csv
    if len(oaAPI) == 0 or len(pcAPI) == 0 or len(csv) == 0:
        print('Unable to access file contents.')
        print('The names you entered do not match with existing files in this directory. Please reattempt.')
        bundle = _userInputNew()
    return bundle

def _userInputLoad():
    inFile = InputFiles()
    oaAPI, pcAPI = __insertOaPc(inFile=inFile)
    print('Please enter the name of the JSON file containing the SAVED embeddings')
    embFileName = input('JSON File: ')
    inFile.set_embFilename(embFileName)
    print('Loading file...')
    emb = inFile.get_emb()
    bundle = oaAPI, pcAPI, emb
    if len(oaAPI) == 0 or len(pcAPI) == 0 or len(emb) == 0:
        print('Unable to access file contents.')
        print('The names you entered do not match with existing files in this directory. Please reattempt.')
        bundle = _userInputLoad()
    return bundle

def _userDefineIndex(pinecone: PineconeService, embeddings: Any | dict | list | None):
    raise NotImplementedError()

def main():
    print('Start project OOP')

main()