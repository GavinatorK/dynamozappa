import smtplib


def send_email(to, subject):

    fromaddr = "rkadiyala@merkleinc.com"
    toaddrs  = to
    subject = subject
    msg = '''
        From: {fromaddr}
        To: {toaddr}
        Subject:testin'
        "this is a test"
    '''
    msg = msg.format(fromaddr =fromaddr, toaddr = toaddrs, subject=subject)
    # The actual mail send
    server = smtplib.SMTP('merkleinc-com.mail.protection.outlook.com:25')
    server.starttls()
    server.ehlo("merkleinc.com")
    server.mail(fromaddr)
    print toaddrs
    server.rcpt(toaddrs)
    server.data(msg)
    server.quit()

if __name__ == '__main__':
    send_email("rkadiyala@merkleinc.com", "test with merkle")
