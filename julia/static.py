import mimetypes
import posixpath
from pathlib import Path

from django.http import (
    FileResponse, Http404, HttpResponseNotModified,
)
from django.utils._os import safe_join
from django.utils.http import http_date
from django.views import static
from django.utils import timezone
from django.core.exceptions import PermissionDenied

from contest.models import Task
from auth.models import User

def secure_serve(request, path, document_root=None, show_indexes=False):
    print(request.user, 123)

    path = posixpath.normpath(path).lstrip('/')
    fullpath = Path(safe_join(document_root, path))
    print(path)
    if fullpath.is_dir():
        if show_indexes:
            return static.directory_index(path, fullpath)
        raise Http404("Directory indexes are not allowed here.")
    if not fullpath.exists():
        raise Http404(('“%(path)s” does not exist') % {'path': fullpath})

    if request.user.is_anonymous:
        raise PermissionDenied('Wait until the end of the contest to see other contestants decisions')

    task_id, username, *_ = path.split('_')
    contest = Task.objects.get(id=int(task_id)).contest
    is_owner = request.user is User.objects.get(username=username)
    if (timezone.now() < contest.start_time + contest.duration) and not is_owner:
        raise PermissionDenied('Wait until the end of the contest to see other contestants decisions')

    statobj = fullpath.stat()
    if not static.was_modified_since(request.META.get('HTTP_IF_MODIFIED_SINCE'),
                              statobj.st_mtime, statobj.st_size):
        return HttpResponseNotModified()
    content_type, encoding = mimetypes.guess_type(str(fullpath))
    content_type = content_type or 'application/octet-stream'
    response = FileResponse(fullpath.open('rb'), content_type=content_type)
    response["Last-Modified"] = http_date(statobj.st_mtime)
    if encoding:
        response["Content-Encoding"] = encoding
    return response