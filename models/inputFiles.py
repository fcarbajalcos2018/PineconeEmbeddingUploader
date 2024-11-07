import pandas as pd
import json

class InputFiles():

    def __init__(self):
        self.oaAPI_filename = ''
        self.pcAPI_filename = ''
        self.csv_filename = ''
        self.emb_filename = ''
    
    def set_oaAPIfilename(self, filename: str):
        self.oaAPI_filename = filename
    
    def set_pcAPIfilename(self, filename: str):
        self.pcAPI_filename = filename

    def set_csvFilename(self, filename: str):
        self.csv_filename = filename
    
    def set_embFilename(self, filename: str):
        self.emb_filename = filename
    
    def _isOaAPIfilenameSet(self):
        print(len(self.oaAPI_filename))
        return len(self.oaAPI_filename) > 0
    
    def _isPcAPIfilenameSet(self):
        return len(self.pcAPI_filename) > 0
    
    def _isCSVfilenameSet(self):
        return len(self.csv_filename) > 0
    
    def _isEmbFilenameSet(self):
        return len(self.emb_filename) > 0
    
    def get_oaAPI(self):
        if not self._isOaAPIfilenameSet():
            return ''
        return self._loadAPI(self.oaAPI_filename)
    
    def get_pcAPI(self):
        if not self._isPcAPIfilenameSet():
            return ''
        return self._loadAPI(self.pcAPI_filename)
    
    def _loadAPI(self, filename: str):
        api = ''
        fullDirPath = f'inputFiles/{filename}.txt'
        try:
            with open(file=fullDirPath, mode='r') as file:
                api = file.read()
        except FileNotFoundError:
            print('File not found')
        return api
        
    def get_csv(self):
        if not self._isCSVfilenameSet():
            return None
        fullDirPath = f'inputFiles/{self.csv_filename}.csv'
        data = pd.read_csv(fullDirPath)
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
    
    def get_emb(self) -> dict:
        if not self._isEmbFilenameSet():
            return None
        fullDirPath = f'inputFiles/{self.emb_filename}.json'
        content = {}
        with open(file=fullDirPath, mode='r') as file:
            try:
                content = json.load(file)
            except TypeError as te:
                print('Unable to retrieve contents:', te)
        return content