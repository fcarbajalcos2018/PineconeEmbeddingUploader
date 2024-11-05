def userWelcome():
    print('Welcome to the Pinecone Embedding and Vector Uploader!')
    print('Press 1 to start a new upload')
    print('Press 2 to continue an upload from saved file')
    res = input('Your response: ')
    if res == 1:
        print('You selected (1) to start a new upload job')
        userInputNew()
    elif res == 2:
        print('You selected (2) to load an existing save file and continue upload job')
        userInputLoad()
    else:
        print('Your selection was INVALID. Please reattempt.')
        userWelcome()

def userInputNew():
    raise NotImplementedError()

def userInputLoad():
    raise NotImplementedError()

def main():
    print('Start project OOP')

main()