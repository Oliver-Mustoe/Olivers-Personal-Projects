This page contains personal notes while creating my projects
<!--
# Entry 10/15/22 & 10/16/22
## The Moving of the Github: Part 1
Began working on the migration of my Github from wiki to repo. My first roadblock is that most of my wiki files contain ':' in the name and windows cannot download those files, so moving into my repo would be dangerous.

I have just began to fix this with the following step:
1. Make a Linux VM (Xubuntu) and download the wiki their
2. Create a script to parse the files and rename them/rename references

This began well as I created the VM, but took a sudden turn when I actually looked through the process of renaming the files :(.

After some time researching the various renaming file programs for linux, I settled on [rename](https://learnbyexample.github.io/learn_perl_oneliners/perl-rename-command.html) (perl version) and created the following script to rename the files:
```
#!/bin/bash
# V0.4

# Fix the colons in Github files names & content
# Install needed software
sudo apt install rename -y
# Ask for a directory, save in $gdir
echo "Please input the name of the folder with the markdown files WITH NO '/' (MUST BE IN THE SAME DIRECTORY AS SCRIPT!!!)"
read gdir
#Use the rename command to substitute all ':' to a '='
rename -n -v 's/:+/=/' $gdir/*
read -p "Approve these changes: [y/N]" user_inp1

# Based on user input, either rename or exit
if [[ ${user_inp1^^} == "Y" ]]; then
	#rename -n -v 's/:/=/' $gdir/*
	echo "TEST COMPLETE"
else
	echo "ABORTED OPERATION--REASON: USER INPUT"
fi
# Todo:
# Use the rename in the if statement (not currently used because I dont want to rename yet)
# Find out how to parse and replace text (awk?!?)
# - Will have to be more precise than filenames as it can contain the colons but we are correcting references
# See if I can make it so that all instances of the ':' are replaced in the filenames -- NOT A PRIORITY!!!
```

As the todo's mention, next I have to go through the process of actually parsing the markdown files themselves for broken references.

Overall, I have learned A LOT about how to mass rename files in Linux (which before this I only really had a little experience with ```mv```) and am excited to see where this project takes me!

### Hardships
Majorly, all of the hardships I faced in this beginning of the script was having to learn more about renaming Linux files then I ever had to. This caused a lot of rabbit holes to be gone into, which sucked up a lot of time. As this is a personal project and not time-restrained, I actually enjoyed learning about some stuff I did not know (I was originally gonna use awk for some stuff, but I can probably use that knowledge further in the script!)

### Sources used on this entry
* https://linuxhint.com/bash_lowercase_uppercase_strings/#:~:text=You%20can%20convert%20the%20case,whole%20string%20to%20the%20uppercase.
* https://askubuntu.com/questions/431128/capture-groups-are-ignored-when-renaming-files
* https://stackoverflow.com/questions/57782374/rename-file-directory-name-in-linux
* https://learnbyexample.github.io/learn_perl_oneliners/perl-rename-command.html
* https://superuser.com/questions/70217/is-there-a-linux-command-like-mv-but-with-regex


# Entry 10/17/22
## The Moving of the Github: Part 2
Updated code:
```
#!/bin/bash
# V0.6

# Fix the colons in Github files names & content
# Install needed software
sudo apt install rename -y
file_rename () {
# Function to rename a directory of files that have colons in them to '='

	# Create a while loop to use find and egrep to check for colons until rename changes them all
	while [[ -n $(find $gdir|egrep ':+') ]]; do
		#Use the rename command to substitute all ':' to a '='
		rename -n -v 's/:+/=/' $gdir/*
		read -p "Approve these changes: [y/N]" user_inp1
		
		# Based on user input, either rename or exit
		if [[ ${user_inp1^^} == "Y" ]]; then
			#rename -n -v 's/:/=/' $gdir/*
			echo "TEST COMPLETE"
		else
			echo "ABORTED OPERATION--REASON: USER INPUT"
			break
		fi
done
}

parse_rename () {
 #Function to parse a directorys files and rename all markdown links with colons to '='
	echo 'COMING SOON'
}

main () {
# Main function for options and intro screen
# -e for \ enabling
echo -e "\nWelcome to Olivers Github fixer for colons!
Have you or a loved one ever put a colon for a markdown file and now want it removed?
Yes, then use this use this program TODAY:
1. Full process (rename files in a directory AND parse through them and rename any links to markdown files)
2. Just file rename
3. Just link fix
4. Exit\n"
read -p 'Selection: ' user_select

# switch based upon $user_select
case $user_select in
	# Since all 3 options need the directory, have any selected option first grab it
	1 | 2 | 3)
		# Ask for a directory, save in $gdir
		echo -e "\nPlease input the name of the folder with the markdown files WITH NO '/' (MUST BE IN THE SAME DIRECTORY AS SCRIPT!!!)"
		read gdir
		;;&
	1)
		file_rename
		parse_rename
		;;
	2)
		file_rename
		;;
	3)
		parse_rename
		;;
	*)
		echo "EXITING"
		;;
esac
}
# Start function call
main

# Todo:
# Use the rename in the if statement (not currently used because I dont want to rename yet)
# Find out how to parse and replace text (awk?!?)
# - Will have to be more precise than filenames as it can contain the colons but we are correcting references
# See if I can make it so that all instances of the ':' are replaced in the filenames -- NOT A PRIORITY!!! (maybe fixed with egrep)
```

Today was mostly a formatting day (having everything in functions) and incorporating user input and usability into the program with a case statement (essentially a switch statement). No hardships, just looking up syntax mostly and how to use case statements. 

Hope to soon move into the file parsing, and the actual move!!!

### Sources used in this entry:
* https://linuxhint.com/echo-newline-bash/
* https://unix.stackexchange.com/questions/577603/possible-to-match-multiple-conditions-in-one-case-statement
* https://stackoverflow.com/questions/23564995/how-to-modify-a-global-variable-within-a-function-in-bash
https://linuxize.com/post/bash-case-statement/



# Put the stuff here
>