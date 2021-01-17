# OW-PUGS-Matchmaker



Basic Discord bot that creates balanced teams for Overwatch PUGS.



# Main Contributors
Cameron Holland

Timothy Wang

# Helped By

Michael Gloner

Vincent Hwang

Daniel Tong

# How to Use
To use any of the following commands, use type a period "." and then the command, if there are additional arguments, add a space and then the appropriate values.
Example: (without quotes)
	
	".support 2500"

# Commands:

.battletag battleTag#1234
	
	- used to set a user's battletag so that the bot may grab your data directly from the game. only works for PC accounts

.update

	- if a user has their battletag set, it will try to grab their SR from Overwatch. must have public profile and be placed in the most current season

.team

	- reminds the user what team they're on, if any

.map

	- returns a random map in the competitive map pool

.commands

	- prints out a brief reminder on how to use the important bot commands

.matchmake

	- makes a match based on users queued. requires 12+ players in queue, 4 for each role

.mm

	- shortcut for .matchmake

.win 1

	- reports the winning team for the bot to change SR values. use 0 for a tie, 1 for team 1, 2 for team 2

.support 1234

	- sets the user's support SR to the value they choose. must be between 0 and 5000

.damage 1234

	- sets the user's damage SR to the value they choose. must be between 0 and 5000

.dps 1234

	- shortcut for .damage

.tank 1234

	- sets the user's tank SR to the value they choose. must be between 0 and 5000

.queue tank/dps/support/fill

	- adds the user to the queue for the role they chose. fill will randomly pick a role that still needs players
	- if left blank (.queue), it will print out all users in the current queue

.q tank/dps/support/fill

	- shortcut for .queue

.roles

	- prints out how many of each role are still needed before a match can be made

.leave

	- leaves the queue

.l

	- shortcut for .leave

.sr

	- prints out the user's SR for each role

.coin

	- returns heads or tails at random
