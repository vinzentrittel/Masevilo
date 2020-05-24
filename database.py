import json
import asyncio
import csv

class database:
""" contains a dictionary for storing location json data.
Consisting of langitude and longitude.
 """
    def __init__(self):
        self.db = {}
        asyncio.run(self.start())

    async def readDB(self): """ reads a json file as dictionary"""
        with open("data.json", "r") as json_file:
            data = json.load(json_file)
        return data

    async def writeDB(self,db): """ writes a dictionary to a json file"""
        #with open("data.json", "w") as db:
        out_file = open("data.json", "w")  
        print(out_file)
        print('writedb')
        json.dump(self.db, out_file,sort_keys=True,  indent=4)
        return 

    async def start(self):""" initializes the database"""
        currdb = await self.readDB()
        print(currdb)
        self.setDB(currdb)
        print( self.db )

        """ appends and element into the database dictionary.
The dictionary gets sorted before saving it as json."""
    async def insertElement(self, insertDict):
        langitude = insertDict[list(insertDict.keys())[0]]
        longitude = insertDict[list(insertDict.keys())[1]]
         
        self.db.update({str(langitude)+"_"+str(longitude):insertDict})
        await self.writeDB(self.db)

""" Gets an element by ID from the dictionary database."""
    async def returnElement(self, idnum):
        db = await self.readDB()
        if(idnum in db):
            return db[idnum]
        return {}

    def setDB(self, db):
        self.db = db
        return
    def getDB(self):
        return self.db
def getLoc():
""" reads a csv database of cities and converts it to json"""
    with open ('worldcities.csv', 'r') as source:
        rdr= csv.reader( source )
        with open("result.csv","w") as result:
            wtr= csv.writer( result )
            for r in rdr:
                wtr.writerow( (  r[2], r[3]) )
    csvfile = open('result.csv', 'r')
    jsonfile = open('file.json', 'w')

    fieldnames = ( "latitude","longitude")
    reader = csv.DictReader( csvfile, fieldnames)
    jsonfile.write('{')
    for   row in  reader:
        lat = row[list(row.keys())[0]]
        long = row[list(row.keys())[1]]
        jsonfile.write('"' +str(lat)+'_'+str(long)+ '"'+' : ')
        jsonfile.write( '{ "latitude":' + str(lat) + ' , "longitude" : '+str(long)+'}')
        #json.dump(row, jsonfile)
        jsonfile.write('\n,')
    jsonfile.write('}')
    
    return
    
if __name__ == '__main__':
    newdb = database()
    insertDict  = {"latitude":-200, "longitude":100}
    asyncio.run(newdb.insertElement(insertDict))
    getLoc()
#{"4":{"latitude":-200, "longitude":100}}



 