import requests
import json
import html
from flask_cors import CORS, cross_origin
from flask import Flask, render_template, request, url_for, jsonify
app = Flask(__name__)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

PRODUCTION = False

@app.route("/registerCertificate", methods=['POST'])
@cross_origin()
def registerCertificate():


    studentName = html.escape(request.json['student-name'])
    # studentName = "\"" + studentName + "\""
    certifyingAutority = html.escape(request.json['certifying-authority'])
    # certifyingAutority = "\"" + certifyingAutority + "\""
    extras = request.json['extras']

    contract = construct_contract(studentName, certifyingAutority)

    file = open('./src/program-c/src/incryptix/incryptix.c', 'w')
    file.write(contract)
    file.close()

    program_id = deploy_contract()

    # add to DB as well
    result = add_to_DB(program_id['result'], studentName, certifyingAutority, extras)
    print(result)


    return program_id

@app.route("/help", methods=['GET'])
@cross_origin()
def help():

    help_text = """
        <html>
            <body>
                <p>send a POST request to /registerCertificate/ with student-name and certifying-authority in the body as a JSON.</p>

                <p>The API will return the program id of the deployed certificate</p>
            </body>
        </html>
    """


    return help_text

def construct_contract(studentName, certifyingAutority):

    template_file = open("./degree_template.c", "r", encoding="utf-8")

    contract = template_file.read()

    contract = contract.replace("STUDENTNAME", studentName)
    contract = contract.replace("CERTIFYINGAUTORITY", certifyingAutority)

    return contract

def deploy_contract():

    # import os
    # os.system("npm run build:program-c & solana program deploy /media/New_Volume_D/workspaces/workspace-ethereum/solana-dapps/youngblob-solana-core/dist/program/helloworld.so")
    import subprocess
    import os

    if PRODUCTION:
        os.chdir('/home/p_s_obheroi/incryptix/solana-deploy/')

    try:
        result = subprocess.getoutput('rm -r ./dist')
    except:
        pass

    if PRODUCTION:
        result = subprocess.getoutput('V=1 make -C ./src/program-c helloworld')
    else:
        result = subprocess.getoutput('npm run build:program-c')

    # V=1 make -C /home/p_s_obheroi/incryptix/solana-deploy/src/program-c helloworld
    result = subprocess.getoutput('solana program deploy ./dist/program/helloworld.so').split('\n')[0]
    program_id = result.split(' ')[2]

    # if len(program_id) != 44:
    #     status_code = 400
    # else:
    #     status_code = 200
    status_code = 200

    return {"result": program_id, "status": status_code}

def add_to_DB(program_id, studentName, certifyingAutority, extras):

    #studentName = studentName.split('"')[1]
    #certifyingAutority = certifyingAutority.split('"')[1]

    url = "https://proxy.incryptix.workers.dev/v1/add/"+program_id+"/"
    myobj = json.dumps({"studentName": studentName, "certifyingAutority": certifyingAutority, "isCertified": False, "extras": extras})
    headers = {"Content-Type": "application/json", "X-Global-Auth": "parmurocks"}

    x = requests.post(url, headers=headers, data = myobj)

    return x
