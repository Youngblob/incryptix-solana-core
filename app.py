import requests
import json
import html
import subprocess
import os
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

    result = deploy_certificate()
    programId = result['result']
    status_code = result['status']
    extras["storageAccounts"] = result['storageAccounts']
    extras["programExecutionTXHash"] = result['programExecutionTXHash']

    # add to DB as well
    print(add_to_DB(programId, studentName, certifyingAutority, extras))


    return {
        "result": programId,
        "status": status_code,
        "storageAccounts": result['storageAccounts'],
        "programExecutionTXHash": result['programExecutionTXHash']
    }

@app.route("/getCertificate", methods=['GET'])
@cross_origin()
def getCertificate():

    programId                           = html.escape(request.json['programId'])
    studentName_storage_pubkey          = html.escape(request.json['programId'])
    certifyingAutority_storage_pubkey   = html.escape(request.json['programId'])
    isCertified_storage_pubkey          = html.escape(request.json['programId'])

    result = subprocess.getoutput(f"node web3_get_data.js {programId} {studentName_storage_pubkey} {certifyingAutority_storage_pubkey} {isCertified_storage_pubkey}")

    return result


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

# ToDo: Move it to a qeueu architecture
def deploy_certificate():

    result = subprocess.getoutput('rm -r ./dist')
    result = subprocess.getoutput('npm run build:program-c')
    result = subprocess.getoutput('solana program deploy ./dist/program/incryptix.so').split('\n')[0]
    programId = result.split(' ')[2]

    # validate tx and create storage accounts
    studentName_storage_pubkey = web3_create_accounts(programId)
    certifyingAutority_storage_pubkey = web3_create_accounts(programId)
    isCertified_storage_pubkey = web3_create_accounts(programId)

    print(programId)
    print(studentName_storage_pubkey)
    print(certifyingAutority_storage_pubkey)
    print(isCertified_storage_pubkey)

    programExecutionTXHash = web3_execute_program(programId, studentName_storage_pubkey, certifyingAutority_storage_pubkey, isCertified_storage_pubkey)

    # if len(programId) != 44:
    #     status_code = 400
    # else:
    #     status_code = 200
    status_code = 200

    return {
        "result": programId,
        "status": status_code,
        "storageAccounts": {
            "studentName": studentName_storage_pubkey,
            "certifyingAutority": certifyingAutority_storage_pubkey,
            "isCertified": isCertified_storage_pubkey
        },
        "programExecutionTXHash": programExecutionTXHash
    }

def web3_create_accounts(programId):

    result = subprocess.getoutput('node web3_create_accounts.js '+programId)

    return result

def web3_execute_program(programId, studentName_storage_pubkey, certifyingAutority_storage_pubkey, isCertified_storage_pubkey):

    result = subprocess.getoutput(f"node web3_create_accounts.js {programId} {studentName_storage_pubkey} {certifyingAutority_storage_pubkey} {isCertified_storage_pubkey}")

    return result

# just in case
def add_to_DB(programId, studentName, certifyingAutority, extras):

    url = "https://proxy.incryptix.workers.dev/v1/add/"+programId+"/"
    myobj = json.dumps({"studentName": studentName, "certifyingAutority": certifyingAutority, "isCertified": False, "extras": extras})
    headers = {"Content-Type": "application/json", "X-Global-Auth": "parmurocks"}

    x = requests.post(url, headers=headers, data = myobj)

    return x
