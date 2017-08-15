# Catalogue_App_Project 


### Project Description

You will develop an application that provides a list of items within a variety of categories as well as provide a user registration and authentication system. Registered users will have the ability to post, edit and delete their own categories and items.

1. Why This Project?
    Modern web applications perform a variety of functions and provide amazing features and utilities to their users; but deep down,   it’s really all just creating, reading, updating and deleting data. In this project, you’ll combine your knowledge of building dynamic websites with persistent data storage to create a web application that provides a compelling service to your users.

2. What Will I Learn?
   You will learn how to develop a RESTful web application using the Python framework Flask along with implementing third-party OAuth authentication. You will then learn when to properly use the various HTTP methods available to you and how these methods relate to CRUD (create, read, update and delete) operations.


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
    $ cd /vagrant/news
  ```
  4. All of the files related to this project are in the [/vagrant/news](https://github.com/mdjolieca/fullstack-nanodegree-vm/tree/master/vagrant/news) directory
  
  
#### Setting up the database:

   1. Unzip the /vagrant/news/newsdata.zip  file.  
  
   2. Load the data into the news database using the newsdata.sql script from step 1 zip file:
  
  ``` 
    psql -d news -f newsdata.sql
  ```
   3. (Optional)Use `psql -d news` to connect to database and veiw the table structure.
      The database includes three tables:
        * The authors table includes information about the authors of articles.
        * The articles table includes the articles themselves.
        * The log table includes one entry for each time a user has accessed the site.
  
 
  #### Generate the reports:
  1. From the /vagrant/news directory inside the virtual machine, run::
  ```
    $ python3  newsreports.py
  ```
  results should be identical to the thoose the [sampleReport](https://github.com/mdjolieca/fullstack-nanodegree-vm/blob/master/vagrant/news/sampleReport)  file provided.
 
