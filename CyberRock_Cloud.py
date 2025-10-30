import random, sys, time, requests
from functools import reduce
from math import log,ceil

environmentURL = 'https://device-api.sandbox.sandgrain.io/'

cyberrock_device_login =                     environmentURL + 'api/auth/deviceLogin'

cyberrock_device_tokenauth_requestcw =       environmentURL + 'api/device/requestCW'
cyberrock_device_tokenauth_replyrw =         environmentURL + 'api/device/replyRW'
cyberrock_device_tokenauth_checkstatus =     environmentURL + 'api/device/checkAuthStatus'

cyberrock_device_tokenauthEK_requestcw =     environmentURL + 'api/device/EKrequestCW'
cyberrock_device_tokenauthEK_replyrw =       environmentURL + 'api/device/EKreplyRW'
cyberrock_device_tokenauthEK_checkstatus =   environmentURL + 'api/device/EKCheckAuthStatus'

cyberrock_device_hostauth_requestcw =        environmentURL + 'api/device/requestHostAuth'
cyberrock_device_hostauth_checkstatus =      environmentURL + 'api/device/checkRequestHostAuthStatus'

cyberrock_device_priorityhostauth =          environmentURL + 'api/device/priorityHostAuth'

cyberrock_device_hostauthEK_requestcw =      environmentURL + 'api/device/EKrequestHostAuth'
cyberrock_device_hostauthEK_checkstatus =    environmentURL + 'api/device/EKcheckRequestHostAuthStatus'

cyberrock_device_EKpriorityhostauth =        environmentURL + 'api/device/EKpriorityHostAuth'

cyberrock_device_requestHRWtransactionid =   environmentURL + 'api/device/requestTransactionID'
cyberrock_device_requestHRW =                environmentURL + 'api/device/requestHRW'
cyberrock_device_requestHRWstatus =          environmentURL + 'api/device/checkRequestHRWStatus'

cyberrock_device_priorityrequestHRW =        environmentURL + 'api/device/priorityRequestHRW'

cyberrock_device_EKrequestHRWtransactionid = environmentURL + 'api/device/EKrequestTransactionID'
cyberrock_device_EKrequestHRW =              environmentURL + 'api/device/EKrequestHRW'
cyberrock_device_EKrequestHRWstatus =        environmentURL + 'api/device/EKcheckRequestHRWStatus'

cyberrock_device_EKpriorityrequestHRW =      environmentURL + 'api/device/EKpriorityRequestHRW'

cyberrock_tenant_login =   environmentURL + 'api/auth/tenantUserLogin'
cyberrock_tenant_claimid = environmentURL + 'api/tenantApi/claimId'

sleeptime = 0.3

#CyberRock calls
def do_device_login(cloudflaretokens, iotusername, iotpassword):

	print("Logging in to CyberRock IoT portal")

	response = requests.post(cyberrock_device_login,
	# headers={'accept: application/json', 'Content-Type: application/json'},
	 headers = cloudflaretokens,
	 data = {'username': iotusername, 'password': iotpassword},
	 )

	print(response.status_code)
	#print(response.json())
	print('')

	logindata = response.json()

	accesstoken = (logindata['accessToken'])
	iotid = (logindata['deviceId'])
#	iotid = (logindata['iotId'])

	return accesstoken, iotid

def do_device_tokenauth_requestcw(cloudflaretokens, accesstoken, TID, requestSignature):

	print("Retrieving CW from CyberRock")

	data_auth = cloudflaretokens | {'Authorization': 'Bearer ' + accesstoken}

	data_post = {"requestSignedResponse": requestSignature,
			"TID": TID
		    }

	response = requests.post(cyberrock_device_tokenauth_requestcw,
	# headers={'accept': 'application/json', 'Content-Type': 'application/json'},
	 headers = data_auth, json = data_post,
	 )
	 
	print(response.url)
	print(response.status_code)
	print(response.json())
	print('')

	cwdata = response.json()

	CW = cwdata['CW']
	transactionid = cwdata['transactionId']
	
	return CW, transactionid
	
