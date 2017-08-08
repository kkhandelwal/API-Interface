#!/usr/bin/python
# __author__ = 'Kuldeep'

"""Module for interaction with MongoDB """

from pymongo import MongoClient
import json

# New instance per test case
ROBOT_LIBRARY_SCOPE = 'TEST CASE'


class MongoDBInterface:
    """ Class provides various methods for interaction with DB   """
    
    def __init__(self, DB_HOST, DB_PORT=None,db_name='MyFitbitRecords'):
        """DB_HOST: Just the host name or IP
        
     
        | Library | MongoDBInterface | '127.00.000.001' | 27017 |
        check_cert = False |
        """
        self.DB_HOST = DB_HOST
        self.DB_PORT = DB_PORT
        self.DB_NAME = db_name
        self.mongo = MongoClient(self.DB_HOST, self.DB_PORT)
        #self.mongo = pymongo.Connection(self.DB_HOST)
        self.mongo_db = self.mongo.self.DB_NAME
        #print self.mongo_db
        self.mongo_db.authenticate('QaDevUser','QaDevUser', mechanism='MONGODB-CR') 

    def get_IOS_app_token(self, collection_name, appname):
        
        """ get IOS registered app token """
        app_collection = self.mongo_db[collection_name]
        app = list(app_collection.find({"appName": appname}))
        return app[0]['appTokenKey']

   
    def get_random_app_token(self, collection_name, appname):

        """ get random registered app token """
        app_collection = self.mongo_db[collection_name]
        return app_collection.find_one()['appTokenKey']

    def get_random_registered_user(self, collection_name, appname):

        """ get random registered app token """
        user_collection = self.mongo_db[collection_name]
        return user_collection.find_one()['emailId']
    
    def get_user_details(self, user_address, collection_name):
        user_collection = self.mongo_db[collection_name]
        print '*INFO* type of email', type(user_address)
        try:
            users = user_collection.find({"emailId": user_address.lower()})
            self.firstName = users[0]['firstName']
            self.lastName = users[0]['lastName']
            self.cortexId = users[0]['cortexId']
            self.userName = users[0]['userName']
            self.emailId = users[0]['emailId']
            self.signinMode = users[0]['signinMode']
            self.userAppTokenKey = users[0]['userAppTokenKey']
            self.gender = users[0].get('gender')
            return  {'firstName' : self.firstName, 'lastName' : self.lastName,
                     'cortexId' : self.cortexId, 'userName' : self.userName,
                     'signinMode' : self.signinMode, 'emailId' : self.emailId,
                     'userAppTokenKey' : self.userAppTokenKey,
                     'gender' : self.gender}
        except IndexError:
            return '*INFO* User does not exist in MongoDB ', user_address.lower()

    def delete_registered_users_from_db(self, user_list, collection_name):
        user_collection = self.mongo_db[collection_name]
        for each in user_list:
            user_collection.remove({"emailId" : each.lower()})

    def get_playback_pattern_for_songs_played(self, tech_desc,
                                          collection_name='Playlist'):
        wave_collection = self.mongo_db[collection_name]
        wave = list(wave_collection.find({"technical_description": tech_desc,
                                          'deleted' : None}))
        return wave[0]['playback_patterns']


    def update_prodflag(self, tech_desc, collection_name):
        """ Update operations in Mongo using set operation """
        vibe_collection = self.mongo_db[collection_name]
        vibe = vibe_collection.update({"technical_description": tech_desc},
                                      {"$set": {"prodFlag" : "Y"}})
        return vibe
        

    def delete_record_permanently(self, tech_desc, collection_name):
        record_collection = self.mongo_db[collection_name]
        success = record_collection.remove({"technical_description": tech_desc})
        return success    

if __name__=='__main__':
    MONGO = MongoDBInterface('54.183.109.151')
    
                                      
    song = MONGO.get_playback_pattern_for_songs('Aerobics')
    user = MONGO.get_user_details('AUTOUser0001441370722@auto.com')
    MONGO.delete_registered_users_from_db(['AUTOUser0001441370722@auto.com'])
    
    ios_token = MONGO.get_random_app_token()
    print ios_token

    import sched, time
    MONGO = MongoDBInterface('127.0.00.12', 27017)
    s = sched.scheduler(time.time, time.sleep)
    def do_something(sc): 
        print "Doing stuff..."
        new = MONGO.update_prodflag()
        print new
        sc.enter(63, 1, do_something, (sc,))

    s.enter(63, 1, do_something, (s,))
    s.run()
                          
        
        
        

