'''
Created on 24/ott/2018

@author: f4b10
'''


from suds.client import Client as SudsClient

url = 'http://ebill.local:5000/io/client?wsdl'
client = SudsClient(url=url)#, cache=None)
# r = client.service.echo(str='hello world', cnt=3)
r = client.service.put_file("<xml>")
print r
