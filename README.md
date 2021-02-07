# django-blog

Site with all the necessary tools for blogging, written in Django.

## Features:

- [User Registration (Sign-in and Sign-up) and Change Password](https://github.com/satyam-nitt18/django-blog/new/master?readme=1#user-registration-sign-in-and-sign-up)
- [Create, Publish, Edit & Delete Posts](https://github.com/satyam-nitt18/django-blog/new/master?readme=1#create-publish-edit--delete-posts)
- [Editable User profiles](https://github.com/satyam-nitt18/django-blog/new/master?readme=1#editable-user-profiles)
- [Account Activation Link sent to Gmail using SMTP](https://github.com/satyam-nitt18/django-blog/new/master?readme=1#account-activation-link-sent-to-gmail-using-smtp)
- [Likes and Comments](https://github.com/satyam-nitt18/django-blog/new/master?readme=1#likes-and-comments)
- [Custom Search using Inverted Indexing](https://github.com/satyam-nitt18/django-blog/new/master?readme=1#custom-search-using-inverted-indexing)
- [Notifications](https://github.com/satyam-nitt18/django-blog/new/master?readme=1#notifications)
- [APIs using Django REST Framework](https://github.com/satyam-nitt18/django-blog/new/master?readme=1#apis-using-django-rest-framework)

### User Registration (Sign-in and Sign-up) and Change Password:
Django-crispy-forms filter has been applied to all the forms used in the site for sign-up, sign-in or editing profile to produce elegant division based fields.

### Create, Publish, Edit & Delete Posts:
Site guests are only allowed to view the detailed Posts.
Creation, Editing and Deletion of Posts are allowed for Signed-in users (including Admin). A particular user cannot edit or delete others' posts. However they can comment on unpublished posts listed in the Drafts Section.
Publish action is allowed for Admin alone. The admin decides whether to publish a particular post submitted by signed-up users (moving that post from the Drafts section to the main Home page) or edit or delete them. 

### Editable User profiles:
Each user has his own personal page, which contains information about username, date of birth (set to a default value on first time Login) contact info (mobile number (optional) and email-ID, list of user's posts, short description and profile image.
All of which can be updated anytime.


### Account Activation Link sent to Gmail using SMTP:
For user authentication and email validation, activation link is sent to the provided gmail account using Simple Mail Transfer Protocol. The account created on the Blog site cannot be accessed by the user without clicking on the activation link.

### Likes and Comments:
Likes and comments model similar to any other social media is allowed only for signed-in users to encourage interaction (through comments) and appreciation (through likes) among bloggers.

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
