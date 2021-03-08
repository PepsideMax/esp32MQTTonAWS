# esp32MQTTonAWS

to make this project you will need:
activated AWS account 
esp32
dht11/22

In aws IoT we start by creating a thing in the manage things tab. The name of this thing is not important just see that you remember it. 
In the next step you can ignore most of the things there. Afterwards you create a new certificate for this thing and download the 3 keys you are given and put these in a safe place. These could put your data at risk if you give them to anyone. 

Click on the activate button below and the download link for the root CA for AWS IoT there you will need to get the amazon root CA 1.

Once you have done this open the .ino file from this project. In this file you should not change a thing. Unless you want to change the used pins or the dht type.
then in the same folder you create a secrets.h file according to the example found. the topics there refer to a topic on the mqtt server and will decide where your data will be stored. 
after including all the information we are gonna need the keys we got earlier when creating our thing, these can just be opened in notepad.
The first key is the last key we downloaded and should have a name with root and ca 1 in it. The second will have certificata.perm.crt.txt in its name. 
the last will have private perm in the name. one you filled these in you can upload the code.

If this works you will get an AWS IoT connected! message on your serial monitor. 

Now on AWS go to the S3 section and here we are going to make a bucket for this you just choose and the server to store the bucket at the smartest choice here is to use the same server as the one where your thing is located. 

now go back to AWS IoT and in act got ot rules here you have to add a new rule here you choose a rule name and in the select * from you change the iot/topic to the before chosen mqtt topic in your secrets.h. 
After this go to add action here you select store message in amazon s3 bucket.
then choose your bucket from the previous step and as key I choose data/${device_id}_${topic()}/${timestamp()}.
and the role I gave is AWSIOT_S3_FULL. 
the data you send should now appear in your bucket.

# part 2 cloud api

Now we are storing the data on a bucket yet this is not ideal so now create an EC2 virtual machine on aws. In my application I used an ubuntu server 
with the t2 micro tear this is one of the verry cheap tears and even free if you play your cards right. The rest you can mostly ignore except for the 6ste step here you have to add http and https (port 80 and 443 do not remove the port 22 connection). 
After clicking confirm you have the option to add a pair key or use an existing one the safest option is to generate a new one. So just give it a name and download your freshly generated key. don’t forget to download it else there is no easy way to recover it.
Ifi things still are as when i did it you now have an outdated key with a different extension then .ppk if you did get a ppk file you don’t have to do this next strep.
First you have to download PuTTY and open PuTTYgen one you open PuTTYgen your klick load and open the key file you just got. It will give you some warnings just ignore them and continue. Now save this key under the same name as the previous key. 
Now go back to aws EC2 where you can find the ip address of your virtual machine.
Now open up PuTTY select ssh as connection type and put in the IP you just got from AWS.
Before you can open the connection on the left side you see a menu here go into ssh and click on auth here click browse and select the file you got from PuTTYgen. 
now you should be able to open a connection using the open button. 

Now you login with the username ubuntu.

Now start by doing the sudo apt-get update and upgrade

When this is finished, do the following commands to get an apache server running and a database.

sudo apt install apache2
sudo apt install mysql-server
sudo apt install php libapache2-mod-php php-mysql
sudo chmod 777 /var/www/html
sudo systemctl restart apache2
sudo apt install certbot
sudo apt install python3-certbot-apache

sudo mysql

now you have entered the mysql command line
now follow these steps (can also be found in the sql.txt file)
everything in [] should be changed to something of your choice. do remember these because we will be needing them for your secrets file.


CREATE DATABASE [DATABASENAME];
  
CREATE USER '[USERNAME]'@'localhost' IDENTIFIED BY '[PASSWORD]';
  
GRANT ALL PRIVILEGES ON [DATABASENAME].* TO '[USERNAME]'@'localhost';
  
FLUSH PRIVILEGES;

USE [DATABASENAME];
  
CREATE TABLE esp32 (  
ID INT NOT NULL AUTO_INCREMENT,  
Device_id VARCHAR (100) NOT NULL,  
Temperature Float,  
Humidity Float,  
Datetime DATETIME DEFAULT CURRENT_TIMESTAMP,
PRIMARY KEY (ID)  
); 

quit

Now you have made a database for your data to test if this was done correctly, copy/create the test.php and mysql_connect.php from the cloud_api folder to the /var/www/html directory. 
In this same directory you create a secrets.php from the example_secrets in the cloud_api.

Now in your web browser you can test if this works by surfing to your ip followed by /test.php.

Now to make your connection https instead of http you need to create an account on the noip https://www.noip.com/. Here we create a dns for your ip by clicking the create hostname button.
After choosing the best hostname click on it in the no-ip hostname list and putting in your virtual machine ip as the destination. Do take notice that if your machine is closed you will have to do this step gain if you want this domain to keep on working. To solve this follow this link:
https://www.noip.com/support/knowledgebase/installing-the-linux-dynamic-update-client-on-ubuntu/ 
(sudo apt install make &  gcc)

Now to actually get certified we need to use certbot just use the ‘sudo certbot --apache’ command and fill in your information and at the end select option 2 to force everyone to use https.

Now for the finishing touches add the api.php file and list.php files to the var/www/html folder.

To now make aws send your data to the correct location go back to the rule we made in part 1 and add a new action to this rule a http action withe as link your very amazing link followed by /api.php. and three headers withe the keys: device_id, temperature and humidity and values: ${devide_id}, ${temperature} and ${humidity} respectively.

Now by opening your site followed by list.php you should see your esp32 data.

