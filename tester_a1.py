import argparse
import requests 
import os

def isgoodipv4(s):
    digs_only = s.replace('http://', '')
    pieces = digs_only.split('.')
    if len(pieces) != 4: return False
    try: return all(0<=int(p)<256 for p in pieces)
    except ValueError: return False


parser = argparse.ArgumentParser()
parser.add_argument(
    "--ip_addr", help="the IP of your web app, e.g. http://34.228.7.61", type=str, required=True)
args = parser.parse_args()

print("--------------------------------------------------------------------")
print("ECE1779 auto-tester A1")
print("--------------------------------------------------------------------")
print("checking your web app IP...")
if not args.ip_addr.startswith('http://'):
    exit('error: your IP address should starts with "http://"')
elif not isgoodipv4(args.ip_addr):
    exit('please use a valid IPv4 address with the correct format, e.g. http://34.228.7.61')

# link set up 
url = args.ip_addr + ':5000/api'
print("tester will be run on: {}".format(url))
score = 0


# test 1: delete_all
print("--------------------------------------------------------------------")
print("test 1: delete all keys & values from the application")
test_1_flag = True
try:
    response = requests.post(url+"/delete_all")
except:
    print("error in test 1: could not post /delete_all to your web app")
    print("check the web app connection, IP, port, API endpoint path, etc.")
    test_1_flag = False

if test_1_flag:
    try:
        jsonResponse = response.json()
    except: 
        print("error in test 1: your response cannot be represented in JSON format")
    try:
        if jsonResponse["success"] == "true":
            score += 1
        else: 
            print('error in test 1: /delete_all operation should return {"success": "true"}')
            print("your response: ")
            print(jsonResponse)
            print("")
    except: 
        print('error in test 1: access failure on ["success"] of the post response')
        print("")


# test 2: list_keys 
print("--------------------------------------------------------------------")
print("test 2: list_keys without any upload")
test_2_flag = True
try:
    response = requests.post(url+"/list_keys")
except:
    print("error in test 2: could not post /delete_all to your web app")
    print("check the web app connection, IP, port, API endpoint path, etc.")
    test_2_flag = False 

if test_2_flag:
    try:
        jsonResponse = response.json()
    except: 
        print("error in test 2: your response cannot be represented in JSON format")

    try:
        if jsonResponse["success"] == "true" and jsonResponse["keys"] == []:
            score += 1
        else:
            print("""error in test 2: /list_keys operation should return 
                {
                    "success": "true",
                    "keys": []
                }""")
            print("your response: ")
            print(jsonResponse)
            print("")
    except: 
        print('error in test 2: access failure on ["success"]/["key"] of the post response') 
        print("")
    

# test 3: upload
print("--------------------------------------------------------------------")
print("test 3: upload 2 images")   
filenames = ['1.jpeg', '2.png']
work_dir = os.path.abspath(os.getcwd())

try: 
    file_1 = {'file': open(work_dir+'/images/'+filenames[0],'rb')}
except:
    print("script failure: unable to open the image file. Please contact TA at wenjun.qiu@mail.utoronto.ca")

test_3_flag_1 = True
try:
    response = requests.post(url+"/upload", files=file_1, data={'key': 'test_1'})
except:
    print("error in test 3-1: could not post /delete_all to your web app")
    print("check the web app connection, IP, port, API endpoint path, etc.")
    test_3_flag_1 = False 

if test_3_flag_1:
    try: 
        jsonResponse = response.json()
    except:
        print("error in test 3-1: your response cannot be represented in JSON format")

    try:
        if jsonResponse["success"] == "true" and jsonResponse["key"] == ['test_1']:
            score += 1
        else:

            print("""error in test 3-1: /upload operation should return 
                    {
                        "success": "true",
                        "key": [test_1]
                    }""")
            print("your response: ")
            print(jsonResponse)
            print("")
    except:
        print('error in test 3-1: access failure on ["success"]/["key"] of the post response')
        print("")

try:
    file_2 = {'file': open(work_dir+'/images/'+filenames[1],'rb')}
except:
    print("script failure: unable to open the image file. Please contact TA at wenjun.qiu@mail.utoronto.ca")

test_3_flag_2 = True
try:
    response = requests.post(url+"/upload", files=file_2,
                       data={'key': 'test_2'})
except:
    print("error in test 3-2: could not post /delete_all to your web app")
    print("check the web app connection, IP, port, API endpoint path, etc.")
    test_3_flag_2 = False 

if test_3_flag_2:
    try: 
        jsonResponse = response.json()
    except:
        print("error in test 3-2: your response cannot be represented in JSON format")

    try:
        if jsonResponse["success"] == "true" and jsonResponse["key"] == ['test_2']:
            score += 1
        else:

            print("""error in test 3-2: /upload operation should return 
                    {
                        "success": "true",
                        "key": [test_2]
                    }""")
            print("your response: ")
            print(jsonResponse)
            print("")
    except:
        print('error in test 3-2: access failure on ["success"]/["key"] of the post response')
        print("")



# test 4: retrieval 
print("--------------------------------------------------------------------")
print("test 4: retrieve 1 image")    

test_4_flag = True
try:
    response = requests.post(url+"/key/test_1")
except:
    print("error in test 4: could not post /key/test_1 to your web app")
    print("check the web app connection, IP, port, API endpoint path, etc.")
    test_4_flag = False 

if test_4_flag: 
    try: 
        jsonResponse = response.json()
    except:
        print("error in test 4: your response cannot be represented in JSON format")
    try: 
        if jsonResponse["success"] == "true" and jsonResponse["key"] == ['test_1'] and jsonResponse["content"] != None:
            score += 1
        else:
            print("""error in test 4: /key/test_1 operation should return 
                    {
                        "success": "true", 
                        "key" : [test_1],
                        "content" : file contents
                    }""")
            print("your response: ")
            print(jsonResponse)
            print("")
    except:
        print('error in test 4: access failure on ["success"]/["key"]/["content"] of the post response')
        print("")


print("--------------------------------------------------------------------")
print("tester total: {}/5".format(score))    








