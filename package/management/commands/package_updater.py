# python -m smtpd -n -c DebuggingServer localhost:1025

from socket import error as socket_error
from time import sleep, gmtime, strftime
from xml.parsers.expat import ExpatError
from xmlrpclib import ProtocolError

from django.conf import settings
from django.core.management.base import NoArgsCommand
from django.core.mail import send_mail

from package.models import Package


class Command(NoArgsCommand):

    help = "Updates all the packages in the system. Commands belongs to django-packages.package"

    def handle(self, *args, **options):

        text = "Commencing package updating now at %s " % strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())

        for index, package in enumerate(Package.objects.all()):
            print index
            if index > 3:
                break
            try:
                try:
                    package.fetch_metadata()
                    package.fetch_commits()
                except socket_error, e:
                    text += "\nFor '%s', threw a socket.error: %s" % (package.title, e)
                    #print >> stdout, "For '%s', threw a socket.error: %s" % (package.title, e)
                    continue
            except RuntimeError, e:
                #message = "For '%s', too many requests issued to repo threw a RuntimeError: %s" % (package.title, e)
                text += "\nFor '%s', too many requests issued to repo threw a RuntimeError: %s" % (package.title, e)
                continue
            except UnicodeDecodeError, e:
                #message = "For '%s', UnicodeDecodeError: %s" % (package.title, e)
                #print >> stdout, message
                text += "\nFor '%s', UnicodeDecodeError: %s" % (package.title, e)
                continue
            except ProtocolError, e:
                #message = "For '%s', xmlrpc.ProtocolError: %s" % (package.title, e)
                #print >> stdout, message
                text += "\nFor '%s', xmlrpc.ProtocolError: %s" % (package.title, e)
                continue
            except ExpatError, e:
                #message = "For '%s', ExpatError: %s" % (package.title, e)
                #print >> stdout, message
                text += "\nFor '%s', ExpatError: %s" % (package.title, e)
                continue

            if not hasattr(settings, "GITHUB_ACCOUNT"):
                sleep(5)
            #print >> stdout, "%s. Successfully updated package '%s'" % (index + 1, package.title)
            text += "\n%s. Successfully updated package '%s'" % (index + 1, package.title)

        #print >> stdout, "-" * 40
        text += "\n"
        text += "-" * 40
        #print >> stdout, "Finished at %s" % strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
        text += "\nFinished at %s" % strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())

        print text

