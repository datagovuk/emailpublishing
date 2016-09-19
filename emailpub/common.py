import email
import poplib
import smtplib
from datetime import timedelta, datetime
from random import randint
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import config
import scraperwiki

from jinja2 import Environment, PackageLoader

env = Environment(loader=PackageLoader('emailpub', 'templates'))

""" Strips the email part from one that looks like
    NAME <email> """
def raw_email(addr):
    if '<' in addr:
        email = addr[addr.index("<")+1:-1]
    else:
        email = addr

    return email

""" Strips the token from an email address, where the token
    is in the +part of the address """
def token_from_email(email):
    if not '+' in email:
        return ''
    at = email[0:email.index("@")]
    return at[at.index('+')+1:]

""" Given an email address and the name of a dataset, will return a
newly formatted email address with a token inserted """
def generate_token_and_address(email, dataset):
    import uuid

    d = {
        "token": str(uuid.uuid4()),
        "email": email,
        "dataset": dataset
    }
    scraperwiki.sql.save(["token"], d, table_name="tokens")

    address = config.this_email()
    at = address.index("@")
    new_address = address[0:at] + "+{}".format(d['token']) + address[at:]

    return new_address

""" Given a token and a user's email address, will either fail to validate
or will return the name of the dataset the user is working with """
def validate_token(token, user_email):
    res = scraperwiki.sql.select("* FROM tokens WHERE token=?", [token])
    if not res:
        return False, None

    record = res[0]
    if record['email'] != raw_email(user_email):
        return False, None

    return True, record['dataset']


"""
Get the latest n messages from the POP3 server.
"""
def get_latest_messages(n=10):
    messages = []
    settings = config.incoming_mail()

    pop = None
    if settings.get('tls'):
        pp = poplib.POP3_SSL
    else:
        pp = poplib.POP3

    pop = pp(settings.get('host'), settings.get('port'))
    pop.set_debuglevel(1)

    pop.user(settings.get('username'))
    pop.pass_(settings.get('password'))

    fetch_count = n
    (message_count, _) = pop.stat()
    if message_count < n:
        fetch_count = message_count

    for i in range(1, fetch_count+1):
        stat, content_lines, size = pop.top(i, 111000)
        mail = email.message_from_string('\n'.join(content_lines))
        messages.append(mail)

    pop.rset()
    pop.quit()

    return messages


def send_notification(email, frm):
    settings = config.outgoing_mail()

    template_html = env.get_template('notification.html')
    rendered_html = template_html.render().encode('utf-8')

    template_text = env.get_template('notification.txt')
    rendered_text = template_text.render()

    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Dataset due for update"
    msg['From'] = frm
    msg['To'] = email

    msg.add_header('reply-to', frm)

    part1 = MIMEText(rendered_text, 'plain')
    part2 = MIMEText(rendered_html, 'html')

    msg.attach(part1)
    msg.attach(part2)

    sc = None
    if settings.get('tls'):
        sc = smtplib.SMTP_SSL
    else:
        sc = smtplib.SMTP

    s = sc(settings.get('host'))
    s.ehlo_or_helo_if_needed()

    s.login(settings.get('username'), settings.get('password'))
    s.sendmail(frm, email, msg.as_string())
    s.quit()

""" Generate a schedule for the user with the given email address """
def generate_schedule(email):
    datasets = config.get_datasets()

    settings = config.outgoing_mail()

    template_html = env.get_template('schedule.html')
    rendered_html = template_html.render(datasets=datasets).encode('utf-8')

    template_text = env.get_template('schedule.txt')
    rendered_text = template_text.render(datasets=datasets)

    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Publishing Schedule"
    msg['From'] = config.this_email()
    msg['To'] = email

    part1 = MIMEText(rendered_text, 'plain')
    part2 = MIMEText(rendered_html, 'html')

    msg.attach(part1)
    msg.attach(part2)

    sc = None
    if settings.get('tls'):
        sc = smtplib.SMTP_SSL
    else:
        sc = smtplib.SMTP

    s = sc(settings.get('host'))
    s.ehlo_or_helo_if_needed()
    s.login(settings.get('username'), settings.get('password'))
    s.sendmail(config.this_email(), email, msg.as_string())
    s.quit()

""" Pick a random date between two provided dates """
def random_date(start, end):
    res = start + timedelta(
        seconds=randint(0, int((end - start).total_seconds())))
    return res.strftime("%d/%m/%Y")