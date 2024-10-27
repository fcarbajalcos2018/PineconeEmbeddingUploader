import openai
import pandas as pd
import pinecone

def loadFiles(oaFile: str, pcFile: str, csv: pd.DataFrame, pcServFile):
    oaAPI = lf_loadAPIFile(oaFile)
    pcAPI = lf_loadAPIFile(pcFile)
    csvData = lf_loadCSV(csv)
    pcServer = lf_loadAPIFile(pcServFile)
    return oaAPI, pcAPI, csvData, pcServer

def lf_loadAPIFile(fileName: str):
    api = ''
    try:
        with open(fileName, 'r') as file:
            api = file.read()
    except FileNotFoundError:
        print('File not found')
        return ''
    return api

def lf_loadCSV(fileName: str):
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

def pineconeService(oaAPI: str, pcAPI: str, csvData: list, pcServ: str, indexName: str, embModel: str, ):
    oa = openai.OpenAI(api_key=oaAPI)
    pc = pinecone.Pinecone(api_key=pcAPI)
    ps_defineIndex(pc=pc, indexName=indexName)
    index = ps_defineIndex(pc=pc, indexName=indexName, pcServ=pcServ)
    vectors = ps_addVectors(oa=oa, pc=pc, csvData=csvData, embModel=embModel)

def ps_defineIndex(pc: pinecone.Pinecone, indexName: str, pcServ: str):
    indexes = [index['name'] for index in pc.list_indexes()]
    if len(indexes) == 0 or indexName not in indexes:
        pc.create_index(
            name=indexName,
            dimension=3072,
            metric='cosine',
            spec=pinecone.ServerlessSpec(
                cloud='aws',
                region='us-east-1'
            )
        )
    return pc.Index(name=indexName, host=pcServ)

def ps_addVectors(oa: openai.OpenAI, pc: pinecone.Pinecone, csvData: list, embModel: str):
    vectors = []
    for entry in csvData:
        try:
            vector = {
                'id': str(entry['id']),
                'values': ps_av_generateEmbedding(oa=oa, content=entry['content'], embModel=embModel),
                'metadata': {
                    'title': entry['title']
                }
            }
            vectors.append(vector)
        except AttributeError as e:
            print('Could not complete vector assignment:', e)
    return vectors

def ps_av_generateEmbedding(oa: openai.OpenAI, content: str, embModel: str):
    try:
        res = oa.embeddings.create(input=content, model=embModel)
        embedding = res['data'][0]['embedding']
        print(f"Generated embedding of length {len(embedding)}")
        return embedding
    except Exception as e:
        print(f"Error generating embedding: {e}")
        return None

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