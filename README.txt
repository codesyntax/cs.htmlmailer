Introduction
============

This small library has a method to create a MIME Multipart email object
with HTML and Text content to be able to send it by e-mail.

This allows you to prepare an HTML content (with a templating language)
and forget about the text representation of the HTML; just import the
method and call it with the HTML content and the e-mail headers (to, cc,
subject, ...)

This is the signature of the method::

  def create_html_mail(subject, html, text=None, from_addr=None, to_addr=None,
                     cc_addrs=[], headers=None, encoding='UTF-8'):
