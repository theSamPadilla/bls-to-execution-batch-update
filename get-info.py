import json, requests

def main():
    #Get configs
    with open('config.json', "r") as f:
        buff = json.load(f)
        network = buff["network"]
        starting_index = buff["starting-index"]
        deposit_address = buff["eth1-deposit-address"]
        withdrawal_address = buff["eth1-withdrawal-address"]
        beacon_endpoint = buff["beacon-api-endpoint"]
        beacon_api_key = buff["beacon-api-key"]
        beaconcha_in_api_key = buff["beaconcha-in-api-key"]
        f.close()

    #Set beaconcha.in endpoint
    if network != "mainnet":
        beaconcha_in_endpoint = f"https://{network}.beaconcha.in"
    else:
        beaconcha_in_endpoint = "https://beaconcha.in"
 
    #Get validator related to address /api/v1/validator/eth1/{eth1address}
    response = requests.get(f"{beaconcha_in_endpoint}/api/v1/validator/eth1/{deposit_address}?apikey={beaconcha_in_api_key}")
    
    #Fail missed requests gracefully
    if response.status_code != 200:
        print(f"\n\n[FATAL] Beaconcha.in API Request Failed with code {response.status_code}. Try again later.")
        print(response.text)
        exit(1)

    #Process response
    buff = json.loads(response.text)["data"]
    validator_public_keys_to_indexes = {}
    for validator in buff:
       validator_public_keys_to_indexes[validator["publickey"]] = validator["validatorindex"]

    #Get withdrawal credentials for each validator
    validator_indexes_to_withdrawal_credentials = {}

    for i in validator_public_keys_to_indexes.values():
        if beacon_api_key:
            response = requests.get(f"{beacon_endpoint}/eth/v1/beacon/states/head/validators/{i}?key={beacon_api_key}")
        if response.status_code != 200:
            print(f"\n\n[FATAL] API Request to beacon node failed with code {response.status_code}. Try again later.")
            print(response.text)
            exit(1)

        #Process response
        buff = json.loads(response.text)
        withdrawal_credentials = buff["data"]["validator"]["withdrawal_credentials"]
        if withdrawal_credentials[:4] == "0x00": #Check that withdrawal are unset
            validator_indexes_to_withdrawal_credentials[i] = withdrawal_credentials

    #Output Comma separated response
    print(", ".join([str(i) for i in validator_indexes_to_withdrawal_credentials.keys()]))
    print(", ".join(validator_indexes_to_withdrawal_credentials.values()))

    #Ouput how many 0x00 credentials found for {address}, network, and starting index
    print(len(validator_indexes_to_withdrawal_credentials))
    print(deposit_address)
    print(network)
    print(starting_index)
    print(withdrawal_address)
    
    return

if __name__ == "__main__":
    main()