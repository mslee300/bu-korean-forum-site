# from django.core.paginator import Paginator
# from django.db.models import Q
from django.shortcuts import render, get_object_or_404

# from pybo.models import Question

from django.contrib.auth.decorators import login_required


@login_required(login_url='common:login')
def index(request):
  return render(request, "pybo/search.html", {})
