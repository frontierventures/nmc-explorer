import StringIO
import json
import pycurl
import urllib

c = pycurl.Curl()
c.setopt(c.USERPWD, 'test:test')
c.setopt(c.URL, 'http://127.0.0.1:8336/')
c.setopt(c.HTTPHEADER, ['content-type: text/plain'])

def summary():
    data = '{"jsonrpc": "1.0", "id":"curltest", "method": "getinfo", "params": [] }'
    #data = '{"jsonrpc": "1.0", "id":"curltest", "method": "name_list", "params": [] }'
    #data = '{"jsonrpc": "1.0", "id":"curltest", "method": "name_filter", "params": ["test"] }'
    
    b = StringIO.StringIO()
    c.setopt(c.WRITEFUNCTION, b.write)
    c.setopt(c.POSTFIELDS, data)
    c.perform()

    output = b.getvalue()
    output = json.loads(output)
    return output
        

def search(query):
    data = '{"jsonrpc": "1.0", "id":"curltest", "method": "name_filter", "params": ["%s"]}' % query

    print 
    print data
    #data = '{"jsonrpc": "1.0", "id":"curltest", "method": "name_list", "params": [] }'
    #data = '{"jsonrpc": "1.0", "id":"curltest", "method": "name_filter", "params": ["test"] }'
    
    b = StringIO.StringIO()
    c.setopt(c.WRITEFUNCTION, b.write)
    c.setopt(c.POSTFIELDS, data)
    c.perform()

    output = b.getvalue()
    output = json.loads(output)
    return output
        

def inventory():
    data = '{"jsonrpc": "1.0", "id":"curltest", "method": "name_list", "params": [] }'

    print 
    print data
    #data = '{"jsonrpc": "1.0", "id":"curltest", "method": "name_filter", "params": ["test"] }'
    
    b = StringIO.StringIO()
    c.setopt(c.WRITEFUNCTION, b.write)
    c.setopt(c.POSTFIELDS, data)
    c.perform()

    output = b.getvalue()
    output = json.loads(output)
    return output
        

def reserve(domain):
    data = '{"jsonrpc": "1.0", "id":"curltest", "method": "name_new", "params": ["d/%s"] }' % domain

    print 
    print data
    #data = '{"jsonrpc": "1.0", "id":"curltest", "method": "name_filter", "params": ["test"] }'
    
    b = StringIO.StringIO()
    c.setopt(c.WRITEFUNCTION, b.write)
    c.setopt(c.POSTFIELDS, data)
    c.perform()

    output = b.getvalue()
    output = json.loads(output)
    return output
        

def activate(name, rand1, rand2, value):
    data = '{"jsonrpc": "1.0", "id":"curltest", "method": "name_firstupdate", "params": ["d/%s", "%s", "%s", "%s"] }' % (str(name), str(rand2), str(rand1), str(value))

    print 
    print data
    #data = '{"jsonrpc": "1.0", "id":"curltest", "method": "name_filter", "params": ["test"] }'
    
    b = StringIO.StringIO()
    c.setopt(c.WRITEFUNCTION, b.write)
    c.setopt(c.POSTFIELDS, data)
    c.perform()

    output = b.getvalue()
    output = json.loads(output)
    return output
        

def update(name, record):
    record = json.dumps(record)
    data = '{"jsonrpc": "1.0", "id":"curltest", "method": "name_update", "params": ["d/%s", %s] }' % (str(name), record)
    
    print 
    print data
    
    b = StringIO.StringIO()
    c.setopt(c.WRITEFUNCTION, b.write)
    #c.setopt(c.POST, 1)
    c.setopt(c.POSTFIELDS, data)
    c.perform()

    output = b.getvalue()
    output = json.loads(output)
    return output
    
#    try:
#        c.perform()
#        output = b.getvalue()
#        output = json.loads(output)
#        
#        #print output
#        #print output['result']['blocks']
#    
#    except pycurl.error, error:
#        errno, errstr = error
#        print errno, errstr
#
#    return output
