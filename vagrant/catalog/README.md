# Catalogue_App_Project 


### Project Description

You will develop an application that provides a list of items within a variety of categories as well as
provide a user registration and authentication system. Registered users will have the ability to post, 
edit and delete their own categories and items.

1. Why This Project?
    Modern web applications perform a variety of functions and provide amazing features and utilities to their
    users; but deep down,   it’s really all just creating, reading, updating and deleting data. In this project, 
    you’ll combine your knowledge of building dynamic websites with persistent data storage to create a web 
    application that provides a compelling service to your users.

2. What Will I Learn?
   You will learn how to develop a RESTful web application using the Python framework Flask along with implementing
   third-party OAuth authentication. You will then learn when to properly use the various HTTP methods available
   to you and how these methods relate to CRUD (create, read, update and delete) operations.


### How to Run?

#### PreRequisites:
  * [Python3](https://www.python.org/)
  * [Vagrant](https://www.vagrantup.com/)
  * [VirtualBox](https://www.virtualbox.org/)
  
#### Setup Project:
  1. Install Vagrant and VirtualBox
  2. Download or Clone [fullstack-nanodegree-vm](https://github.com/mdjolieca/fullstack-nanodegree-vm) repository.
  
#### Launching the Virtual Machine:
  1. Launch the Vagrant VM inside Vagrant sub-directory in the downloaded fullstack-nanodegree-vm repository using command:
  
  ```
    $ vagrant up
  ```
  2. Then Log into this using command:
  
  ```
    $ vagrant ssh
  ```
  3. Change directory to /vagrant/news and look around with ls.
  ```
    $ cd /vagrant/catalog
  ```
  4. All of the files related to this project are in the [/vagrant/catalog](https://github.com/mdjolieca/fullstack-nanodegree-vm/tree/master/vagrant/catalog) directory
  
  
#### Setting up the database:

   1. run the /vagrant/catalog/database_setup.py  script:
    ```
    $ python3 database_setup.py
  ```
  
   2. Load the data into the catalog database using the populate_db.py script. Before running this 
   script edit line [16](https://github.com/mdjolieca/fullstack-nanodegree-vm/blob/master/vagrant/catalog/populate_db.py#L16)
   to include the gmail email adress that will be used for testing. Do not worry about the user name or picture. They will be 
   updated on firts login. After you have edited the populate_db.py script run it:
  
  ``` 
    $ vi populate_db.py   # besure to update line 16 as mentioned above
    $ python3 populate_db.py
  ```
   3. Google Oauth Setup
        1. Go to your app's page in the Google APIs Console — https://console.developers.google.com/apis
        2. At top of dashboard home click 
        2. Choose Credentials from the menu on the left.
        3. Create an OAuth Client ID.
        4. When you're presented with a list of application types, choose Web applicationite.
  
 
  #### Run the Catalog App:

 
