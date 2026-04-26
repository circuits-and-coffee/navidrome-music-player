# navidrome-music-player
My first independent Boot.Dev project!

# What does it do?
This app authenticates with a user's Navidrome/Subsonic server, and shuffles 10 songs from their library.

While quite primative, the goal of this repo is to practice with APIs, authentication, and basic GUI design.

# How is authentication handled?
Server domain name & username is stored in a (soon to be) encrypted config.ini file, and credentials are stored in the OS's keyring.

From Subsonic API docs

> Starting with API version 1.13.0, the recommended authentication scheme is to send an
> authentication token, calculated as a one-way salted hash of the password.
> 
> This involves two steps:
> 
> 1) For each REST call, generate a random string called the salt. Send this as parameter s.
>     - Use a salt length of at least six characters.
> 2) Calculate the authentication token as follows: token = md5(password + salt). The md5() function takes a string and returns the 32-byte ASCII hexadecimal representation of the MD5 hash, using lower case characters for the hex values. The '+' operator represents concatenation of the two strings. Treat the strings as UTF-8 encoded when calculating the hash. Send the result as parameter t.
> 
> For example: if the password is sesame and the random salt is c19b2d, then token = md5("sesamec19b2d") = 26719a1196d2a940705a59634eb18eab. The corresponding request URL then becomes:
> http://your-server/rest/ping.view?u=joe&t=26719a1196d2a940705a59634eb18eab&s=c19b2d&v=1.13.0&c=myapp

Since the goal is to ultimately run this on an SBC (like a Raspberry Pi or PocketBeagle), I may need to explore libraries like `keyrings.alt`. I'll see how `keyring` works on a stripped down Debian image works.

# Notes
While LLMs were used for the discovery and learning phases of this project, all code is hand-written by myself. You can tell because of how rough and ragged it is :)