def do_device_tokenauth_replyrw(cloudflaretokens, accesstoken, TID, CW, RW, transactionid, requestSignature):

	print("Submitting RW to CyberRock")
	
	data_auth = cloudflaretokens | {'Authorization': 'Bearer ' + accesstoken}

	data_post = {
		"requestSignedResponse": requestSignature,
		"TID": TID,
		"CW": CW,
		"RW": RW,
		"transactionId": transactionid	
			}

	response = requests.post(cyberrock_device_tokenauth_replyrw,
	# headers={'accept': 'application/json', 'Content-Type': 'application/json'},
	 headers = data_auth, json = data_post,
	 )
	 
	print(response.url)
	print(response.status_code)
	print(response.json())

	print('')
	
	cwdata = response.json()

	transactionid = cwdata['transactionId']
	
	return transactionid

def do_device_tokenauth_checkstatus(cloudflaretokens, accesstoken, transactionid, requestSignature):
	print("Retrieving result from CyberRock")

	data_auth = cloudflaretokens | {'Authorization': 'Bearer ' + accesstoken}

	authenticationresult = 'NOT_READY'
	
	params_post = {"transactionId": transactionid}
	
	data_post = {		 
		"requestSignedResponse": requestSignature}

	while (authenticationresult == 'NOT_READY'):
		
		time.sleep(sleeptime)
		
		response = requests.get(cyberrock_device_tokenauth_checkstatus,
		# headers={'accept': 'application/json', 'Content-Type': 'application/json'},
		 headers = data_auth, params = params_post, json = data_post,
		 )

		print(response.url)
		print(response.status_code)
		print(response.json())
		print('\n')
		
		responsedata = response.json()
		authenticationresult = responsedata['status']
		
	if (authenticationresult == 'CLAIM_ID'):	
		claimid = responsedata['claimId']
	else:
		claimid = ''
		
	return authenticationresult, claimid

def do_tenant_login(cloudflaretokens, tenantusername, tenantpassword):

	print("Logging in to CyberRock Tenant portal")

	response = requests.post(cyberrock_tenant_login,
	# headers={'accept: application/json', 'Content-Type: application/json'},
	 headers = cloudflaretokens,
	 data = {'email': tenantusername, 'password': tenantpassword},
	 )

	print(response.status_code)
	print(response.json())
	print('')

	logindata = response.json()

	tenantaccesstoken = (logindata['accessToken'])

	return tenantaccesstoken
	

def do_tenant_claimid(cloudflaretokens, tenantaccesstoken, claimid):

	print("Claiming ID in CyberRock Tenant portal")

	data_auth = cloudflaretokens | {'Authorization': 'Bearer ' + tenantaccesstoken}

	response = requests.post(cyberrock_tenant_claimid,
	# headers={'accept: application/json', 'Content-Type: application/json'},
	 headers = data_auth,
	 data = {'claimId': claimid}
	 )

	print(response.status_code)
	print(response.json())
	print('')

	responsedata = response.json()
	result = (responsedata['result'])

	return result
	
def do_device_priorityhostauth(cloudflaretokens, accesstoken, TID, HCW, HRW):

	print("Submitting HCW,HRW to CyberRock")
	
	data_auth = cloudflaretokens | {'Authorization': 'Bearer ' + accesstoken}

	data_post = {
		"TID": TID,
		"HCW": HCW,
		"HRW": HRW
		}

	print(HCW)
	print(HRW)

	response = requests.post(cyberrock_device_priorityhostauth,
	# headers={'accept': 'application/json', 'Content-Type': 'application/json'},
	headers = data_auth, data = data_post,
	)

	print(response.url)
	print(response.status_code)
	print(response.json())

	print('')
	
	responsedata = response.json()
	result = (responsedata['status'])

	return result

def do_device_requestHRWtransactionid(cloudflaretokens, accesstoken, TID, HCW):

	print("Requesting TransactionID from CyberRock")
	
	data_auth = cloudflaretokens | {'Authorization': 'Bearer ' + accesstoken}

	data_post = {
		"TID": TID,
		"HCW": HCW
		}

	response = requests.post(cyberrock_device_requestHRWtransactionid,
	# headers={'accept': 'application/json', 'Content-Type': 'application/json'},
	headers = data_auth, data = data_post,
	)

	print(response.url)
	print(response.status_code)
	print(response.json())

	print('')
	
	tiddata = response.json()

	transactionid = tiddata['transactionId']
	
	return transactionid


