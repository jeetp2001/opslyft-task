# opslyft-task

This repository contains two lambda functions.<br>
Steps for creating lambda function:
1) Navigate to the AWS Lambda console
2) Click on the 'Create function' button
3) Provide the basic information like function name, runtime i.e. programming language, architecture and click on 'Create function'.
4) Navigate to the code section and modify the function code.
5) Go to the configuraton section if you want to add permissions to the lambda function.
<br>

-> The internshiptask lambda function contains the code for sending mail, storing instance id to dynamodb and creating cloudwatch events.
-> The terminate-ins lambda function contains the code for terminating the ec2 instance according to thier id
