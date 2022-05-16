# Project Proposal: Bored?

"Bored" is a web application that allows the user to find activities to do when they are bored.

- This site can be used by anyone with a valid email address. Parents/Guardians, some activities are kid friendly!

# Data

- This app will use the Bored API to access data such as :

  - Activities - Receive activities based on specified criteria or get a random activity by not selecting a criteria at all
  - Type - Select from a wide variety of activity types such as charity, educational, music, social, relaxation, and many more
  - Participants - Choose how many people may be involved in the activity
  - Price Range - Choose from price ranges (Free, $, $$, $$$)

# DB Schema

- The database schema consist of tables:
  - Activity - activities, type, participants, price
  - User - username, email, password
  - User Activities - saved, completed (with date), and ignored activities

# API Issues

- If data isn't being received, please check that the API isn't offline.
  - API Link: https://www.boredapi.com

# Application Functionality

- Sign Up / Login
- Mark activities as completed
- Save activities for later
- Ignore activities to avoid it in a future search
- Add custom tags to activities completed
- Add custom notes to activities completed

# User Flow

- Sign Up / Login Page - This will be the landing page for all users coming into the application.
- User Home Page - After login in or signing up, users will see:
  - Navigation bar - Home, My Activities, My Tags, Logout
    - My Activities sub menu - Saved Activities, Completed Activities
  - User home page - Details page with information such as:
    - Number of completed activities with a link to a page with all activities completed.
    - Number of saved activities with a link to a page with all saved activities.
  - A form with criteria for searching an activity will be right below this. The form also provides a random button that chooses a random activity without the criteria constraints. Upon form submission, the activity list will appear under the form. User can choose to save the activity, complete it, or ignore it.
  - Delete Account button for users that wish to remove their account.
- My Activities page - Shows saved and completed activities with their corresponding tags. Remove activities. Add tags to activities or remove them.
- My Tags page - Shows form to add tags as well as a list of all tags user has created. Clicking on a tag links the user to a page with all activities they completed that has that tag included. This tag activities page has a form to update the tag or delete it, deleting this tag from all activities completed.
