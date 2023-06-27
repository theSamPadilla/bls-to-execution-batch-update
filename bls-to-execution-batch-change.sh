#!/bin/bash
#Execute python get-info.py script and capture the output
echo "Running `get-info.py`..."
output=$(python3 ./get-info.py)

# Assign each line of output to respective variables
validator_indices=$(echo "$output" | sed -n '1p')
withdrawal_credentials=$(echo "$output" | sed -n '2p')
number_of_validators=$(echo "$output" | sed -n '3p')
deposit_address=$(echo "$output" | sed -n '4p')
network=$(echo "$output" | sed -n '5p')
index=$(echo "$output" | sed -n '6p')
withdrawal_address=$(echo "$output" | sed -n '7p')

if [[ -n $validator_indices && -n $withdrawal_credentials && -n $number_of_validators && -n $deposit_address && -n $network && -n $index && -n $withdrawal_address ]]; then
    echo "Found $number_of_validators validators on ethereum $network with 0x00 withdrawals."
    echo "Executing the update at starting index $index..."

    # Deposit command
    ./deposit --language=english generate-bls-to-execution-change \
    --chain=$network \
    --bls_withdrawal_credentials_list=$withdrawal_credentials \
    --validator_start_index=$index \
    --validator_indices=$validator_indices \
    --execution_address=$address

else
    echo "One or more variables are missing. Cannot proceed."
    echo $output
fi
