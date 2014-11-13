#! /usr/bin/env python

"""
The MIT License (MIT)

Copyright (c) 2014 Jaan Janesmae

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

"""

import getopt
import sys
import requests
import json

# !!! Very important constants for the script !!!
# idea: maybe in the future I'll add the conversation id as a system argument
EMAIL = ""
PWD = ""
CONV_ID = ""

# API Location
API = "https://fleep.io/api/"

#--------------------------------------------------#

# Usage help
def usage():
    print 'USAGE: post_via_fleep_api.py -m "<message>"'
    sys.exit()
    
def config():
    print 'Script is not properly configured!'
    sys.exit()
 
# function for posting to fleep via API 
def post_via_fleep_api(message):
    if not message:
        usage()
        
    r = requests.post(API + "account/login",
            headers = {"Content-Type": "application/json"},
            data = json.dumps({"email": EMAIL,"password": PWD})
    )
    r.raise_for_status()      # break, in case we made a bad request
    TICKET = r.json()["ticket"]
    TOKEN = r.cookies["token_id"]
    
    # API send message
    r = requests.post(API + "message/send/" + CONV_ID,
                cookies = {"token_id": TOKEN},
                headers = {"Content-Type": "application/json"},
                data = json.dumps({
                    "message": message,
                    "ticket": TICKET}))
    r.raise_for_status()
    print 'Success'
    sys.exit()

def main(argv):
    message = ''
    if not EMAIL or not PWD or not CONV_ID:
        config()
    
    try:
        opts, args = getopt.getopt(argv, "m:h", ["help", "message="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt in ("-m", "--message"):
            message = arg
    
    post_via_fleep_api(message)

if __name__ == "__main__":
    main(sys.argv[1:])