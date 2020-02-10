__doc__ = """ Mailer stolen from collective.singing """

from email.Header import Header
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.Utils import formatdate
from types import UnicodeType

import email
import formatter
import htmllib
import StringIO


class HTMLMustBeUnicodeException(Exception):
    pass


class TextMustBeUnicodeException(Exception):
    pass


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

    if type(html) is not UnicodeType:
        raise HTMLMustBeUnicodeException

    html = html.encode(encoding)
    if text is None:
        # Produce an approximate textual rendering of the HTML string,
        # unless you have been given a better version as an argument
        textout = StringIO.StringIO()
        formtext = formatter.AbstractFormatter(
            formatter.DumbWriter(textout, plain_text_maxcols)
        )
        parser = htmllib.HTMLParser(formtext)
        parser.feed(html)
        parser.close()

        # append the anchorlist at the bottom of a message
        # to keep the message readable.
        counter = 0
        anchorlist = "\n\n" + ("-" * plain_text_maxcols) + "\n\n"
        for item in parser.anchorlist:
            counter += 1
            anchorlist += "[%d] %s\n" % (counter, item)

        text = textout.getvalue() + anchorlist
        del textout, formtext, parser, anchorlist
    else:
        if type(text) is not UnicodeType:
            raise TextMustBeUnicodeException

        text = text.encode(encoding)

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
    msg["Message-ID"] = email.Utils.make_msgid()
    if headers:
        for key, value in headers.items():
            msg[key] = value
    msg.preamble = "This is a multi-part message in MIME format."

    alternatives = MIMEMultipart("alternative")
    msg.attach(alternatives)
    alternatives.attach(MIMEText(text, "plain", _charset=encoding))
    alternatives.attach(MIMEText(html, "html", _charset=encoding))

    return msg
