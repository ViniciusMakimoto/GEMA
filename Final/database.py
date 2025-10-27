from pymongo import MongoClient
from bson.objectid import ObjectId

class Database():
    def __init__(self, serverIP= "localhost", port= 27017):
        self.opened = False

        self.openClient(serverIP, port)
        self.setDatabase()
        self.setCollection()

        self.getAllItems()
        self.getItemByID()

    def openClient(self, serverIP, port):

        if self.opened:
            self.closeClient()

        self.client = MongoClient(serverIP, port)
        self.opened = True

    def closeClient(self):
        if not self.opened:
            return
        
        self.client.close()
        self.opened = False

    def setDatabase(self, databaseName = "Lab66"):
        # Obtem todos os bancos de dados disponíveis
        databaseNames = self.client.list_database_names()

        # Verifica se o banco de dados existe
        if not databaseName in databaseNames:
            print(f"O Banco de dados '{databaseName}' não existe.")
            return
        
        self.database = self.client[databaseName]
        print(f"Banco de dados '{databaseName}' conectado com sucesso.")

    def setCollection(self, collectionName = "Multimetros"):
        collectionNames = self.database.list_collection_names()

        # Verifica se o banco de dados existe
        if not collectionName in collectionNames:
            print(f"A coleção '{collectionName}' não existe.")
            return
        
        self.collection = self.database[collectionName]
        print(f"Coleção '{collectionName}' conectado com sucesso.")

    def getAllItems(self):
        items = self.collection.find({})

        for item in items:
            print(item)

        return items
    
    def getItemByID(self, id= 132):

        item = self.collection.find_one({"_id": id})

        print("-----------")
        print(item)

        return item


if __name__ == "__main__":
    database = Database()
