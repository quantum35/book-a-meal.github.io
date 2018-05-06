# BOOK A MEAL
[![Build Status](https://travis-ci.org/quantum35/book-a-meal.github.io.svg?branch=feature%2Fchallenge3)](https://travis-ci.org/quantum35/book-a-meal.github.io)

Book-A-Meal is an application that allows customers to make food orders and helps the food vendor know what the customers want to eat.
This Project Was created Using  Stories From Pivotal Tracker [here](https://www.pivotaltracker.com/n/projects/2165741) intergrated to Github Using Its API Token

## Getting started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. 
See deployment for notes on how to deploy the project on a live system.
###                             Clone the Repository [here](https://github.com/quantum35/book-a-meal.github.io.git)

### Introduction
This web Project is created to Easen the work of a Customer by simply Ordering Food Of Choice From The Comform Of his or her Home Then The caterer(admin) will Recieve the Order and Deliver IT To the Customer in Time.
This Project is Composed Of Two Parts

* Server-side
* Client-side

# Server-side

## Prerequisites
Ensure you Have The Following:

```
1.Postgres
2.Python version 3 and above
3.Virtualenv
4.Flask
5.Postman
```
##### Download latest version of python [here](https://www.python.org/downloads/release/python-365/)
##### Creating virtual environment [here](http://docs.python-guide.org/en/latest/dev/virtualenvs/)
##### Find instruction of installing  Flask [here](http://flask.pocoo.org/docs/1.0/installation/)
##### Download Postman [here](https://www.getpostman.com)

## Dependencies
- Install the project dependencies:
> $ pip install -r requirements.txt

## Set up Database
- Create a database:
> $ createdb todos

- Run migrations:
> $ python manage.py db upgrade

After setting up the above. Run:

```python run.py``` or ``` flask run```
### To run Tests
- Type nosetests on your Terminal
> $ nosetests

Test the endpoints registered on `run.py` on Postman/curl on the port the app is running on. 


# The Client-side

This is Where User both Customer and admin Log in using their Resective Credentials which are secure.
 Here is a sample Login Page ![Login Page](https://github.com/quantum35/book-a-meal.github.io/blob/master/UI/gh-images/Screen%20Shot%202018-04-22%20at%2001.55.19.png) 
Once The User Has Loged in.They Will see Their Respective Profile
## Admin
![Profile](https://github.com/quantum35/book-a-meal.github.io/blob/master/UI/gh-images/Screen%20Shot%202018-04-22%20at%2001.54.45.png)

# Tools To Have To Get Started

* Any Browser I Recomend Google Chrome
* Little Knowledge of **Html**,**CSS** and **JS**
* Text Editor I Recomend Visiual Studio Code

## Contribution
Fork my Git to Contribute and Feel at Home Customising it to your Preffered Layout
