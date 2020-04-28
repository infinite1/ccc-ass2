import couchdb

s = couchdb.Server('http://admin:000121@127.0.0.1:5984/')

db=s.create('docs')

db={
    'id':12354,
    'contents':'hi'
}