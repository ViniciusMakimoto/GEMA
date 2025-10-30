from pymongo import MongoClient
from bson.objectid import ObjectId

class Database():
    def __init__(self, serverIP= "localhost", port= 27017):
        self.opened = False
        self.hasDatabase = False
        self.hasCollection = False

        self.openClient(serverIP, port)
        self.setDatabase()
        self.setCollection()

    def openClient(self, serverIP, port):

        if self.opened:
            self.closeClient()
            
        self.client = MongoClient(serverIP, port)
        self.opened = True
        print("[Database] Conexão com MongoDB foi aberta")

    def closeClient(self):
        if not self.opened:
            return
        
        self.client.close()
        self.opened = False
        print("[Database] Conexão com MongoDB foi fechada")

    def setDatabase(self, databaseName = "Lab66"):
        # Obtem todos os bancos de dados disponíveis
        databaseNames = self.client.list_database_names()

        self.hasDatabase = databaseName in databaseNames

        # Verifica se o banco de dados existe
        if not self.hasDatabase:
            print(f"[Database] O Banco de dados '{databaseName}' não existe.")
            return
        
        self.database = self.client[databaseName]
        print(f"[Database] Banco de dados '{databaseName}' configurada com sucesso.")

    def setCollection(self, collectionName = "Multimetros"):
        collectionNames = self.database.list_collection_names()

        self.hasCollection = collectionName in collectionNames

        # Verifica se o banco de dados existe
        if not self.hasCollection:
            print(f"[Database] A coleção '{collectionName}' não existe.")
            return
        
        self.collection = self.database[collectionName]
        print(f"[Database] Coleção '{collectionName}' configurada com sucesso.")

    def getAllItems(self):
        if not self.hasCollection:
            print(f"[Database] Impossível obter Items - Coleção não foi definida")
            return 

        return self.collection.find({})
    
    def getItemByID(self, id= 132):

        if not self.hasCollection:
            print(f"[Database] Impossível obter Item - Coleção não foi definida")
            return 
 
        return self.collection.find_one({"_id": id})
    
    def updateItemByID(self, id= 132, updateList= {}):
        if not self.hasCollection:
            print(f"[Database] Impossível atualizar Item - Coleção não foi definida")
            return False

        result = self.collection.update_one({"_id": id}, {"$set": updateList})

        return result.acknowledged

if __name__ == "__main__":
    database = Database()

    #items = database.getAllItems()

    #for item in items:
    #    print(item)

    item = database.getItemByID()
    
    print("-----------")
    print(item)

    database.updateItemByID(updateList={"status": "Manutenção"})

    item = database.getItemByID()
    
    print("-----------")
    print(item)
