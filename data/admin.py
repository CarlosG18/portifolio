from django.contrib import admin
from django.utils.html import format_html
from data.models import (
    Tech, Estatisticas, Sobre, DetailExperiencia, Experiencia, 
    RedesSociais, Contato, Habilidades, Projeto, ImagemProjeto, Certificacao
)

# Inline Admin Classes
class HabilidadesInline(admin.TabularInline):
    model = Habilidades
    extra = 1
    classes = ['collapse']

class ImagemProjetoInline(admin.TabularInline):
    model = ImagemProjeto
    extra = 1
    readonly_fields = ['preview_imagem']
    
    def preview_imagem(self, obj):
        if obj.imagem:
            return format_html('<img src="{}" width="100" height="60" style="object-fit: cover;" />', obj.imagem.url)
        return "-"
    preview_imagem.short_description = "Preview"

class DetailExperienciaInline(admin.TabularInline):
    model = Experiencia.detalhes_experiencia.through
    extra = 1
    classes = ['collapse']

class RedesSociaisInline(admin.TabularInline):
    model = Contato.redes.through
    extra = 1
    classes = ['collapse']

# Model Admin Classes
@admin.register(Tech)
class TechAdmin(admin.ModelAdmin):
    list_display = ['nome', 'versao', 'area', 'get_experiencias_count', 'get_projetos_count']
    list_display_links = ['nome']  # Define o link para edição
    list_filter = ['area',]
    search_fields = ['nome', 'descricao']
    list_editable = ['versao']  # Apenas versão é editável na lista
    list_per_page = 20
    
    def get_experiencias_count(self, obj):
        return obj.experiencias.count()
    get_experiencias_count.short_description = 'Exp. Count'
    
    def get_projetos_count(self, obj):
        return obj.projetos.count()
    get_projetos_count.short_description = 'Proj. Count'

@admin.register(Estatisticas)
class EstatisticasAdmin(admin.ModelAdmin):
    list_display = ['id', 'anos_experiencia', 'projetos_concluidos', 'tecnologias_dominadas', 'clientes_satisfeitos']
    list_display_links = ['id']  # Usa ID como link
    list_editable = ['anos_experiencia', 'projetos_concluidos', 'tecnologias_dominadas', 'clientes_satisfeitos']

@admin.register(Sobre)
class SobreAdmin(admin.ModelAdmin):
    list_display = ['nome', 'cargo', 'data_atualizacao', 'preview_foto']
    list_display_links = ['nome']  # Nome como link
    search_fields = ['nome', 'cargo', 'descritivo']
    readonly_fields = ['data_atualizacao', 'preview_foto']
    
    def preview_foto(self, obj):
        if obj.foto_perfil:
            return format_html('<img src="{}" width="80" height="80" style="object-fit: cover; border-radius: 50%;" />', obj.foto_perfil.url)
        return "Sem foto"
    preview_foto.short_description = "Foto"

@admin.register(DetailExperiencia)
class DetailExperienciaAdmin(admin.ModelAdmin):
    list_display = ['cargo', 'empresa', 'ano_entrada', 'ano_saida', 'atual', 'get_techs_count']
    list_display_links = ['cargo']  # Cargo como link
    list_filter = ['atual', 'ano_entrada', 'techs__area']
    search_fields = ['cargo', 'empresa', 'descricao']
    filter_horizontal = ['techs']
    date_hierarchy = 'ano_entrada'
    list_per_page = 15
    
    def get_techs_count(self, obj):
        return obj.techs.count()
    get_techs_count.short_description = 'Techs'

@admin.register(Experiencia)
class ExperienciaAdmin(admin.ModelAdmin):
    list_display = ['id', 'tipo', 'get_detalhes_count']
    list_display_links = ['id']  # ID como link
    list_filter = ['tipo']
    filter_horizontal = ['detalhes_experiencia']
    inlines = [DetailExperienciaInline]
    
    def get_detalhes_count(self, obj):
        return obj.detalhes_experiencia.count()
    get_detalhes_count.short_description = 'Detalhes'

@admin.register(RedesSociais)
class RedesSociaisAdmin(admin.ModelAdmin):
    list_display = ['nome', 'link', 'ativo', 'ordem', 'preview_icon']
    list_display_links = ['nome']  # Nome como link
    list_editable = ['ativo', 'ordem']  # Apenas ativo e ordem são editáveis
    list_filter = ['ativo']
    search_fields = ['nome']
    readonly_fields = ['preview_icon']
    
    def preview_icon(self, obj):
        if obj.icon:
            return format_html('<img src="{}" width="30" height="30" />', obj.icon.url)
        return "-"
    preview_icon.short_description = "Ícone"

@admin.register(Contato)
class ContatoAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'numero', 'get_redes_count']
    list_display_links = ['id']  # ID como link
    search_fields = ['email', 'numero']
    filter_horizontal = ['redes']
    inlines = [RedesSociaisInline]
    
    def get_redes_count(self, obj):
        return obj.redes.count()
    get_redes_count.short_description = 'Redes'

