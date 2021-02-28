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
then choose your bucket from the previous step and as key I choose dht/${timestamp()}.
and the role I gave is AWSIOT_S3_FULL. 
the data you send should now appear in your bucket.


