# CandC
Command and Control server for compromising machines during and engagement. Purpose is to provide semi-remote access to a central location while traveling. Allowing for connections to compromised machines to persist while changing physical location.

## Installation

Learning how to make a requirements.txt file until then just pip install the following:

flask
pymongo
bcrypt
ifaddr

## Config

Currently the only configuration needed for opperation is an admin user be added to the database. Database should be setup in the following way.

database name: CandC
tables: 
	CandC_auth - users table
	CandC_files - files for individual users to upload and download
	CandC_servers - servers that are spun up by the users.

## Usage

python3 main.py