def do_device_requestHRW(cloudflaretokens, accesstoken, TID, HCW, transactionid):

	print("Submitting TID, HCW to CyberRock")
	
	data_auth = cloudflaretokens | {'Authorization': 'Bearer ' + accesstoken}

	data_post = {
		"TID": TID,
		"HCW": HCW,
		"transactionId": transactionid
		}

	response = requests.post(cyberrock_device_requestHRW,
	# headers={'accept': 'application/json', 'Content-Type': 'application/json'},
	headers = data_auth, data = data_post,
	)

	print(response.url)
	print(response.status_code)
	print(response.json())

	print('')
	
	tiddata = response.json()

	transactionid = tiddata['transactionId']
	
	return transactionid


def do_device_requestHRWstatus(cloudflaretokens, accesstoken, HRWtransactionID):

	print("Retrieving result from CyberRock")
	
	data_auth = cloudflaretokens | {'Authorization': 'Bearer ' + accesstoken}

	result = 'NOT_READY'

	while (result == 'NOT_READY'):
		
		time.sleep(sleeptime)
		
		response = requests.get(cyberrock_device_requestHRWstatus,
		# headers={'accept': 'application/json', 'Content-Type': 'application/json'},
		headers = data_auth, params = {"transactionId": HRWtransactionID},
		)

		print(response.url)
		print(response.status_code)
		print(response.json())

		print('')
			
		responsedata = response.json()
		result = responsedata['status']
		
	if (result == 'GENERATED_RW'):	
		hrw = responsedata['HRW']
	else:
		hrw = ''
			
	return result, hrw


def do_device_tokenauthEK_requestcw(cloudflaretokens, accesstoken, TID):

	print("Retrieving CW from CyberRock")

	data_auth = cloudflaretokens | {'Authorization': 'Bearer ' + accesstoken}

	data_post = {"TID": TID}

	response = requests.post(cyberrock_device_tokenauthEK_requestcw,
	# headers={'accept': 'application/json', 'Content-Type': 'application/json'},
	 headers = data_auth, data = data_post,
	 )
	 
	print(response.url)
	print(response.status_code)
	print(response.json())
	print('')

	cwdata = response.json()

	CW = cwdata['CW']
	transactionid = cwdata['transactionId']
	
	return CW, transactionid
	
def do_device_tokenauthEK_replyrw(cloudflaretokens, accesstoken, TID, CW, RW, transactionid):

	print("Submitting RW to CyberRock")
	
	data_auth = cloudflaretokens | {'Authorization': 'Bearer ' + accesstoken}

	data_post = {
		"TID": TID,
		"CW": CW,
		"RW": RW,
		"transactionId": transactionid	
			}

	response = requests.post(cyberrock_device_tokenauthEK_replyrw,
	# headers={'accept': 'application/json', 'Content-Type': 'application/json'},
	 headers = data_auth, data = data_post,
	 )
	 
	print(response.url)
	print(response.status_code)
	print(response.json())

	print('')
	
	cwdata = response.json()

	transactionid = cwdata['transactionId']
	
	return transactionid

def do_device_tokenauthEK_checkstatus(cloudflaretokens, accesstoken, transactionid):
	print("Retrieving result from CyberRock")

	data_auth = cloudflaretokens | {'Authorization': 'Bearer ' + accesstoken}

	authenticationresult = 'NOT_READY'

	while (authenticationresult == 'NOT_READY'):
		
		time.sleep(sleeptime)
		
		response = requests.get(cyberrock_device_tokenauthEK_checkstatus,
		# headers={'accept': 'application/json', 'Content-Type': 'application/json'},
		 headers = data_auth, params = {'transactionId': transactionid, "requestSignedResponse": "True"},
		 )

		print(response.url)
		print(response.status_code)
		print(response.json())
		print('\n')
		
		responsedata = response.json()
		authenticationresult = responsedata['status']
		
	ekresult = responsedata['EK']
		
	if (authenticationresult == 'CLAIM_ID'):	
		claimid = responsedata['claimId']
	else:
		claimid = ''
		
	return authenticationresult, claimid, ekresult


def do_device_EKpriorityhostauth(cloudflaretokens, accesstoken, TID, HCW, HRW):
    print("Submitting HCW,HRW to CyberRock")

    data_auth = cloudflaretokens | {'Authorization': 'Bearer ' + accesstoken}

    data_post = {
        "TID": TID,
        "HCW": HCW,
        "HRW": HRW
    }

    print(HCW)
    print(HRW)

    response = requests.post(cyberrock_device_EKpriorityhostauth,
                             # headers={'accept': 'application/json', 'Content-Type': 'application/json'},
                             headers=data_auth, data=data_post,
                             )

    print(response.url)
    print(response.status_code)
    print(response.json())

    print('')

    responsedata = response.json()
    result = (responsedata['status'])
    ekresult = responsedata['EK']

    return result, ekresult


