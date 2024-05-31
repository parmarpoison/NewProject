
Vendor Management System
-------------------------

Overview
---------

1. This project is a Vendor Management System (VMS) 

2. Developed using Django and Django REST Framework  

3. It provides features for 

    a. Managing vendor profiles,

    b. Tracking purchase orders, and 

    c. Evaluating vendor performance 



Installation
-------------

1.  Clone the repository: 

2.  Install dependencies: pip install -r requirements.txt

3.  Run migrations: python manage.py migrate

4.  Start the development server: python manage.py runserver

Usage
------

1. Create a superuser: python manage.py createsuperuser

2. Access the admin panel to manage vendors, purchase orders, and evaluations: http://localhost:8000/admin/

3. Use the API endpoints to interact with the system: http://localhost:8000/api/

MUST NOTE:
----------

    """  This application uses JWT authentication ,
         so first client need to be a authenticated person.
         For this client should be register as a user , and login  
         Then only he is able to access all above features.  """

    a.   URL   :      "  api/register/  "   ( For Registration as a user)
    b.   URL   :      "  api/login/  "      ( For login as a user )


Features
---------

1. Vendor Profile Management:

   a.  Create a vendor 
              URL :    " POST/api/vendors/ "

   b.  List all vendor
              URL :    " GET/api/vendors/ "

   c.  Get a vendor record 
              URL :    " GET/api/vendors/int:pk/ "

   c.  Update a vendor
              URL :    " PUT/api/vendors/int:pk/ "

   d.  Delete a vendor
              URL :    " DELETE /api/vendors/int:pk/ "

2. Purchase Order Tracking:

   a.  Track All purchase orders:
              URL :    " api/purchase_orders/ "

   b.  Track a single purchase:
              URL :    " api/purchase_orders/<int:pk>/ "
   

3. Vendor Performance Evaluation:
   a. Evaluate vendor performance based on predefined criteria.

              URL :  " api/vendors/<int:vendor_id>/performance/ "

              URL :  " api/purchase_orders/<int:po_id>/acknowledge/ "



In this project Some test case are also defined at the time of 
development all test cases passes successfully. 
    
   


