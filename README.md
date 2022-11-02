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
Please find the demo here: <demo_video>

