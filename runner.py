import openai
import pandas as pd
import pinecone

def loadFiles(oaFile: str, pcFile: str, csv: pd.DataFrame):
    oaAPI = lf_loadAPIFile(oaFile)
    pcAPI = lf_loadAPIFile(pcFile)
    csvData = lf_loadCSV(csv)
    return oaAPI, pcAPI, csvData

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

def pineconeService(oaAPI: str, pcAPI: str, csvData: list, indexName: str, embModel: str, batchSize: int):
    oa = openai.OpenAI(api_key=oaAPI)
    pc = pinecone.Pinecone(api_key=pcAPI)
    index = ps_defineIndex(pc=pc, indexName=indexName)
    vectors = ps_addVectors(oa=oa, csvData=csvData, embModel=embModel)
    isUploaded = ps_uploadVectors(index=index, vectors=vectors, batchSize=batchSize)
    if isUploaded:
        print('Upload successful!')
    else:
        print('Upload unsuccessful :(')


def ps_defineIndex(pc: pinecone.Pinecone, indexName: str):
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
    return pc.Index(name=indexName)

def ps_addVectors(oa: openai.OpenAI, csvData: list, embModel: str):
    vectors = []
    #print(csvData)
    countErrors = 0
    for entry in csvData:
        #print('a', entry)
        if countErrors == 3:
            print('Error limit reached. Breaking operation.')
            break
        try:
            vector = {
                'id': str(entry['id']),
                'values': ps_av_generateEmbedding(oa=oa, content=entry['content'], embModel=embModel),
                'metadata': {
                    'title': entry['title']
                }
            }
            if len(vector['values']) == 0:
                countErrors += 1
                print('Due to error, embedding will not be added as vector.')
                print('Error count:', countErrors)
                continue
            vectors.append(vector)
            countErrors = 0
        except AttributeError as e:
            print('Could not complete vector assignment:', e)
            countErrors += 1
            print('Error count:', countErrors)
            
    return vectors

def ps_av_generateEmbedding(oa: openai.OpenAI, content: str, embModel: str):
    try:
        res = oa.embeddings.create(input=content, model=embModel)
        embedding = res.data[0].embedding
        print(f"Generated embedding of length {len(embedding)}")
        return embedding
    except Exception as e:
        print(f"Error generating embedding: {e}")
    return []

def ps_uploadVectors(index: pinecone.Index, vectors: list, batchSize: int):
    vectorsLength = len(vectors)
    batch = []
    couldUpload = True
    print('begin upload')
    if vectorsLength == 0:
        return False
    print('start..')
    for i in range(vectorsLength):
        batch.append(vectors[i])
        print('append', i)
        print(i + 1, '%', batchSize, (i + 1) % batchSize, (i + 1) % batchSize == 0)
        if (i + 1) % batchSize != 0 and i != vectorsLength - 1:
            continue
        print('batch', [vector['id'] for vector in batch])
        try:
            index.upsert(batch)
        except TypeError as e:
            print('Unable to upload due to the following:', e)
            couldUpload = False
        batch.clear()
    return couldUpload    

def main():
    print('Start project straightforward')
    print('Load files')
    oaFile = 'inputFiles/APIKey.txt'
    pcFile = 'inputFiles/pcAPIKey2.txt'
    csv = 'inputFiles/vectors-csv-2024-10-14.csv'
    oaAPI, pcAPI, csvData = loadFiles(oaFile, pcFile, csv)
    indexName = 'indextestsf2'
    embModel = 'text-embedding-3-large'
    batchSize = 2
    pineconeService(oaAPI=oaAPI, pcAPI=pcAPI, csvData=csvData, indexName=indexName, embModel=embModel, batchSize=batchSize)
    print('OpenAI API:', oaAPI)
    print('Pinecone API:', pcAPI)
    print('CSV:')
    print([row['id'] for row in csvData])

main()