@admin.register(Habilidades)
class HabilidadesAdmin(admin.ModelAdmin):
    list_display = ['id', 'tech', 'progresso', 'nivel', 'anos_experiencia', 'ordem']
    list_display_links = ['id']  # ID como link
    list_editable = ['progresso', 'nivel', 'anos_experiencia', 'ordem']
    list_filter = ['nivel', 'tech__area']
    search_fields = ['tech__nome']
    list_per_page = 25
    ordering = ['ordem', '-progresso']

@admin.register(Projeto)
class ProjetoAdmin(admin.ModelAdmin):
    list_display = [
        'titulo', 'status', 'data_inicio', 'data_conclusao', 
        'destaque', 'get_tecnologias_count', 'preview_imagem'
    ]
    list_display_links = ['titulo']  # Título como link
    list_filter = ['status', 'destaque', 'data_inicio', 'tecnologias__area']
    search_fields = ['titulo', 'descricao', 'descricao_curta']
    filter_horizontal = ['tecnologias']
    readonly_fields = ['tempo_desenvolvimento', 'preview_imagem']
    date_hierarchy = 'data_inicio'
    list_editable = ['status', 'destaque']  # Apenas status e destaque são editáveis
    inlines = [ImagemProjetoInline]
    list_per_page = 15
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('titulo', 'descricao_curta', 'descricao', 'status', 'destaque')
        }),
        ('Datas', {
            'fields': ('data_inicio', 'data_conclusao', 'tempo_desenvolvimento'),
            'classes': ('collapse',)
        }),
        ('Mídia e Links', {
            'fields': ('imagem_destaque', 'preview_imagem', 'link_demo', 'link_repositorio'),
            'classes': ('collapse',)
        }),
        ('Tecnologias', {
            'fields': ('tecnologias', 'ordem')
        }),
    )
    
    def get_tecnologias_count(self, obj):
        return obj.tecnologias.count()
    get_tecnologias_count.short_description = 'Techs'
    
    def preview_imagem(self, obj):
        if obj.imagem_destaque:
            return format_html('<img src="{}" width="120" height="80" style="object-fit: cover;" />', obj.imagem_destaque.url)
        return "Sem imagem"
    preview_imagem.short_description = "Preview"

@admin.register(ImagemProjeto)
class ImagemProjetoAdmin(admin.ModelAdmin):
    list_display = ['id', 'projeto', 'descricao', 'ordem', 'preview_imagem']
    list_display_links = ['id']  # ID como link
    list_editable = ['ordem']  # Apenas ordem é editável
    list_filter = ['projeto']
    search_fields = ['projeto__titulo', 'descricao']
    readonly_fields = ['preview_imagem']
    
    def preview_imagem(self, obj):
        if obj.imagem:
            return format_html('<img src="{}" width="150" height="100" style="object-fit: cover;" />', obj.imagem.url)
        return "-"
    preview_imagem.short_description = "Preview"

@admin.register(Certificacao)
class CertificacaoAdmin(admin.ModelAdmin):
    list_display = [
        'titulo', 'instituicao', 'data_emissao', 'data_expiracao', 
        'expirado', 'get_tecnologias_count'
    ]
    list_display_links = ['titulo']  # Título como link
    list_filter = ['instituicao', 'data_emissao', 'data_expiracao']
    search_fields = ['titulo', 'instituicao', 'codigo_credencial']
    filter_horizontal = ['tecnologias']
    readonly_fields = ['expirado']
    date_hierarchy = 'data_emissao'
    list_per_page = 20
    
    def get_tecnologias_count(self, obj):
        return obj.tecnologias.count()
    get_tecnologias_count.short_description = 'Techs'
    
    def expirado(self, obj):
        return obj.expirado
    expirado.boolean = True

# Customizando o Admin Site
admin.site.site_header = "Administração do Portfólio"
admin.site.site_title = "Portfólio Admin"
admin.site.index_title = "Gerenciamento do Portfólio"

# Ordenação personalizada dos models no admin
def get_app_list(self, request):
    app_dict = self._build_app_dict(request)
    
    # Ordem desejada dos models para o app data
    model_ordering = {
        'Sobre': 1,
        'Experiência': 2,
        'Detalhe de Experiência': 3,
        'Projeto': 4,
        'Imagem do Projeto': 5,
        'Tecnologia': 6,
        'Habilidade': 7,
        'Certificação': 8,
        'Estatística': 9,
        'Contato': 10,
        'Rede Social': 11,
    }
    
    app_list = []
    
    for app_name, app in app_dict.items():
        if app_name == 'data':
            # Ordena os models do app data
            app['models'].sort(key=lambda x: model_ordering.get(x['name'], 999))
            app_list.append(app)
        else:
            app_list.append(app)
    
    return app_list

admin.AdminSite.get_app_list = get_app_list