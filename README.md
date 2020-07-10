# questionBank

## How to setup:

This project was setup using python 3.7 So it's recommended to install it and use it. Virtual enviornment using venv is recommended for development.

1. Activate your virtual env.
2. Install dependencies listed in req.txt using the command: pip install -r req.txt
3. Your dependencies will be installed. Your setup is complete.

## Functionality

1. Signup for the user - (username, email, password)
2. Verification link will be sent to the given email, by clicking on link the user can login.
3. user can complete its student profile (naqme, class, phone number, etc.)
4. user can upload question papers of any subjetcs providing (subject code, subject name, year and type[minor, major])
5. created one to many relationship for question paper files, so that we can get the multiple images for a single subject (minimising qualty issues by this).
6. suppose a user uploads a question paper of subject 'A' and if there is already a question paper uploaded for subject 'A' then it will be uploaded under
   that else will upload normally.
7. user can download any question paper anytime.
8. search option - not smart search but a simple search like- we can filter in the basis of subject code, subject name, year and type of the question paper.
9. user can give feedback to us, that will be stored in our db. and an email wuill be sent to the user that we recieved your feedback
10. password reset option.
password forgot option [link sent to the user'email, after clicking and verifying , user can change the password.]

## Tech stack used
Django, HTML, css, Bootstrap, sqllite(will use other db for deploying) .


## Purpose

made for the students of the college to make their life easy. Now students can get previous year question papers pn single platform, this will not waste the time of 
the students one night before the exam. 
