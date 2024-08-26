from  jinja2 import Template
from sqlalchemy import null
from application.workers import celery
import datetime
import smtplib
from celery.schedules import crontab
from flask_sse import sse
import requests

@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(hour=5, minute=00 , day_of_month=1), send_report.s(), name = '1st of every month at 5:00AM')
    sender.add_periodic_task(crontab(hour=17, minute=00), check_revised_reminder.s(), name = 'Daily reminder/check job at 5:00PM')
    # sender.add_periodic_task(crontab(hour=15, minute=7), send_report.s(), name = 'test task')

@celery.task()
def send_report():
    users=requests.get('http://localhost:8080/api/user')
    users=users.json()
    toMail=[]
    if users['status']=='success':
        users=users['data']
        for user in users:
            currentUserDecks=requests.get('http://localhost:8080/api/user/decks/'+str(user['user_id']), headers={"APItoken":user['api_key']})
            currentUserDecks=currentUserDecks.json()['data']
            reports={'visited_decks':[],'unvisited_decks':[],'never_visited_decks':[],'scores':{},'average_difficulty':{}}
            for cudeck in currentUserDecks:
                if cudeck['last_reviewed'] != 'None':
                    if ((datetime.datetime.now())-parser.parse(cudeck['last_reviewed'])) < datetime.timedelta(days=30):
                        reports['visited_decks'].append(cudeck['deck_name'])
                    else:
                        reports['unvisited_decks'].append(cudeck['deck_name'])
                else:
                    reports['never_visited_decks'].append(cudeck['deck_name'])
                reports['scores'][cudeck['deck_name']]=cudeck['total_score']
                if len(cudeck['cards'])>0:
                    avg_df=(cudeck['total_score']/len(cudeck['cards']))*10
                else:
                    avg_df=-1
                if avg_df>=0 and avg_df<35:
                    df='Hard'
                elif avg_df>=35 and avg_df<70:
                    df='Medium'
                elif avg_df>=70:
                    df='Easy'
                else:
                    df='No Cards'
                reports['average_difficulty'][cudeck['deck_name']]=df
            print(reports)
            toMail.append({'username':user['username'], 'email':user['email'], 'report':reports})
    with open("./templates/report_mail.html") as fil:
        template=Template(fil.read())
    for tom in toMail:
        mail_body=template.render(data=tom)
        job = send_mail.delay(to_addr=tom['email'], subject='Monthly report for Flash Card App for : '+datetime.datetime.now().strftime('%B-%Y'), body=mail_body)
    return('done sending report')

from dateutil import parser
@celery.task()
def check_revised_reminder():
    users=requests.get('http://localhost:8080/api/user')
    users=users.json()
    toMail=[]
    if users['status']=='success':
        users=users['data']
        for user in users:
            currentUserDecks=requests.get('http://localhost:8080/api/user/decks/'+str(user['user_id']), headers={"APItoken":user['api_key']})
            currentUserDecks=currentUserDecks.json()['data']
            unrevised_decks=[]
            for cudeck in currentUserDecks:
                if cudeck['last_reviewed'] != 'None':
                    if ((datetime.datetime.now())-parser.parse(cudeck['last_reviewed'])) > datetime.timedelta(hours=24):
                        unrevised_decks.append(cudeck['deck_name'])
                else:
                    unrevised_decks.append(cudeck['deck_name'])
            toMail.append({'username':user['username'], 'email':user['email'], 'decks':unrevised_decks})
    with open("./templates/reminder_mail.html") as fil:
        template=Template(fil.read())
    for tom in toMail:
        mail_body=template.render(data=tom)
        job = send_mail.delay(to_addr=tom['email'], subject='Daily reminder jobs Flash Card App', body=mail_body)
    return('sent reminders')

from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

@celery.task()
def send_mail(to_addr, subject=None, body='Default mail body', attachments=[]):
    message = MIMEMultipart("alternative")
    message['Subject']=subject
    filen = attachments
    message['From']="flashcardapp@yahoo.com"
    message['To']=to_addr  
    part=MIMEText(body, "html")
    message.attach(part)
    for f in filen:
        with open("./attachments/"+f, 'rb') as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            "attachment", filename=f
        )
        message.attach(part)
    try:
        smtpObj = smtplib.SMTP('smtp.mail.yahoo.com', 587)
        smtpObj.starttls()
        smtpObj.login('flashcardapp@yahoo.com', 'zqbltxqoachxlsth')
        smtpObj.send_message(message)  
        smtpObj.quit()       
        print("Successfully sent email")
    except:
        print("Error: unable to send email")
    return('Done sending mail ')

@celery.task()
def export_deck(deck_id, user_id, apit):
    deck = requests.get('http://localhost:8080/api/decks/'+str(deck_id)+"?user_id="+str(user_id), headers={'APItoken':apit})
    deck =deck.json()['data']
    filename = "export-"+str(deck['deck_name'])+str(datetime.datetime.now().strftime("%d-%m-%Yat%H:%M:%S"))+".csv"
    with open("exports/"+filename, 'w') as f:
        f.write('Deck ID'+','+ str(deck.get('deck_id'))+"\n")
        f.write('User ID'+','+ str(deck.get('user_id'))+"\n")
        f.write('Deck Name'+','+ str(deck.get('deck_name'))+"\n")
        f.write('Total Score'+','+ str(deck.get('total_score'))+"\n")
        f.write('Last Reviewed'+','+ str(deck.get('last_reviewed'))+"\n")
        f.write('Cards'+"\n")
        f.write('Front, Back, Card Score'+"\n")
        for card in deck.get('cards'):
            f.write(str(card.get('front'))+','+str(card.get('back'))+','+str(card.get('card_score'))+"\n")

    sse.publish({"status":"success","message":"done export", "file_name":filename}, type='export-tasks')
    return('done exporting')
import csv
@celery.task()
def import_deck(filename, user_id, apit):
    data=[]
    f = open("imports/"+filename, 'r')
    csvreader = csv.reader(f)
    for row in csvreader:
        data.append(row)
    print(data)
    data_dct={}
    i=0
    for r in range(len(data)):
        i=r
        cd=[]
        if data[r][0] == 'Deck Name':
            data_dct['deck_name']=data[r][1]
        if data[r][0] == 'Cards':
            i+=2
            while i < len(data):
                if data[i][0][0] == '#':
                    break
                cd.append([data[i][0],data[i][1]])
                i+=1
            data_dct['cards']=cd
    if not data_dct['deck_name']:
        sse.publish({"status":"error","message":"error in csv"}, type='import-tasks')
        return 'error in csv'
    
    res = requests.post("http://10.1.1.43:8080/api/decks?user_id="+str(user_id), json={'deck_name':data_dct['deck_name']}, headers={'APItoken':apit})
    res=res.json()
    if res['status'] == 'error':
        sse.publish({"status":"error","message":'some error occured : '+res['message']}, type='import-tasks')
        return 'some error occured : '+res['message']
    di=res['deck_id']
    for c in data_dct['cards']:
        res = requests.post("http://10.1.1.43:8080/api/cards?user_id="+str(user_id), json={'front':c[0], 'back':c[1], 'deck_id':di}, headers={'APItoken':apit})
    sse.publish({"status":"success","message":"done import"}, type='import-tasks')
    return ("done imports")