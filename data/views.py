from django.shortcuts import render
from .models import Sobre, Estatisticas, Contato

# Create your views here.
def index(request):
    sobre = Sobre.objects.all().first()
    estatisticas = Estatisticas.objects.all().first()
    contato = Contato.objects.all().first()
    
    context = {
        'sobre': sobre,
        'estatisticas': estatisticas,
        'contato': contato,
    }

    return render(request, 'index.html', context)