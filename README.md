# CSE546-Calorie-Counter

Web tier:
-	Unzip Calorie Counter folder.  Go to frontend folder (which contains react application) and run “npm install”. Make sure npm is installed in the machine. Node version v14.15.4 was used for the application.
-	Run “npm run build” from frontend folder. build folder will be created. Copy all the contents from build folder to views folder present in frontend. 
-	Go to Calorie Counter folder (which contains express application)  from terminal and run “npm install”.
-	Set environment variables to run google application. Hit below command to set env variables: $env:GOOGLE_APPLICATION_CREDENTIALS="config\creds.json" (path to main_folder/config/creds.json)
-	To run the main application go to Calorie Counter folder and run “npm start” and application will be accessible at “http://localhost:3001/” 

App tier:
-	Unzip gcp-calorie folder. This contains the main.py and requirements.txt files.
-	Create a cloud function and set the trigger for cloud storage and select the bucket.
-	In the code section, select Python 3.9. Copy the code to main.py and requirements.txt respectively.
- Deploy the cloud function.
