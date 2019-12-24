#!/usr/bin/env python3

import argparse
import pymongo
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
from pprint import pprint

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', required=True, help='Destination IP.')
    parser.add_argument('-p', type=int, default='27017', help='Destination Port (default: 27017).')
    args = parser.parse_args()

    if args.d and args.p:
        mongoConnect(args.d,args.p)

def mongoConnect(d,p):
    '''
    mongoConnect takes the destination and port and initiates the mongo client connection.
    '''

    print(f'Connecting to {d}:{p}')
    global mongoConnection
    mongoConnection = MongoClient(d, p,maxPoolSize=50)
    
    try:
        info = mongoConnection.server_info()
        getMongoDatabases()

    except ServerSelectionTimeoutError:
        print('Server is not responding.')

def getMongoDatabases():
    '''
    getMongoDatabases takes the client connection above and enumerates the visible database names.
    '''
    
    global mongo_dbnames
    mongo_dbnames = list(mongoConnection.list_database_names())

    print('\nThe following Databases\' have been identified:\n')

    for i in range(len(mongo_dbnames)):
        print('\t- %s' % mongo_dbnames[i])
        i+=1

    if len(mongo_dbnames) >= 1:
        db_selection = input('\nEnter a db name to get collection info: ')
        if db_selection:
            getMongoCollections(db_selection)
    else:
        print("No Databases Identified.")
        exit()

def getMongoCollections(db_selection):
    '''
    getMongoCollections takes our list of databases above and attempts to extract sample data from each.
    '''

    global db_connection
    global mongo_collections
    db_connection = mongoConnection[db_selection]
    
    print('\nThe following collections have been identified in %s.\n' % db_selection)

    mongo_collections = []
    for collection in db_connection.list_collection_names(include_system_collections=False):
        print('\t- %s' %collection)
        mongo_collections.append(collection)

    print('\nSample data from collections:\n')
    for coll in mongo_collections:
        cursor = db_connection[coll].find_one()
        
        if cursor is not None:
           print('%s\n%s\n' % (coll,cursor))

if __name__ == "__main__":main()
