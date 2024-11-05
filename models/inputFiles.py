import pandas as pd

class InputFiles():

    def __init__(self):
        self.oaAPI_filename = ''
        self.pcAPI_filename = ''
        self.csv_filename = ''
    
    def set_oaAPIfilename(self, filename: str):
        self.oaAPI_filename = filename
    
    def set_pcAPIfilename(self, filename: str):
        self.pcAPI_filename = filename

    def set_csvFilename(self, filename: str):
        self.csv_filename = filename
    
    def _isOaAPIfilenameSet(self):
        return len(self.oaAPI_filename) > 0
    
    def _isPcAPIfilenameSet(self):
        return len(self.pcAPI_filename) > 0
    
    def _isCSVfilenameSet(self):
        return len(self.csv_filename) > 0
    
    def get_oaAPI(self):
        if self._isOaAPIfilenameSet():
            return ''
        return self._loadAPI(self.oaAPI_filename)
    
    def get_pcAPI(self):
        if self._isPcAPIfilenameSet():
            return ''
        return self._loadAPI(self.pcAPI_filename)
    
    def _loadAPI(self, filename: str):
        api = ''
        fullDirPath = f'inputFiles/{filename}.txt'
        try:
            with open(fullDirPath, 'r') as file:
                api = file.read()
        except FileNotFoundError:
            print('File not found')
        return api
        
    def get_csv(self):
        if self._isCSVfilenameSet():
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