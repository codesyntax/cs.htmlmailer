__doc__ = """ Mailer stolen from collective.singing """

from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate
from email.utils import make_msgid
from html.parser import HTMLParser


class HTMLFilter(HTMLParser):
    text = ""
    anchorlist = []

    def handle_data(self, data):
        self.text += data

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            for key, value in attrs:
                if key == "href":
                    self.anchorlist.append(value)


def create_html_mail(
    subject,
    html,
    text=None,
    from_addr=None,
    to_addr=None,
    cc_addrs=[],
    headers=None,
    encoding="UTF-8",
):
    """Create a mime-message that will render HTML in popular
    MUAs, text in better ones.
    """
    # Use DumbWriters word wrapping to ensure that no text line
    # is longer than plain_text_maxcols characters.
    plain_text_maxcols = 72

    if text is None:
        # Produce an approximate textual rendering of the HTML string,
        # unless you have been given a better version as an argument
        parser = HTMLFilter()
        parser.feed(html)
        parser.close()

        # append the anchorlist at the bottom of a message
        # to keep the message readable.
        anchorlist = "\n\n" + ("-" * plain_text_maxcols) + "\n\n"
        for counter, item in enumerate(parser.anchorlist, start=1):
            anchorlist += "[%d] %s\n" % (counter, item)

        text = parser.text + anchorlist

    # if we would like to include images in future, there should
    # probably be 'related' instead of 'mixed'
    msg = MIMEMultipart("mixed")
    # maybe later :)  msg['From'] = Header("%s <%s>" % (send_from_name, send_from), encoding)
    msg["Subject"] = Header(subject, encoding)
    msg["From"] = from_addr
    msg["To"] = to_addr
    if cc_addrs:
        msg["Cc"] = ", ".join(cc_addrs)
    msg["Date"] = formatdate(localtime=True)
    msg["Message-ID"] = make_msgid()
    if headers:
        for key, value in headers.items():
            msg[key] = value
    msg.preamble = "This is a multi-part message in MIME format."

    alternatives = MIMEMultipart("alternative")
    msg.attach(alternatives)
    alternatives.attach(MIMEText(text, "plain", _charset=encoding))
    alternatives.attach(MIMEText(html, "html", _charset=encoding))

    return msg
