# opslyft-task

This repository contains two lambda functions.<br>
Steps for creating lambda function:
1) Navigate to the AWS Lambda console
2) Click on the 'Create function' button
3) Provide the basic information like function name, runtime i.e. programming language, architecture and click on 'Create function'.
4) Navigate to the code section and modify the function code.
5) Go to the configuraton section if you want to add permissions to the lambda function.
<br>

-> The internshiptask lambda function contains the code for sending mail, storing instance id to dynamodb and creating cloudwatch events.<br>
-> The terminate-ins lambda function contains the code for terminating the ec2 instance according to thier id<br>
-> Another Cloudwatch event is also created for executing the lambda function every hour.


The execution of function:<br>
-> I created a dynamodb table for storing the insatnce id.<br>
1) First the 'internshiptask' lambda function will run and check the tags of the ec2 instances present.
2) If the tagging criteria is not fullfilled then it will send a mail to that particular instance and will add that instance into dynamodb table.
3) After this, it will create a cloudwatch event which is scheduled 6 hours after sending the mail to ec2 instance and this event will call another lambda function which will extract the instance id from dynamodb table and terminate it.
4) This lamnda function will execute every hour with the help of cloudwatch event.
5) This whole task is included in free tier. 
