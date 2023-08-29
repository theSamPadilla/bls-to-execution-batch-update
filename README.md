# Batch bls-to-execution-change
Every pre-merge validator has to update their ehtereum withdrawal credentials at some point by following the instructions on the [Ethereum launchpad](https://launchpad.ethereum.org/en/btec/).

There are a few ways to do this, but the most common one is using the [`deposit-cli`](https://github.com/ethereum/staking-deposit-cli/releases/).

While straight forward, the process can be tedius for node operators running multiple validators on testnet or mainnet. For that, this repo contains python and bash scripts to batch update all the credentials associated to a given address.

This repo **does not handle validator keys** and the scripts here **only start the process of generating the `bls_to_execution_changes-*.json` file**, needing still manual confirmation from the user when interacting with the `deposit-cli`.

Running this script **is reversible** and safe. Withdrawal credentials will only be updated once the generated `bls_to_execution_changes-*.json` is submitted to a beacon node.

## Setup
#### 1. Clone the Repo and download python
To clone the repo:
```
git clone https://github.com/theSamPadilla/bls-to-execution-batch-update
```

To [download python see these instructions](https://www.python.org/downloads/).

#### 2. Add your validator and wallet info to `config.json`.
```
{
    "network": "<network>",
    "eth1-deposit-address": "<deposit-address>",
    "eth1-withdrawal-address": "<withdrawal-address>",
    "beacon-api-endpoint": "<beacon-endpoint>",
    "beacon-api-key": "<parameter key if any>",
    "beaconcha-in-api-key": "<beaconcha.in api key>",
    "starting-index": 0
}
```
Namely, replace:
- `<network>` with the network for where you run the validators (mainnet, goerli, etc).
- `<deposit-address>` with the **eth1 address that performed the deposit for the validators.**
- `<withdrawal-address>` with the **eth1 address to set as the withdrawal address** (can be the same as the first one).
- - **NOTE: MAKE SURE YOU HAVE FULL CONTROL OF THIS ADDRESS**
- `<beacon-endpoint>` with the beacon endpoint for `netowrk`. Make sure this node is synced to the specified network or the process will not work.
- `<parameter key if any>` with the parameter key for the beacon endpoint, if any.
- `<beaconcha.in api key>` with your beaconcha.in api key. Free tier should be enough. For information on how to get an API endpoint go to https://beaconcha.in/pricing.

**NOTE: The script assumes that the starting index for your validators according to [EIP-2334](https://eips.ethereum.org/EIPS/eip-2334#eth2-specific-parameters) is 0 and that all validators have keys are derived from the same mnemonic**. If this is not the case it is not encouraged to use this script.

#### 3. Download the Ethereum deposit CLI to the same root directory.
[Official Page](https://github.com/ethereum/staking-deposit-cli/releases/) for the Ethereum CLI at the time of writing.
```
wget <latest version url>
tar -xzf <filename>.tar.gz
```

#### 4. Run the script
To execute, just run the script:
```
./bls-to-execution-batch-change.sh
```

Alternatively, you can also run the python script to get the info you need and interact with the deposit on your own. To run the script, simply:
```
python3 get-info.py
```

#### 5. Finish the process by interacting with the deposit CLI
After running the script above, you will be prompted to re-enter the `withdrawal-address` set in the `config.json`. Take this moment to **triple-check you have full control over this address**.

Finally, you will be prompted to enter your `mnemonic phrase` that was generated when you first created the validator keys.

**NOTE:** You are interacting here directly with the `deposit-cli`, not with any of the code in this repo.

#### 6. Upload the bls_to_execution_changes-*.json file to your beacon node.
If everything is succesful, a `bls_to_execution_changes-*.json` file will be generated in the `./bls_to_execution_changes` directory.

To upload this to your beacon node and complete the process, run:
```
curl -X POST -H "Content-type: application/json" -d @<path-to-bls_to_execution_changes-*.json> \
http://<BEACON_NODE_HTTP_API_URL>/eth/v1/beacon/pool/bls_to_execution_changes
```

Make sure to replace:
- `<path-to-bls_to_execution_changes-*.json>` with the proper path to the `.json` file.
- `<BEACON_NODE_HTTP_API_URL>` with your chosen beacon api endpoint. The same you defined in the config file should work.

---

## How it works
The `get-info.py` file makes a request to the `beaconcha.in` API to get all the validator indices funded by the `deposit-address`.

It then gets all the current `0x00` credentials for those validator indices, and outputs a comma-separated string of all the indices and credentials, alongside with other information.

All this information is used then by the `bls-to-execution-batch-change.sh` script to interact with the deposit.

## Disclaimer & License
Although Google is the employer of the author of the repo, this is not an officially supported Google product and does not reflect on Google in any ways.

Neither the author of this repo nor its employer shall be held liable for any issues caused by the usage of this code. This includes but is not limited to bugs, errors, wrong or outdated inforamtion, or even lost of funds.

This repo is published solely on the basis of good faith and as a tool to help developers. This code should be used with caution. The user is running this code at its own risk.

Apache Header:
```
Copyright 2023 Sam Padilla

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```