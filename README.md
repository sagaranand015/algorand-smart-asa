# Algorand Smart ASA
The Algorand Smart ASA allows for more flexible way to work with ASAs providing re-configuration functionalities and the possibility of building additional business logics.
This repo is aimed at [this gitcoin bounty](https://gitcoin.co/issue/29369) for implementing an algorand Smart Contract interacting with Smart ASA providing real world functionality. 

## Abstract
As the new building blocks on the Algorand Blockchain, Smart-ASAs provide the possibility of exploring and implementing custom business logics around operations like asset transfers, royalties, role-based-transfers, limit-amount-transfers, mints, and burns.
Given that Algorand Smart-ASAs has such features in-built, we plan to use Algorand Smart Contracts and Smart-ASAs to implement compliance and rewards automatation in the environmental regulatory industry.

## Entities:
1. Regulators: Institutions responsible for maintaining environmental safeguards and making sure that polluting industries adhere to the standards set by their governing land. 
2. Businesses: Institutions dependent on the environment to create and manufacture products for general use.  

## Implementation
This implementation consists of the following parts, with explanations below:
1. *Compliance Smart Contract*: This smart contract (aka Emission Control) consists of creating an app by a regulatory authority, setting emission controls and their acceptable ranges for a safe environment. The regulatory authority acts as an admin for this compliance app and is responsible for managing the emission controls

2. *Compliance NFT*: The Emission Control(aka Compliance Smart Contract) is capable of minting and transferring these Smart-ASAs to a business based on their compliance status. These NFTs are managed by the emission control(aka Smart Contract) and allows the regulators to build automations on emission controls and businesses. 

## Use cases
The Algorand Smart ASAs allows for several use case to be served for institutions and businesses alike. In the regulatory industry, these potential solutions can be enumerated as:
1. *Compliance Management by Regulators*: Algorand blockchain could become a public medium for regulators to manage their compliance requirements, without the need of any data to be stored with a central entity. Given the blockchain philosophy, all emission controls are publicly accessible on Algorand and allows for an easy way for any regulator to manage compliance in the most public way. 

2. *Compliance Management for Businesses*: With the Algorand blockchain, businesses and institutions have an easy way to hook up their emissions data to a dApp and keep an eye on their compliance levels at any given time. For instance, dApps can allow for a sensor input and keep checking the compliance status at all times. 

3. *Compliance NFT management for Businesses*: Given the in-built features of the Algorand Smart-ASAs, emission controls(aka Smart Contracts) have the ability to issue, mint, transfer, freeze, close the compliance NFTs for businesses with or without grace limits on the businesses' compliance levels. These features also allow regulators to build automations on Compliance NFTs and enforce standards that businesses must stick to, based on the rules laid by their governments. 

4. *Compliance Automations and Rules*: With the Algorand Smart-ASAs, regulators can even build a rule engine baked directly into the Algorand blockchain. In addition to the rules engine, regulators can build workflows like:
    1. automated Compliance NFT minting, 
    2. automated Compliance NFT freezing,
    3. automated reward points based on compliance levels
    4. Reporting on business compliances, generated from publicly available data and so on...

## Solutions Implementation
This repo consists of the following artifacts that would then become the cornerstone of the implementation for a larger, production ready solutions. Please note: 
1. *Emission Control*: Emission Control is a smart contract written using the pyteal-beaker framework and allows for creating emission controls with acceptable ranges of emission values. Emission control also helps:
    1. In managing business/institution compliance
    2. Minting Compliance NFTs
    3. Transferring Compliance NFTs to eligible businesses
    4. Reporting data on Compliance NFTs holders 

## Setup
This implementation is written in python using the Algorand Python SDK and the pyteal-beaker framework for Smart Contracts. To setup the environment, please follow the steps below:
1. Make sure python3.10+ is installed on your development machine and that you've cloned the repo 
2. Run the following commands to setup the virtual environment and the app:
```
cd arc-20-smart-asa
python3 --version -> make sure this is python 3.10+
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 emission_control_client.py
```
3. Run through the command line demo app to interact with the emission control App deployed on the algorand blockchain

## Demo
[DEMO VIDEO IS AVAILABLE HERE](https://youtu.be/v4iyuRsXeec)


## Sample Run of the application on Algorand testnet:
Notes:
1. All the following info is available on the algorand testnet exploer
2. Business1 Account used: `SZ3K22H6MZ3A3ORYIVTAYMQMMBWVFOMJWXR3QCODNMJBQRIKBXN5PXX6AI`
3. Regulator Account used: `2RYRFNXY66QK7TSYNGODPBOYCALJNOPRHVDCDQNQ57BUBS2TBJH3H2QBJQ`

### Step 1:
```
--- Starting Emission Control App Interaction with the python client ---
--- See .emission_control file for verbose details ---
--- CHOOSE FROM THE MENU OPTION BELOW ---
1. Create an Emission Control for Carbon Dioxide (max emission: 100)
2. Show the Emission Control Values configured for the app
3. Update the Carbon Dioxide Emission Control value to 200
4. Check if Business1 is compliant with Carbon Dioxide Emission Control (emission value for Business1 is: 90)
5. Check if Business2 is compliant with Carbon Dioxide Emission Control (emission value for Business2 is: 220)
6. Create a Compliance NFT
7. Make Business1 Opt into the Compliance NFT
8. Transfer Compliance NFT to Business1
0. Press 0 to Exit

--- INPUT YOUR CHOICE: 1
Created Compliance app at 120292561 JPH3TKASKTUQHXVJSWFXF2NR3Z7QYGSFMEXUTI2Q5Y6UJZS3T6MNJDT2MQ
Funded app
Opted in
Current app state:{'emission_max': 0, 'emission_min': 0, 'emission_parameter': '', 'regulator': ''}
```
This step creates the compliance app with id: 120292561 and aty address: JPH3TKASKTUQHXVJSWFXF2NR3Z7QYGSFMEXUTI2Q5Y6UJZS3T6MNJDT2MQ

### Step 2:
```
--- CHOOSE FROM THE MENU OPTION BELOW ---
1. Create an Emission Control for Carbon Dioxide (max emission: 100)
2. Show the Emission Control Values configured for the app
3. Update the Carbon Dioxide Emission Control value to 200
4. Check if Business1 is compliant with Carbon Dioxide Emission Control (emission value for Business1 is: 90)
5. Check if Business2 is compliant with Carbon Dioxide Emission Control (emission value for Business2 is: 220)
6. Create a Compliance NFT
7. Make Business1 Opt into the Compliance NFT
8. Transfer Compliance NFT to Business1
0. Press 0 to Exit

--- INPUT YOUR CHOICE: 2
Current app state:{'emission_max': 0, 'emission_min': 0, 'emission_parameter': '', 'regulator': ''}
```
The Current app state after creation is set to default.

### Step 3:
```
--- CHOOSE FROM THE MENU OPTION BELOW ---
1. Create an Emission Control for Carbon Dioxide (max emission: 100)
2. Show the Emission Control Values configured for the app
3. Update the Carbon Dioxide Emission Control value to 200
4. Check if Business1 is compliant with Carbon Dioxide Emission Control (emission value for Business1 is: 90)
5. Check if Business2 is compliant with Carbon Dioxide Emission Control (emission value for Business2 is: 220)
6. Create a Compliance NFT
7. Make Business1 Opt into the Compliance NFT
8. Transfer Compliance NFT to Business1
0. Press 0 to Exit

--- INPUT YOUR CHOICE: 3
=============== BLOCKCHAIN INTERACTION RESULT ===============
TXN: Z35RNNLQOBHKEIAZTN3Z52RFFWZNCIB7GW4JLWHEXCM3BWYYJO6Q, RESULT: b'\x80', RETURN_VAL: True
=============== BLOCKCHAIN INTERACTION RESULT ===============
```
Result Txn: Z35RNNLQOBHKEIAZTN3Z52RFFWZNCIB7GW4JLWHEXCM3BWYYJO6Q
The current state of the app should now be set to {'emission_max': 200, 'emission_parameter': 'CO2:Carbon Dioxide Emission', 'regulator': '', 'emission_min': 0} (See step 4 below)

### Step 4:
```
--- CHOOSE FROM THE MENU OPTION BELOW ---
1. Create an Emission Control for Carbon Dioxide (max emission: 100)
2. Show the Emission Control Values configured for the app
3. Update the Carbon Dioxide Emission Control value to 200
4. Check if Business1 is compliant with Carbon Dioxide Emission Control (emission value for Business1 is: 90)
5. Check if Business2 is compliant with Carbon Dioxide Emission Control (emission value for Business2 is: 220)
6. Create a Compliance NFT
7. Make Business1 Opt into the Compliance NFT
8. Transfer Compliance NFT to Business1
0. Press 0 to Exit

--- INPUT YOUR CHOICE: 2
Current app state:{'emission_max': 200, 'emission_parameter': 'CO2:Carbon Dioxide Emission', 'regulator': '', 'emission_min': 0}
```
Result: New app state now is {'emission_max': 200, 'emission_parameter': 'CO2:Carbon Dioxide Emission', 'regulator': '', 'emission_min': 0}

### Step 5:
```
--- CHOOSE FROM THE MENU OPTION BELOW ---
1. Create an Emission Control for Carbon Dioxide (max emission: 100)
2. Show the Emission Control Values configured for the app
3. Update the Carbon Dioxide Emission Control value to 200
4. Check if Business1 is compliant with Carbon Dioxide Emission Control (emission value for Business1 is: 90)
5. Check if Business2 is compliant with Carbon Dioxide Emission Control (emission value for Business2 is: 220)
6. Create a Compliance NFT
7. Make Business1 Opt into the Compliance NFT
8. Transfer Compliance NFT to Business1
0. Press 0 to Exit

--- INPUT YOUR CHOICE: 4
=============== BLOCKCHAIN INTERACTION RESULT ===============
TXN: ZXAT2WV2QEV6VZN2DCX73WCGF52U4WK3SCBNWYXXO5AYQVCXE63Q, RESULT: b'\x80', RETURN_VAL: True
=============== BLOCKCHAIN INTERACTION RESULT ===============
```
Result: `Business1` is NOW COMPLIANT with the emission control created in step 1. Txn: ZXAT2WV2QEV6VZN2DCX73WCGF52U4WK3SCBNWYXXO5AYQVCXE63Q

### Step 6:
```
--- CHOOSE FROM THE MENU OPTION BELOW ---
1. Create an Emission Control for Carbon Dioxide (max emission: 100)
2. Show the Emission Control Values configured for the app
3. Update the Carbon Dioxide Emission Control value to 200
4. Check if Business1 is compliant with Carbon Dioxide Emission Control (emission value for Business1 is: 90)
5. Check if Business2 is compliant with Carbon Dioxide Emission Control (emission value for Business2 is: 220)
6. Create a Compliance NFT
7. Make Business1 Opt into the Compliance NFT
8. Transfer Compliance NFT to Business1
0. Press 0 to Exit

--- INPUT YOUR CHOICE: 5
=============== BLOCKCHAIN INTERACTION RESULT ===============
TXN: VIDMKTTU45XWKM6TW7PGT3HFR2DSIC4F7GIR5IKG2LK4LMHU7OWQ, RESULT: b'\x00', RETURN_VAL: False
=============== BLOCKCHAIN INTERACTION RESULT ===============
```
Result: `Business2` is NOW COMPLIANT with the emission control created in step 1. Txn: VIDMKTTU45XWKM6TW7PGT3HFR2DSIC4F7GIR5IKG2LK4LMHU7OWQ

### Step 7:
```
--- CHOOSE FROM THE MENU OPTION BELOW ---
1. Create an Emission Control for Carbon Dioxide (max emission: 100)
2. Show the Emission Control Values configured for the app
3. Update the Carbon Dioxide Emission Control value to 200
4. Check if Business1 is compliant with Carbon Dioxide Emission Control (emission value for Business1 is: 90)
5. Check if Business2 is compliant with Carbon Dioxide Emission Control (emission value for Business2 is: 220)
6. Create a Compliance NFT
7. Make Business1 Opt into the Compliance NFT
8. Transfer Compliance NFT to Business1
0. Press 0 to Exit

--- INPUT YOUR CHOICE: 6
=============== BLOCKCHAIN INTERACTION RESULT ===============
TXN: GDXAYZIKG7KMM733JMIHJA33KOZR54QT3NRCDQ7KJUECND2NKYMA, RESULT: b'\x00\x00\x00\x00\x07+\x85\xe0', RETURN_VAL: 120292832
=============== BLOCKCHAIN INTERACTION RESULT ===============
```
Result: Smart ASA created with asset id: 120292832 and Txn: GDXAYZIKG7KMM733JMIHJA33KOZR54QT3NRCDQ7KJUECND2NKYMA

### Step 8:
```
--- CHOOSE FROM THE MENU OPTION BELOW ---
1. Create an Emission Control for Carbon Dioxide (max emission: 100)
2. Show the Emission Control Values configured for the app
3. Update the Carbon Dioxide Emission Control value to 200
4. Check if Business1 is compliant with Carbon Dioxide Emission Control (emission value for Business1 is: 90)
5. Check if Business2 is compliant with Carbon Dioxide Emission Control (emission value for Business2 is: 220)
6. Create a Compliance NFT
7. Make Business1 Opt into the Compliance NFT
8. Transfer Compliance NFT to Business1
0. Press 0 to Exit

--- INPUT YOUR CHOICE: 7
Signed transaction with txID: A5PNDQB64YCRIKHAO5X5B7DPWRTUIUUZD6RTUCSEJ6TAP2XZFUWA
TXID:  A5PNDQB64YCRIKHAO5X5B7DPWRTUIUUZD6RTUCSEJ6TAP2XZFUWA
Result confirmed in round: 25260587
```
Result: Business1 signs the OPT-IN transaction for the compliance NFT. Txn:  A5PNDQB64YCRIKHAO5X5B7DPWRTUIUUZD6RTUCSEJ6TAP2XZFUWA


### Step 9:
```
--- CHOOSE FROM THE MENU OPTION BELOW ---
1. Create an Emission Control for Carbon Dioxide (max emission: 100)
2. Show the Emission Control Values configured for the app
3. Update the Carbon Dioxide Emission Control value to 200
4. Check if Business1 is compliant with Carbon Dioxide Emission Control (emission value for Business1 is: 90)
5. Check if Business2 is compliant with Carbon Dioxide Emission Control (emission value for Business2 is: 220)
6. Create a Compliance NFT
7. Make Business1 Opt into the Compliance NFT
8. Transfer Compliance NFT to Business1
0. Press 0 to Exit

--- INPUT YOUR CHOICE: 8
=============== BLOCKCHAIN INTERACTION RESULT ===============
TXN: GUJILCJOTKIPBHRQOV3SN4E3FPKH73LLM2AECSEUN3JMP547XZSQ, RESULT: b'\x00\x00\x00\x00\x07+\x85\xe0', RETURN_VAL: 120292832
=============== BLOCKCHAIN INTERACTION RESULT ===============
```
Result: The Compliance NFT (asset id: 120292832) is now transferred to Business1 with Txn: GUJILCJOTKIPBHRQOV3SN4E3FPKH73LLM2AECSEUN3JMP547XZSQ

### Step 10:
```
--- CHOOSE FROM THE MENU OPTION BELOW ---
1. Create an Emission Control for Carbon Dioxide (max emission: 100)
2. Show the Emission Control Values configured for the app
3. Update the Carbon Dioxide Emission Control value to 200
4. Check if Business1 is compliant with Carbon Dioxide Emission Control (emission value for Business1 is: 90)
5. Check if Business2 is compliant with Carbon Dioxide Emission Control (emission value for Business2 is: 220)
6. Create a Compliance NFT
7. Make Business1 Opt into the Compliance NFT
8. Transfer Compliance NFT to Business1
0. Press 0 to Exit

--- INPUT YOUR CHOICE: 0
--- BYE. THANK YOU!
```
Result: Exiting from the app

