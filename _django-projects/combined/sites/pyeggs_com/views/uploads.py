from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response

def handle_uploaded_file(f):
    destination = open('some/file/name.txt', 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()
    
def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            return HttpResponseRedirect('/upload-success/')
    else:
        form = UploadFileForm()
    return render_to_response('upload.html', {'form': form})