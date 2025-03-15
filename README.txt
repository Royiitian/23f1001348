extract both `zip` files in separate folders.

for backend ("the one with the python files") :
	open the project using > right click > open with vscode
	open the terminal > ctrl+` (control + backtick)

	enter the following commands:
	python -m venv .venv
	.\.venv\Scripts\activate
	pip install -r requirements.txt

	To run the project:
	python app.py

for frontend ("the one with the vue components/files") : 
	open the project using > right click > open with vscode
	open the terminal > ctrl+` (control + backtick)
	
	enter the following commands:
	npm install

	to start the project:
	npm run serve
	then ctrl+click on the localhost link (for local PC), or the network link (the one with the IP) for network hosting (LAN hosting)
	


these steps complete the installation and running of the main backend/frontend

Celery and Redis for auto mailing:


	

	before starting up with this section, make sure you have your app password and mail entered in the sender password field and the sender mail field,
	to get the app password, go to your google account > profile icon > manage your google account > search for app password > click on App passwords (security) > enter your app name > 	click on create > copy your app password > enter it in the backend send_email.py file.



	install wsl (for windows), if on any linux distro, no need
	after downloading wsl, run command `wsl --install -d Ubuntu-24.04`
	after installation, complete the remaining setup steps for registration of new ubuntu user (self explanatory)
	in the ubuntu terminal, enter:
		sudo apt update
		sudo apt install redis
		to verify redis installation: redis-cli --version
		check if redis has started, to do so, enter `redis-cli ping` terminal should output "PONG"
		if not started then use `sudo service redis-server start`
		then test again.

	once redis starts up, go to vscode where the backend project is opened up
		open up a new terminal
		enter `	.\.venv\Scripts\activate`
		then `celery -A tasks worker --loglevel=info --pool=gevent --concurrency=5`
		the above command should start the worker, if you do not see the word "ready" on any line, then close the terminal and repeat steps after closing current terminal and opening new terminal
		before running the next script, in the `celery_config.py`, replace the `1` in '*/1' with the number of minutes after which you want the task to repeat, for example, 1440 for 24 hours
		then open a new terminal and enter `.\.venv\Scripts\activate`
		then enter `celery -A celery_config beat --loglevel=info -l debug` this command should start the repeating job



with this the whole project is running, note, before finalising these steps, i suggest repeating them in another directory.


IF ANY PACKAGE IS MISSING, SIMPLY INSTALL IT BY USING `pip install <package_name>' for the backend, `npm install <package_name>` for the frontend
