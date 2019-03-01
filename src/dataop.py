import json

data_file = open('data.json',"r")
print data_file
data = json.loads(data_file.read())
data_file.close()
print(data)


def update():
    jsondata = json.dumps(data)
    data_file = open('data.json',"w")
    data_file.write(jsondata)
    data_file.close()


def add(key,value):
    data[key] = value
    print data
    update()


def delete(key):
    del data[key]
    update()


def search(key):
    print "data:"+str(data)
    return data[key]
