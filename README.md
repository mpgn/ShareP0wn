### ShareP0wn (14,15)

ShareP0wn is basically this [metasploit module](https://github.com/0rigen/SharePwn_MSFModules) but in Python except a CSV is generated at the end. The tool analyse a list of SharePoint URL and retreive all possibles information about the version and the user rigths. Then a nice excel is generated to have a global vision. This tool can be used for blueteam as redteam.

After that, depending on the user rigths, the attacker cann use the default upload feature of SharePoint to upload a webshell. See the **After** part !  

## Getting Started

* Donwload the project
* Complete the file target_url.txt with all urls you want to check
* Complete the file user_list.txt with users you want to test
	- enter the user this order user1 < user2 < user3 in terms of rights
	- example: user1 can read file, user2 can edit file, user3 is an administrator
* `python ShareP0wn.py`
* A nice CSV will be created on the same directory
* Enjoy

## Informations

	* The script interpret the list of users like this : anonymous < user1 < user2 < user3 etc in terms of rights
	* If user anonymous can access to a ressource, the other users will not be checked, in the other case, user1 will be checked etc

The path_list.txt file can be filled with more path, full liste in can be found in the file all_path.txt.

## After

If you see this :
```
        200 USER /
        200 USER /_layouts/user.aspx
        200 USER /_layouts/userdisp.aspx?id=1
        200 USER /_layouts/sitemanager.aspx
```
You probably can upload a webshell in the document section !
https://www.helloitsliam.com/2015/04/30/sharepoint-security-and-a-web-shell/

If you see this :
```
        200 ANONYMOUS /
        200 ANONYMOUS /_layouts/userdisp.aspx?id=1
```

You can use the tool **get_user.py url max_id** to retrieve information about users.

## History

* 0.0.1
	* First release

## Credits

* [@mpgn_x64](https://twitter.com/mpgn_x64)
* [0rigen](https://github.com/0rigen)

## License

MIT License

