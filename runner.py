from typing import Any
from controllers.mainUI import MainUI

def main():
    print('Start project OOP')
    ui = MainUI()
    ui.welcome()
    ui.loadOrNew()
    ui.defineIndexEmbeddings()
    ui.addVectors()
    ui.uploadVectors()

main()