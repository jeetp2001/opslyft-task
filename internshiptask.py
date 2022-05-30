import json
import boto3
import imaplib
import smtplib
from email.mime.text import MIMEText
import email
from datetime import timedelta, datetime
import datetime
from dateutil import parser
from boto3.dynamodb.conditions import Key

username = 'jeetrpatel2001@gmail.com'
password = '********'
imapserver = imaplib.IMAP4_SSL('imap.gmail.com')
imapserver.login(username,password)

ec2 = boto3.resource('ec2')
dynamodb = boto3.resource('dynamodb')
events = boto3.client('events')
lambdaclient = boto3.client('lambda')

def send_mail(sentto,sentsubject,msg):
    # gmail_user = username
    # gmail_paas = password
    server = smtplib.SMTP_SSL('smtp.gmail.com',465)
    server.ehlo()
    server.login(username,password)
    # sent_from = username
    # sent_to = sentto
    sent_subject = sentsubject
    sent_body = "this is body"
    message = MIMEText(msg)
    message['Subject'] = sent_subject
    message['To'] = sentto
    message['From'] = username
    server.sendmail(username, sentto, message.as_string())


def lambda_handler(event, context):
    timenow = datetime.datetime.now()
    
    h = timenow.hour

    taglist = ['Name','Key1']
    instanceids = []
    table = dynamodb.Table("instance-info")
    values = table.scan()
    dynamoids = []
    for i in values['Items']:
        dynamoids.append(i['insid'])
    
    for instance in ec2.instances.filter(Filters=[{'Name': 'instance-state-name','Values':['running','stopped']}]):
        absenttags = []
        tags = []
        sentto = ''
        for i in instance.tags:
            if i['Key']=='created by':
                sentto += i['Value']
            tags.append(i['Key'])
        for j in taglist:
            if j not in tags:
                absenttags.append(j)
        
        
        if absenttags != []:
            sentsubject = "Please tag your EC2 instance of Id : "+instance.id
            msg ='Your EC2 instance of ID : '+instance.id+' does not contain the following tags : \n'+str(absenttags)
            send_mail(sentto,sentsubject,msg)
            for ids in dynamoids:
                if ids==instance.id:
                    break
            else:
                print('hello')
                instanceids.append(instance.id)
                if 'autoterminate' not in tags:
                    ec2.create_tags(Resources=[instance.id], Tags=[{'Key': 'autoterminate', 'Value':'yes'}])
                print('mail sent successfully...')
                res, messages = imapserver.select('"[Gmail]/Sent Mail"')
                status, msg = imapserver.search(None,'TO "%s" SUBJECT "Please tag your EC2 instance of Id : %s"'%(sentto,instance.id))
                l = msg[0].split()
                if l != []:
                    l1 = l[0].decode("utf-8")        
                    res, data = imapserver.fetch(l1,'(RFC822)')
                    email_message = data[0][1].decode('utf-8')
                    message = email.message_from_string(email_message)
                    date = message['Date']
                    date = parser.parse(date)
                    date = date + timedelta(hours=7)
                    date = date + timedelta(hours=6)
                    hour = date.strftime("%H")
                    minutes = date.strftime("%M")
                    day = date.strftime("%d")
                    month = date.strftime("%m")
                    year = date.strftime("%Y")
               
    resp = table.query(KeyConditionExpression=Key('hour').eq('%s'%(h)))

    if resp['Items'] == []:
        for i in instanceids:
            table.put_item(Item={'hour': '%s'%(hour),'insid': '%s'%(i)})
        # response = events.put_rule(Name='lambdascheduler%s'%(minutes),ScheduleExpression='cron(%s %s %s %s ? %s)'%(int(minutes),int(hour),int(day),int(month),int(year)),State='ENABLED')
        # response = events.put_targets(Rule = 'lambdascheduler%s'%(minutes), Targets=[{'Arn': 'arn:aws:lambda:ap-south-1:453343253242:function:terminate-ec2', 'Id': '1'}])
    for k in resp['Items']:
        for i in instanceids:
            if k['insid'] != i:
                table.put_item(Item={'hour': '%s'%(hour),'insid': '%s'%(instance.id)})
    for i in instanceids:
        if i not in dynamoids:
            response = events.put_rule(Name='lambdascheduler%s'%(hour),ScheduleExpression='cron(%s %s %s %s ? %s)'%(int(minutes),int(hour),int(day),int(month),int(year)),State='ENABLED')
            response = events.put_targets(Rule = 'lambdascheduler%s'%(hour), Targets=[{'Arn': 'arn:aws:lambda:ap-south-1:453343253242:function:terminate-ec2', 'Id': '1'}])            
            break
    data2 = events.describe_rule(Name="lambdascheduler%s"%(hour))
    lambdaclient.add_permission(FunctionName='arn:aws:lambda:ap-south-1:453343253242:function:terminate-ec2', StatementId='%s'%(h),Action='lambda:InvokeFunction',Principal='events.amazonaws.com',SourceArn=data2['Arn'])
    
            
        
    
    
    
