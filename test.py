#!/usr/bin/python
# -*- coding:utf-8 -*-
import httplib2
import logging
import time
from apiclient.discovery import build
from oauth2client.client import SignedJwtAssertionCredentials
import pprint
import json
import os
import os.path
_dir = os.path.dirname(os.path.abspath(__file__))
conf=json.load(open(_dir+os.sep+'config.json'))

class BQC(object):
    def __init__(self):
        f = file(conf['KEYFILE'], 'rb')
        self.key = f.read()
        f.close()
        self.projectId=conf['PROJECT_NUMBER']
        self.email=conf['SERVICE_ACCOUNT_EMAIL']
    def _credential(self):
        credentials = SignedJwtAssertionCredentials(
            self.email,
            self.key,
            scope='https://www.googleapis.com/auth/bigquery')

        http = httplib2.Http()
        http = credentials.authorize(http)

        service = build('bigquery', 'v2')
        return http,service

    def datalist(self,service,http):
        datasets = service.datasets()
        response = datasets.list(projectId=self.projectId).execute(http)
        print('Dataset list:\n')
        for dataset in response['datasets']:
            print("%s\n" % dataset['id'])

    def show_result(self,result):
        #pprint.pprint(result)
        print 'Query Results:'
        for row in result['rows']:
            result_row = []
            for field in row['f']:
                if field['v']:
                    result_row.append(field['v'])
            print ('\t').join(result_row)



    def sync_method(self,service,http):
        q='SELECT *  FROM [nicodata_test.videoinfo] WHERE title like "%{}%" LIMIT 10;'.format(u'ボカロ'.encode('utf-8'))
        print q
        #q='SELECT TOP(title, 30) as title, COUNT(*) as revision_count FROM [publicdata:samples.wikipedia] WHERE wp_namespace = 0;'
        query_request=service.jobs()
        query_data={'query':q}
        query_response = query_request.query(projectId=self.projectId,
                                             body=query_data).execute(http)
        return query_response
  
    def async_method(self,service,http):
        q='SELECT *  FROM [nicodata_test.videoinfo] WHERE title like "%{}%" LIMIT 90;'.format(u'ボカロ'.encode('utf-8'))
        q='SELECT *  FROM [nicodata_test.comment_data] WHERE comment like "%{}%" LIMIT 90;'.format(u'ボカロ'.encode('utf-8'))

        print q
        query_request=service.jobs()
        query_data={'query':q}
        query_data = {
            'configuration': {
                'query': {
                    'query': q,
                    }
                }
            }

        ft=time.time()
        insertResponse = query_request.insert(projectId=self.projectId,
                                         body=query_data).execute(http)
        print 'start query diff={}'.format(time.time()-ft)
        while True:
            print 'stat_get'
            ft2=time.time()
            status = query_request.get(projectId=self.projectId, jobId=insertResponse['jobReference']['jobId']).execute(http)
            print 'end get diff={}'.format(time.time()-ft2)
            currentStatus = status['status']['state']
            if 'DONE' == currentStatus:
                print 'sql done'
                break
            else:
                print 'Waiting for the query to complete...'
                print 'Current status: ' + currentStatus
                print time.ctime()
                time.sleep(0.1)
        currentRow = 0
        queryReply = query_request.getQueryResults(
            projectId=self.projectId,
            jobId=insertResponse['jobReference']['jobId'],
            startIndex=currentRow).execute(http)
        
        while(('rows' in queryReply) and currentRow < queryReply['totalRows']):
            self.show_result(queryReply)
            currentRow += len(queryReply['rows'])
            queryReply = query_request.getQueryResults(
                projectId=self.projectId,
                jobId=queryReply['jobReference']['jobId'],
                startIndex=currentRow).execute(http)

        print currentRow 
    def show(self):
        http,service=self._credential()
        self.datalist(service,http)
        result=self.sync_method(service,http)
        self.show_result(result)
        result=self.async_method(service,http)

def main():
    bqc=BQC()
    bqc.show()
    pass
if __name__=='__main__':main()
