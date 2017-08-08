#!/usr/bin/python
# __author__ = 'Kuldeep'

"""Module for interaction with SalesForce """

import requests
import json

""" New instance per test case """
# I integrated with Robot Framework, hence scope defined.
# You can skip this and set scope as per your test suite.
ROBOT_LIBRARY_SCOPE = 'TEST SUITE'

class SalesForceInterface:
    """ Class provides various methods for interaction with Sales Force   """

    USERNAME     = "<your_account_details>"
    PASSWORD     = "<SF_API_token>"
    LOGINURL     = "https://test.salesforce.com"
    GRANTSERVICE = "/services/oauth2/token?grant_type=password"
    CLIENTID     = "3MVG9Iu66FKeHhIPUh.2_RuT5HrlYu1xrfcUycMJzQcpy8F0BtB6irCRRAmU91iPgHTwaOFzsLhGnFYTmK5x3" # will find this detail in your SF a/c
    CLIENTSECRET = "8925253901379069246" # will find this detail in your SF a/c

    def __init__(self):
        """
        | Library | SalesForceInterface |
        """
        self.salesforce_url = self.LOGINURL + self.GRANTSERVICE + \
                              "&client_id=" + self.CLIENTID + \
                              "&client_secret=" + self.CLIENTSECRET + \
                              "&username=" + self.USERNAME + \
                              "&password=" + self.PASSWORD


        try:
            r = requests.post(self.salesforce_url)
            response_json = json.loads(r.content)
            self.instance_url = response_json['instance_url']
            self.access_token = response_json['access_token']
        except Exception :
            print '*INFO* Error Connecting salesforce ', r.content


    def get_account_details(self, account_id):
        """ get all entried for required id from salesforce"""
        self.userinfo = {}
        local_headers = {'Content-Type': 'application/json', 'Authorization': 'OAuth %s' % self.access_token}

        account_detail_url = self.instance_url + '/services/data/v20.0/sobjects/Account/' + account_id

        resp = requests.get(account_detail_url, headers=local_headers)

        if resp.ok:
            response_json = json.loads(resp.content)
            self.userinfo['username'] = response_json['Name']

        return self.userinfo

    def delete_salesforce_account(self, account_id_list):
        """ delete account from salesforce"""

        local_headers = {'Content-Type': 'application/json', 'Authorization': 'OAuth %s' % self.access_token}

        for each in account_id_list:
            account_detail_url = self.instance_url + '/services/data/v20.0/sobjects/Account/' + each
            try:
                resp = requests.delete(account_detail_url, headers=local_headers)
                assert resp.ok == True
            except:
                print "*INFO* Error deleting salesforce account %s Please delete manually"
        

if __name__=='__main__':
    SF = SalesForceInterface()
    account = SF.get_account_details('001R000000pgUWi')
    print account

    
                          
        
        
        

