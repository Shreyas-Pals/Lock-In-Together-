Well - This is literally in Its development stage- A lot of unfinished stuff. I have so many ideas for this project. This is basically a Website which uses the Spotipy API which essentially is a 3rd party Spotify WEB API. The purpose of this website 
is to make Spotify JAM - A premium feature, more fun. I mean, by allowing people's opinions on if a particular song should be played or not. I am also planning to add like a focus mode, and many cool features, but it might take weeks to work 
cleanly. I'm kind of an Audiophile so - I love it when it comes to songs and making something related to it is exciting.

Right now, What I've added and fixed is:-

1) Allowing Logging in through spotify - So Another tab using the same accoutn won't be allowed

2) Allowing multiple users => Each user will be remembered when the code is running, and each user's environment is isolated from every other user, as every user has a unique token associated with him/her
(Its not connected to a database so it's not permanent login which I feel is better for a lightweight website.)

3) Basic "Welcome Page" which is linked to the Home Page(WHhich right now has no UI - but I'm planning to add cool features like waves which move based on how loud the sound is and play as an animation in the background)

Features yet to come:-

There are more features yet to come than there are features there - because I hardly did anything. But some of these are:-

1) Adding a "master - user" who actually is the one who has the access token to spotify to play songs - to make the experience smooth. He would have to send the JAM Link to others - or it could be displayed on the Site itself
2) An "Up Next" to show who's turn it is next to pick a song. Other would have to dislike it if they dont want it to be played.
3) Personalized Queues - Where each user can see his own queue of songs he wants to play next. Every user gets a turn to pick a song. And they can all pre-add/pre-pick songs that they want to be played.
4) Previously played on the JAM - and Tracking number of Dislikes for each song that was played
5) Focus Mode - If someone is actually locked in in his work - he wouldn't want to spend time on any site, he can just have his headphones/earphones on and listen to the songs while staying on the site - without having to "pick a song"/ participate in rating another guy's pick
6) A CLI based version is what I'm more excited about than the web-based one :) That's why I'm probably going to do this first and then the web based version.
7) Currently, I'm planning to use Bootstrap and Vanilla CSS or SCSS for styling.. and Flask to manage routing,requests, connection with Spotify,etc..

I will provide a short video of my website actually running(Which doesn't have much right now)
