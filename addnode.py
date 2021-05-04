#script - can use a script box on the website
#!/usr/local/bin/python
import hashlib
import hmac
import time
import requests
import base64
import json

# Client credentials - From the Clusters Portal
client_id = "************.img.frame.nutanix.com" 
client_secret = "***********”
cluster_id ="0005AC9D-****-****-****-5F727B535EC9"
# Create signature
timestamp = int(time.time())
to_sign = "%s%s" % (timestamp, client_id)
signature = hmac.new(client_secret, to_sign, hashlib.sha256).hexdigest()
domain = prod_domain

# Prepare http request headers
headers = { "X-Frame-ClientId": client_id, "X-Frame-Timestamp": str(timestamp), "X-Frame-Signature": signature }

r = requests.get(domain + "/v1/clusters/" + cluster_id, headers=headers)

response = r.json()
#node = json.loads(response)
#Find the current nodecapacity 
cap = response['capacity_settings'][0]['nodes_count']
#Add 1 node to the current capacity 
newNodeCount = cap + 1

# Create the cluster
body = {
  "capacity_settings": [
    {
      "instance_type_name": "z1d.metal",
      "nodes_count":  newNodeCount
    }
  ]
}
#print body
print domain + '/v1/clusters/' + cluster_id + '/cluster_capacity'

#update the intent for more nodes  cluster
increase = requests.post(domain + "/v1/clusters/" + cluster_id + "/cluster_capacity", headers=headers, json=body)
print increase #double check response 
