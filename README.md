# QuickCheckout
Project with objective of creating an EPoS (Electronic Point of Sale, modern day till system) for supermarkets.

# Start
To start, run main.py 
Default Credentials:
Username = admin
Password = password

# Features
* Checkout Window
* Transaction History 
* Item Management
* Employee Management

## Checkout Window
Main EPoS window. Allows for selection of items and processes customer's bill

## Transaction History
To show the previous transactions, with details about 
* Customer Details
* Date of Transaction
* Details of Item's Bought
* ID of Cashier

## Item Management
To show the items available for purchase. 
SET the price of items, add new items, delete items, modify available amount.

Note: On transaction, amount of items bought is automatically subtracted from the available amount for each item. 

## Employee Management
Manage accounts which have access to main application.
* Add/Delete accounts
* Set Details about employee. 

Employee's are of 2 types, Admin and Default. 
Default accounts only have access to main EPoS window. 

If an account's personal information isn't stored, it prompts a `Registration Window` to take in personal details. 



