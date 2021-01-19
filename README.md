# django-blog

Site with all the necessary tools for blogging, written in Django.

## Features:

- [User Registration (Sign-in and Sign-up)](https://github.com/satyam-nitt18/django-blog/new/master?readme=1#user-registration-sign-in-and-sign-up)
- [Create, Publish, Edit & Delete Posts](https://github.com/satyam-nitt18/django-blog/new/master?readme=1#create-publish-edit--delete-posts)
- [User Change Password](https://github.com/satyam-nitt18/django-blog/new/master?readme=1#user-change-password)
- [Editable User profiles](https://github.com/satyam-nitt18/django-blog/new/master?readme=1#editable-user-profiles)
- [Account Activation Link sent to Gmail using SMTP](https://github.com/satyam-nitt18/django-blog/new/master?readme=1#account-activation-link-sent-to-gmail-using-smtp)
- [Likes and Comments](https://github.com/satyam-nitt18/django-blog/new/master?readme=1#likes-and-comments)
- [Custom Search using Inverted Indexing](https://github.com/satyam-nitt18/django-blog/new/master?readme=1#custom-search-using-inverted-indexing)
- [Notifications](https://github.com/satyam-nitt18/django-blog/new/master?readme=1#notifications)
- [APIs using Django REST Framework](https://github.com/satyam-nitt18/django-blog/new/master?readme=1#apis-using-django-rest-framework)

### User Registration (Sign-in and Sign-up):

### Create, Publish, Edit & Delete Posts:

### User Change Password:

### Editable User profiles:
Each user has his own personal page, which contains information about username, date of birth (set to a default value on first time Login) contact info (mobile number (optional) and email-ID, list of user's posts, short description and profile image.
All of which can be updated anytime.


### Account Activation Link sent to Gmail using SMTP:

### Likes and Comments:

### Custom Search using Inverted Indexing:
Custom search engine based on inverted indexes. You can search for one word and whole sentences in random order.
### Notifications:
Notifications gives you the opportunity to subscribe to user activity (new posts) and to new posts comments.  
Notifications come in real time.

### APIs using Django REST Framework:
API for extracting all Posts and Users.
These can be accessed from the command-line, using curl:  
bash: curl -H 'Accept:application/json;indent=4' -u username:password https://satyam10899.pythonanywhere.com/api-root/users/  
bash: curl -H 'Accept:application/json;indent=4' -u username:password https://satyam10899.pythonanywhere.com/api-root/posts/  

Or directly through the browser, by going to the URL https://satyam10899.pythonanywhere.com/api-root/  
