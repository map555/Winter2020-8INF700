# Winter2020-8INF700
Smart clock prototype made by a bachelor degree student at Université du Québec à Chicoutimi in the context of the "Special Subject in
Computer Science (8INF700)" class under the supervisition of Sylvain Hallé. This project is made for Raspberry Pi's Raspbian and the Raspberry Pi's
official 7 inches display (v1.1).


This little application has the following functionnality:

- Hour and weather

- Spotify music (a Spotify premium account is required to play Spotify's music on your Pi)

- Alarm clock

- Messenger's notification


INSTALLATION
For installating the app, you have to type this command in the terminal:

sh -c "$(curl -fsSL https://raw.githubusercontent.com/map555/Winter2020-8INF700/master/Winter20_8INF700/installer.sh)"

Then, you just have to configure raspotify, you can follow the configuration part to set it:
https://pimylifeup.com/raspberry-pi-spotify/




NOTES:
Dark Sky Weather is now Apple's property 😕
So you need to already have a Dark Sky Weather API key to run the app because they stopped the support for new users
and they will support the api for already suscribed user until the end of 2021.


Also because the app emulated the connection to messenger into a browser, you could have problems with your account because sometimes when
the applications connects to messenger, Facebook can interpratate that like a unknown connection to your account and it will be temporarly blocked until 
you reset your password. This problem happens espacialy when it's been a long time that you didn't start the program.

For now, the Messenger Notification only support user to user and group conversation, marketplace sale conversation will crash the app.

You can't use your Spotify's username and password anymore to generate authentification token with the spotify-token library. You have to use respectively the "sp_dc" and "sp_key" cookies as Spotify's username and password. For more details you can consult the spotify-token' usage instruction at the Python Package Index page of the project:
https://pypi.org/project/spotify-token/1.0.0/
