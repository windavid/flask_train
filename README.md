# Usage

python 3 required (3.6)

functionality: 1, 2 option 2, 3

$ pytest # launch all tests
$ python manage.py -h # view more usage description

# Challenge description

We are running the web application which stores and exposes Patients and their Payments. 
The application must stay in sync with external users's system data and provide
some additional analytics on top of the data.

## Models 

As a sample, basic SQLAlchemy models are provided in models.py file.
Feel free to extend and modify them, but do not delete existing fields.

**external_id** field must contain id of an object in external system, and is  
unique in the external source. It is the only field guaranteed not to change. 
All other fields in external source ***can change***, including payment amount!

#### Fameworks/ORMs

You can use flask/django or other framework of choice, just convert the models
by yourself.


## Required functionality

1. Implement web service which exposes methods
    * GET /patients?payment_min=10&payments_max=20
      - Returns list of patients with total amount of payments in supplied range (in 
      this example between $10 and $20) 
      - filters are optional
    
    * GET /payments?external_id=
      - Returns the list of payments, probably filtered by patient's external_id
      - filters are optional
      
2. Implement data sync
    Just for the sake of simplicity we assume all the data comes in one piece, which 
    should be replicated in the database. If something is missing in the upload,
    it means object has been deleted in external system. 
 
    * Option 1. POST /patients and POST /payments methods
    * Option 2. Import json files from the command line
       
3. Keep track of `created` and `updated` model fields. 


## Sample data

Sample data is provided in patients.json and payments.json files. 

 
## Evaluation criteria

* Code as you will code for a production use. You can omit some of the boring stuff 
 if you leave the comment that it should be there.
 Make performance/reliability decisions as for production with 1000x more data/load. 
* Challenge completion time is important, build the working version as fast as you can 

## How to submit
* Clone the repo or start a new one. Do not fork it!
* Upload in public or private repository on github. In case of private, please share the access.
* Keep your commit history.
