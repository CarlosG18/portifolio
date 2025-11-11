from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from enum import Enum

class AreaEnum(Enum):
    FRONTEND = "Frontend Development"
    BACKEND = "Backend Development"
    FULLSTACK = "Full Stack Development"
    MOBILE = "Mobile Development"
    DEVOPS = "DevOps & Infrastructure"
    DATA_SCIENCE = "Data Science"
    MACHINE_LEARNING = "Machine Learning & AI"
    CYBERSECURITY = "Cybersecurity"
    CLOUD_COMPUTING = "Cloud Computing"
    DATABASE = "Database Administration"
    GAME_DEVELOPMENT = "Game Development"
    EMBEDDED_SYSTEMS = "Embedded Systems"
    IOT = "Internet of Things"
    BLOCKCHAIN = "Blockchain & Web3"
    QA_TESTING = "Quality Assurance & Testing"
    UI_UX = "UI/UX Design"
    PRODUCT_MANAGEMENT = "Product Management"
    AGILE_DEVOPS = "Agile & DevOps"
    COMPUTER_VISION = "Computer Vision"
    NATURAL_LANGUAGE_PROCESSING = "Natural Language Processing"
    BIG_DATA = "Big Data"
    AR_VR = "Augmented & Virtual Reality"
    QUANTUM_COMPUTING = "Quantum Computing"
    ROBOTICS = "Robotics & Automation"
    NETWORKING = "Networking & Telecommunications"

    @classmethod
    def choices(cls):
        return [(tipo.name, tipo.value) for tipo in cls]

class TipoExperienciaEnum(Enum):
    PROFISSIONAL = "Profissional"
    ACADEMICA = "Acadêmica"
    PESSOAL = "Pessoal"

    @classmethod
    def choices(cls):
        return [(tipo.name, tipo.value) for tipo in cls]

class NivelProficienciaEnum(Enum):
    INICIANTE = "Iniciante"
    INTERMEDIARIO = "Intermediário"
    AVANCADO = "Avançado"
    ESPECIALISTA = "Especialista"

    @classmethod
    def choices(cls):
        return [(nivel.name, nivel.value) for nivel in cls]

class StatusProjetoEnum(Enum):
    PLANEJAMENTO = "Em planejamento"
    DESENVOLVIMENTO = "Em desenvolvimento"
    CONCLUIDO = "Concluído"
    PAUSADO = "Pausado"
    CANCELADO = "Cancelado"

    @classmethod
    def choices(cls):
        return [(status.name, status.value) for status in cls]

class Tech(models.Model):
    nome = models.CharField(max_length=200, blank=False, null=False)
    area = models.CharField(max_length=200, choices=AreaEnum.choices())
    versao = models.CharField(max_length=50, blank=True, null=True, help_text="Versão principal da tecnologia")
    descricao = models.TextField(blank=True, null=True, help_text="Breve descrição da tecnologia")
    
    class Meta:
        verbose_name = "Tecnologia"
        verbose_name_plural = "Tecnologias"
        ordering = ['nome']

    def __str__(self):
        if self.versao:
            return f"{self.nome} {self.versao}"
        return self.nome

class Estatisticas(models.Model):
    anos_experiencia = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])
    projetos_concluidos = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])
    tecnologias_dominadas = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])
    clientes_satisfeitos = models.PositiveIntegerField(default=0, blank=True, null=True)
    
    class Meta:
        verbose_name = "Estatística"
        verbose_name_plural = "Estatísticas"

