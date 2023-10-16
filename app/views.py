from django.shortcuts import render, get_object_or_404, HttpResponse
from django.urls import reverse_lazy
from django.utils import timezone
from . import utils, models
from django.contrib.auth.decorators import login_required
from django.http import FileResponse


def index(request):
    object_list = models.PrivateFile.objects.all()
    return render(request, 'index.html', {'object_list': object_list})


@login_required(login_url='/admin/login/')
def create_token_url(request):
    if request.method == 'POST':
        pk = request.POST.get('id')
        private_file = get_object_or_404(models.PrivateFile, pk=pk)
        file_token = models.PrivateFileToken.objects.create(file=private_file)
        file_url = reverse_lazy('serve_file', kwargs={'token': file_token.token})
        domain = utils.get_current_domain(request)
        url = domain + file_url
        return HttpResponse(f"""<a download="{private_file.file.name}" href="{url}"> {url} </a>""")
    return HttpResponse('Method not allowed')


def serve_file(request, token):
    private_file = get_object_or_404(
        models.PrivateFileToken, token=token, expire_at__gte=timezone.now()
    ).file
    return FileResponse(open(private_file.file.path, 'rb'))


def file_not_access_url(request, str):
    return HttpResponse('File not access')
