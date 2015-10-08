import os
import logging
import httplib2
import json

from apiclient.discovery import build

from apiclient import errors
from apiclient import http

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from ds.models import CredentialsModel, FlowModel
from docsql import settings
from oauth2client import xsrfutil
from oauth2client.client import flow_from_clientsecrets
from oauth2client.django_orm import Storage




# CLIENT_SECRETS, name of a file containing the OAuth 2.0 information for this
# application, including client_id and client_secret, which are found
# on the API Access tab on the Google APIs
# Console <http://code.google.com/apis/console>
CLIENT_SECRETS = os.path.join(os.path.dirname(__file__), 'cred.json')




print "always"

FLOW = flow_from_clientsecrets(
    CLIENT_SECRETS,
    scope=['https://www.googleapis.com/auth/drive'],
    redirect_uri='http://localhost:8000/oauth2callback')

@login_required
def index(request):
  storage = Storage(CredentialsModel, 'id', request.user, 'credential')
  credential = storage.get()


#  return render_to_response("accounts/welcome.html", {'activitylist': ['ddss','asdasd','3ed23d32d']})





  if credential is None or credential.invalid == True:
    FLOW.params['state'] = xsrfutil.generate_token(settings.SECRET_KEY,
                                                   request.user)
    authorize_url = FLOW.step1_get_authorize_url()
    return HttpResponseRedirect(authorize_url)
  else:
    http = httplib2.Http()

    http = credential.authorize(http)
    service = build("drive", "v2", http=http)
    files = service.files().list().execute()
    #print json.dumps(files)



    #simport pdb; pdb.set_trace()

    return render_to_response('accounts/welcome.html', {
                'activitylist': files,
                })

@login_required
def auth_return(request):
    print "xxxxxxxxxxxxPSTATE " , request.REQUEST['state']
    print "xxxxxxxxxxxxU ", request.user
    print "xxxxxxxxxxxxS ", settings.SECRET_KEY
    print "xxxxxxxxxxxxV ", xsrfutil.validate_token(
            settings.SECRET_KEY, request.REQUEST['state'], request.user)
    print "xxxxxxxxxxxxG ", xsrfutil.generate_token(settings.SECRET_KEY,
                                                   request.user)


    if not xsrfutil.validate_token(
            settings.SECRET_KEY, str(request.REQUEST['state']), request.user):
        return HttpResponseBadRequest()


    credential = FLOW.step2_exchange(request.REQUEST)
    storage = Storage(CredentialsModel, 'id', request.user, 'credential')

    storage.put(credential)
    return HttpResponseRedirect("/")

def table2sql(request,id=0):
    bucket_name = '';
    if id:

        storage = Storage(CredentialsModel, 'id', request.user, 'credential')
        credential = storage.get()
        http1 = httplib2.Http()

        http2 = credential.authorize(http1)
        service = build("drive", "v2", http=http2)
#        files = service.files().list().execute()
#        request = service.files().get_media(fileId=id)
#        local_fd  = open('workfile', 'w');
#        media_request = http.MediaIoBaseDownload(local_fd, request)
#        close f;


        # Retry transport and file IO errors.
        RETRYABLE_ERRORS = (httplib2.HttpLib2Error, IOError)

        # Number of times to retry failed downloads.
        NUM_RETRIES = 5

        # Number of bytes to send/receive in each request.
        CHUNKSIZE = 2 * 1024 * 1024

        # Mimetype to use if one can't be guessed from the file extension.
        DEFAULT_MIMETYPE = 'application/octet-stream'

        print 'Building download request...'
        filename = 'xxx'
        f = file(filename, 'w')
        request = service.files().get_media(fileId=id)
        media = http.MediaIoBaseDownload(f, request, chunksize=CHUNKSIZE)

        print 'Downloading bucket: %s object: %s to file: %s' % (bucket_name,
                                                           id,
                                                           filename)

        progressless_iters = 0
        done = False
        while not done:
            error = None
            try:
              progress, done = media.next_chunk()
              if progress:
                print_with_carriage_return(
                    'Download %d%%.' % int(progress.progress() * 100))
            except HttpError, err:
              error = err
              if err.resp.status < 500:
                raise
            except RETRYABLE_ERRORS, err:
              error = err

            if error:
              progressless_iters += 1
              handle_progressless_iter(error, progressless_iters)
            else:
              progressless_iters = 0

        print '\nDownload complete!'


        return render_to_response('table2sql.html', {
                'fileid': id,
        })
    else:
        return HttpResponse('<h1>Page was found</h1>',id)