class Sobre(models.Model):
    nome = models.CharField(max_length=200, blank=False, null=False)
    cargo = models.CharField(max_length=200, blank=False, null=False)
    descritivo = models.TextField(max_length=1000, blank=True, null=True)
    foto_perfil = models.ImageField(upload_to='sobre/', blank=True, null=True)
    curriculo = models.FileField(upload_to='curriculos/', blank=True, null=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Sobre"
        verbose_name_plural = "Sobre"

    def __str__(self):
        return f"{self.nome} - {self.cargo}"

class DetailExperiencia(models.Model):
    ano_entrada = models.DateField()
    ano_saida = models.DateField(blank=True, null=True, help_text="Deixe em branco se for a experiência atual")
    cargo = models.CharField(max_length=200)
    empresa = models.CharField(max_length=200)
    descricao = models.TextField(blank=True, null=True, help_text="Descrição das responsabilidades e conquistas")
    techs = models.ManyToManyField(Tech, related_name='experiencias')
    atual = models.BooleanField(default=False, help_text="Marcar se é a experiência atual")
    
    class Meta:
        verbose_name = "Detalhe de Experiência"
        verbose_name_plural = "Detalhes de Experiência"
        ordering = ['-ano_entrada']

    def __str__(self):
        status = "Atual" if self.atual else f"{self.ano_saida.year}"
        return f"{self.cargo} at {self.empresa} ({self.ano_entrada.year} - {status})"

class Experiencia(models.Model):
    tipo = models.CharField(max_length=200, choices=TipoExperienciaEnum.choices())
    detalhes_experiencia = models.ManyToManyField(DetailExperiencia, related_name='experiencias')
    
    class Meta:
        verbose_name = "Experiência"
        verbose_name_plural = "Experiências"

    def __str__(self):
        return f"{self.get_tipo_display()}"

class RedesSociais(models.Model):
    nome = models.CharField(max_length=200)
    user = models.CharField(max_length=200, blank=True, null=True)
    link = models.URLField()
    icon = models.ImageField(upload_to='redes/', blank=True, null=True)
    ativo = models.BooleanField(default=True)
    ordem = models.PositiveIntegerField(default=0, help_text="Ordem de exibição")
    
    class Meta:
        verbose_name = "Rede Social"
        verbose_name_plural = "Redes Sociais"
        ordering = ['ordem', 'nome']

    def __str__(self):
        return self.nome

class Contato(models.Model):
    email = models.EmailField()
    numero = models.CharField(max_length=20, blank=True, null=True)
    endereco = models.TextField(blank=True, null=True)
    redes = models.ManyToManyField(RedesSociais, related_name='contatos', blank=True)
    
    class Meta:
        verbose_name = "Contato"
        verbose_name_plural = "Contatos"

class Habilidades(models.Model):
    tech = models.ForeignKey(Tech, on_delete=models.CASCADE, related_name='habilidades')
    progresso = models.PositiveIntegerField(
        default=0, 
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Progresso de 0 a 100%"
    )
    nivel = models.CharField(
        max_length=50, 
        choices=NivelProficienciaEnum.choices(),
        blank=True, 
        null=True
    )
    anos_experiencia = models.DecimalField(
        max_digits=3, 
        decimal_places=1, 
        default=0,
        help_text="Anos de experiência com esta tecnologia"
    )
    ordem = models.PositiveIntegerField(default=0, help_text="Ordem de exibição")
    
    class Meta:
        verbose_name = "Habilidade"
        verbose_name_plural = "Habilidades"
        ordering = ['ordem', '-progresso']

    def __str__(self):
        return f"{self.tech.nome} - {self.progresso}%"

class Projeto(models.Model):
    titulo = models.CharField(max_length=200)
    descricao = models.TextField(help_text="Descrição detalhada do projeto")
    descricao_curta = models.CharField(max_length=300, blank=True, null=True, help_text="Descrição breve para cards")
    imagem_destaque = models.ImageField(upload_to='projetos/', blank=True, null=True)
    tecnologias = models.ManyToManyField(Tech, related_name='projetos')
    status = models.CharField(
        max_length=50, 
        choices=StatusProjetoEnum.choices(), 
        default=StatusProjetoEnum.CONCLUIDO.value
    )
    data_inicio = models.DateField()
    data_conclusao = models.DateField(blank=True, null=True)
    link_demo = models.URLField(blank=True, null=True, help_text="Link para demonstração ao vivo")
    link_repositorio = models.URLField(blank=True, null=True, help_text="Link para repositório de código")
    destaque = models.BooleanField(default=False, help_text="Marcar como projeto em destaque")
    ordem = models.PositiveIntegerField(default=0, help_text="Ordem de exibição")
    
    class Meta:
        verbose_name = "Projeto"
        verbose_name_plural = "Projetos"
        ordering = ['ordem', '-data_inicio']

    def __str__(self):
        return self.titulo

    @property
    def tempo_desenvolvimento(self):
        if self.data_conclusao:
            delta = self.data_conclusao - self.data_inicio
            return f"{delta.days // 30} meses"
        return "Em andamento"

class ImagemProjeto(models.Model):
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE, related_name='imagens')
    imagem = models.ImageField(upload_to='projetos/imagens/')
    descricao = models.CharField(max_length=200, blank=True, null=True)
    ordem = models.PositiveIntegerField(default=0)
    
    class Meta:
        verbose_name = "Imagem do Projeto"
        verbose_name_plural = "Imagens do Projeto"
        ordering = ['ordem']

class Certificacao(models.Model):
    titulo = models.CharField(max_length=200)
    instituicao = models.CharField(max_length=200)
    data_emissao = models.DateField()
    data_expiracao = models.DateField(blank=True, null=True)
    link_certificado = models.URLField(blank=True, null=True)
    codigo_credencial = models.CharField(max_length=100, blank=True, null=True)
    tecnologias = models.ManyToManyField(Tech, related_name='certificacoes', blank=True)
    
    class Meta:
        verbose_name = "Certificação"
        verbose_name_plural = "Certificações"
        ordering = ['-data_emissao']

    def __str__(self):
        return f"{self.titulo} - {self.instituicao}"

    @property
    def expirado(self):
        if self.data_expiracao:
            from datetime import date
            return self.data_expiracao < date.today()
        return False