def do_device_EKrequestHRWtransactionid(cloudflaretokens, accesstoken, TID, HCW):
    print("Requesting TransactionID from CyberRock")

    data_auth = cloudflaretokens | {'Authorization': 'Bearer ' + accesstoken}

    data_post = {
        "TID": TID,
        "HCW": HCW
    }

    response = requests.post(cyberrock_device_EKrequestHRWtransactionid,
                             # headers={'accept': 'application/json', 'Content-Type': 'application/json'},
                             headers=data_auth, data=data_post,
                             )

    print(response.url)
    print(response.status_code)
    print(response.json())

    print('')

    tiddata = response.json()

    transactionid = tiddata['transactionId']

    return transactionid


def do_device_EKrequestHRW(cloudflaretokens, accesstoken, TID, HCW, transactionid):
    print("Submitting TID, HCW to CyberRock")

    data_auth = cloudflaretokens | {'Authorization': 'Bearer ' + accesstoken}

    data_post = {
        "TID": TID,
        "HCW": HCW,
        "transactionId": transactionid
    }

    response = requests.post(cyberrock_device_EKrequestHRW,
                             # headers={'accept': 'application/json', 'Content-Type': 'application/json'},
                             headers=data_auth, data=data_post,
                             )

    print(response.url)
    print(response.status_code)
    print(response.json())

    print('')

    tiddata = response.json()

    transactionid = tiddata['rwTransactionId']

    return transactionid


def do_device_EKrequestHRWstatus(cloudflaretokens, accesstoken, HRWtransactionID):
    print("Retrieving result from CyberRock")

    data_auth = cloudflaretokens | {'Authorization': 'Bearer ' + accesstoken}

    result = 'NOT_READY'

    while (result == 'NOT_READY'):
        time.sleep(sleeptime)

        response = requests.get(cyberrock_device_EKrequestHRWstatus,
                                # headers={'accept': 'application/json', 'Content-Type': 'application/json'},
                                headers=data_auth, params={"rwTransactionId": HRWtransactionID},
                                )

        print(response.url)
        print(response.status_code)
        print(response.json())

        print('')

        responsedata = response.json()
        result = responsedata['status']
        ekresult = responsedata['EK']

    if (result == 'GENERATED_RW'):
        hrw = responsedata['HRW']
        ekresult = responsedata['EK']
    else:
        hrw = ''
        ekresult = ''

    return result, hrw, ekresult


def do_device_priorityrequestHRW(cloudflaretokens, accesstoken, TID, HCW):
    print("Submitting HCW to CyberRock")

    data_auth = cloudflaretokens | {'Authorization': 'Bearer ' + accesstoken}

    data_post = {
        "TID": TID,
        "HCW": HCW
    }

    print(HCW)

    response = requests.post(cyberrock_device_priorityrequestHRW,
                             # headers={'accept': 'application/json', 'Content-Type': 'application/json'},
                             headers=data_auth, data=data_post,
                             )

    print(response.url)
    print(response.status_code)
    print(response.json())

    print('')

    responsedata = response.json()
    result = (responsedata['status'])
    hrw = responsedata['HRW']

    return result, hrw


def do_device_EKpriorityrequestHRW(cloudflaretokens, accesstoken, TID, HCW):
    print("Submitting HCW to CyberRock")

    data_auth = cloudflaretokens | {'Authorization': 'Bearer ' + accesstoken}

    data_post = {
        "TID": TID,
        "HCW": HCW
    }

    print(HCW)

    response = requests.post(cyberrock_device_EKpriorityrequestHRW,
                             # headers={'accept': 'application/json', 'Content-Type': 'application/json'},
                             headers=data_auth, data=data_post,
                             )

    print(response.url)
    print(response.status_code)
    print(response.json())

    print('')

    responsedata = response.json()
    result = (responsedata['status'])
    hrw = responsedata['HRW']
    ekresult = responsedata['EK']

    return result, hrw, ekresult


#/api/device/requestHostAuth
#/api/device/checkRequestHostAuthStatus

#/api/device/EKRequestHostAuth
#/api/device/EKCheckRequestHostAuthStatus
