# _tennis_court_reservations
>author: Michał Tarnacki

**In this program an user can make, cancel, print and save reservations.**

Let's us take a look at the main menu:

	What do you want to do:
	1.Make a reservation
	2.Cancel a reservation
	3.Print schedule
	4.Save schedule to a file
	5.Exit

It provides several options. To choose one of them, user can either prompt a command or enter an option number.
To make UI more user friendly this rule also applies to other prompts.

**Lets enter then "Make a reservation"**

	What's your Name?

**Do not know the input format? Do not worry! The program will help you if you do something wrong:**

	Given name is invalid, it should contain first name, last name and space between. Only letters are valid

**Have you changed your mind? No problem, just enter "exit"**

There are a lot of different alerts so you should know where you are and why something is not working.

**If you want to change some program's parameters you can simply do it by changing variables in Macros file.**

For example you can set different time intervals or increase their number. Keep in mind, custom parameters have not been tested and may cause errors.

**Due to lack of time there are only several unit tests, but I did not encounter any bugs which does not mean they are not any.**

Every input is validated so user should not do anything leading to error.

**Notes**

I assume that user can make a reservation at time like 9:37 as long as it is during opening hours (set in Macros file).
To achieve data persistence the the schedule is kept in SQLite database.
