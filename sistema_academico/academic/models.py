from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from accounts.models import CustomUser

class Materia(models.Model):
    nombre      = models.CharField(max_length=100)
    codigo      = models.CharField(max_length=20, unique=True)
    descripcion = models.TextField(blank=True)
    docente     = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, null=True,
        limit_choices_to={'rol': 'docente'}, related_name='materias'
    )
    creditos    = models.PositiveSmallIntegerField(default=3)
    activa      = models.BooleanField(default=True)

    def __str__(self): return f"{self.codigo} - {self.nombre}"

class Curso(models.Model):
    nombre   = models.CharField(max_length=100)
    año      = models.PositiveIntegerField()
    periodo  = models.CharField(max_length=20)  # Ej: "2024-1"
    materias = models.ManyToManyField(Materia, blank=True)
    estudiantes = models.ManyToManyField(
        CustomUser, blank=True, limit_choices_to={'rol': 'estudiante'},
        related_name='cursos'
    )

    def __str__(self): return f"{self.nombre} ({self.periodo})"

class Nota(models.Model):
    estudiante = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE,
        limit_choices_to={'rol': 'estudiante'}, related_name='notas'
    )
    materia  = models.ForeignKey(Materia, on_delete=models.CASCADE, related_name='notas')
    curso    = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='notas')
    valor    = models.DecimalField(
        max_digits=4, decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    tipo     = models.CharField(max_length=30,
                choices=[('parcial','Parcial'),('final','Final'),('taller','Taller')])
    fecha    = models.DateField(auto_now_add=True)
    observacion = models.TextField(blank=True)

    class Meta:
        ordering = ['-fecha']

    def __str__(self):
        return f"{self.estudiante} - {self.materia}: {self.valor}"

class Asistencia(models.Model):
    estudiante = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='asistencias'
    )
    materia  = models.ForeignKey(Materia, on_delete=models.CASCADE)
    curso    = models.ForeignKey(Curso, on_delete=models.CASCADE)
    fecha    = models.DateField()
    presente = models.BooleanField(default=True)

    class Meta:
        unique_together = ['estudiante', 'materia', 'fecha']