import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time
import re
from ..constant import paths
from ..service.constant_service import ConstantService


class MailUtilities(object):
    @staticmethod
    def send_success_notification(emails, download_link, start_dt):
        raw_body = '''
        <body style="font-family:arial;">
                      Dear <span>friends</span>,<br><br>

                    <table style="text-align:left;width:100%;font-family:arial">
                         <tr>
                            <td style="padding-bottom:10px;">{head_message}</td>
                         </tr>
        				 <tr>
                            <td style="padding-bottom:10px;">Status: {status}</td>
                         </tr>
                         <tr>
                            <td style="padding-bottom:10px;">Download Link: {download_link}</td>
                         </tr>
        				 <tr>
                            <td>Start Date/Time : {dt}</td>
                         </tr>
                         <tr>
                            <td>End Date/Time : {dtt}</td>
                         </tr>

                    </table>
                        <br><br><br><br><br><br><br>
        				Regards,
                        <br><span style="color:#0073A5"> Social Media Scraping</span>
                        <br><span style="color:#0073A5">(Social Media Scraping-Platform)</span>
                </html>
        '''
        now = datetime.datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

        # head_message = "Xignite {type} process has been started."
        head_message = "Social Media Scraping Completed"

        status = "Completed"

        to = emails
        cc = ConstantService.cc_mail_id()
        subject = " Social Media Scraping Completed Notification - Success"

        head_message.format(type="Quarterly")
        body = raw_body.format(head_message=head_message, status=status, download_link=download_link,
                               dt=start_dt, dtt=dt_string)

        MailUtilities.sendHtmlMail(to, cc, subject, body)

    @staticmethod
    def send_failed_notification(emails, error_log, start_dt):
        raw_body = '''
        <body style="font-family:arial;">
                      Dear <span>friends</span>,<br><br>

                    <table style="text-align:left;width:100%;font-family:arial">
                         <tr>
                            <td style="padding-bottom:10px;">{head_message}</td>
                         </tr>
        				 <tr>
                            <td style="padding-bottom:10px;">Status: {status}</td>
                         </tr>
                         <tr>
                            <td>Start Date/Time : {dt}</td>
                         </tr>
                         <tr>
                            <td>End Date/Time : {dtt}</td>
                         </tr>
                         <tr>
                            <td style="padding-bottom:10px;"><br>Error Log: {download_link}</td>
                         </tr>


                    </table>
                        <br><br><br><br><br><br><br>
        				Regards,
                        <br><span style="color:#0073A5"> Social Media Scraping</span>
                        <br><span style="color:#0073A5">(Social Media Scraping-Platform)</span>
                </html>
        '''
        now = datetime.datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

        # head_message = "Xignite {type} process has been started."
        head_message = " Social Media Scraping has failed."

        status = "Failed"

        to = emails
        cc = ConstantService.cc_mail_id()
        subject = "  linkedin Scraping Notification - Failed"

        head_message.format(type="Quarterly")
        body = raw_body.format(head_message=head_message, status=status,
                               dt=start_dt, dtt=dt_string, download_link=error_log)

        MailUtilities.sendHtmlMail(to, cc, subject, body)

    @staticmethod
    def sendPlainMail(to=None, cc=None, subject=None, body=None):

        status = False

        frm = "no-reply@kognetics.com"
        all_add = cc.split(',') + [to]
        msg = MIMEMultipart()
        msg['From'] = frm
        msg['To'] = to
        msg['Cc'] = cc
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))
        text = msg.as_string()
        try:
            s_mail = smtplib.SMTP("smtp.gmail.com", 587)
            s_mail.set_debuglevel(2)
            s_mail.ehlo()
            s_mail.starttls()
            s_mail.ehlo()
            s_mail.login("no-reply@kognetics.com", "app@mail@1987")
            time.sleep(3)
            s_mail.sendmail(frm, all_add, text)
            status = True
            print("Email has been sent")
            '''logger.logg(debug_msg='Error while sending mail.',
                        info_msg='Mail has been sent',
                        warning_msg=None,
                        error_msg='Module = ' + "mailer.py",
                        critical_msg=None)'''
        except Exception as e:
            ''' logger.logg(debug_msg='Error while sending mail.',
                         info_msg='Mail could not be sent',
                         warning_msg='Error in sending mail',
                         error_msg='Module = ' + "mailer.py",
                         critical_msg=str(e))'''

        return status

    @staticmethod
    def sendHtmlMail(to=None, cc=None, subject=None, body=None):

        status = False
        # logger = Logger()

        frm = "no-reply@kognetics.com"
        all_add = cc.split(',') + [to]
        msg = MIMEMultipart()
        msg['From'] = frm
        msg['To'] = to
        msg['Cc'] = cc
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'html'))
        text = msg.as_string()
        try:
            s_mail = smtplib.SMTP("smtp.gmail.com", 587)
            s_mail.set_debuglevel(2)
            s_mail.ehlo()
            s_mail.starttls()
            s_mail.ehlo()
            s_mail.login("no-reply@kognetics.com", "app@mail@1987")
            time.sleep(3)
            s_mail.sendmail(frm, all_add, text)
            status = True
            print("Email has been sent")
            '''logger.logg(debug_msg='None.',
                        info_msg='Mail has been sent',
                        warning_msg="None",
                        error_msg='Module = ' + "mailer.py",
                        critical_msg="None")'''
        except Exception as e:
            pass
            '''logger.logg(debug_msg='Error while sending mail.',
                        info_msg='Mail could not be sent',
                        warning_msg='Error in sending mail',
                        error_msg='Module = ' + "mailer.py",
                        critical_msg=str(e))'''

        return status

    @staticmethod
    def validate_email(input_email):
        reg = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
        if re.fullmatch(reg, input_email):
            return True
        else:
            return False
