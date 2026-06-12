"""
SIGCU Bolivia — Script de carga de datos reales UATF
=====================================================
Fuente: Documentos oficiales DSA-UATF 2026
Ejecutar desde la raíz del proyecto:

    python manage.py shell < cargar_datos_uatf.py

O con runscript si tienes django-extensions:

    python manage.py runscript cargar_datos_uatf

El script es IDEMPOTENTE: si ya existen los registros los actualiza,
no los duplica. Puedes ejecutarlo varias veces sin problema.
"""

import os
import django
import sys

# ── Configuración de Django ──────────────────────────────────────────────────
# Solo necesaria si ejecutas el script directamente (python cargar_datos_uatf.py)
# Si lo ejecutas con manage.py shell < ... puedes omitir estas líneas.
if 'DJANGO_SETTINGS_MODULE' not in os.environ:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    django.setup()

from universidades.models import Universidad, Facultad, Sede
from carreras.models import Carrera, PlanEstudio
from programas.models import Programa
from seguimiento.models import TipoFase, ProcesoCurricular, FaseProceso

print("=" * 60)
print("SIGCU Bolivia — Carga de datos reales UATF")
print("=" * 60)


# ════════════════════════════════════════════════════════════
# PASO 1 — UNIVERSIDAD
# ════════════════════════════════════════════════════════════
print("\n[1/6] Creando Universidad UATF...")

uatf, created = Universidad.objects.update_or_create(
    sigla='UATF',
    defaults={
        'nombre':       'Universidad Autónoma Tomás Frías',
        'departamento': 'Potosí',
        'rector':       '',
        'telefono':     '(+591-2) 6227300',
        'website':      'https://www.uatf.edu.bo',
        'activa':       True,
    }
)
print(f"  {'✅ Creada' if created else '🔄 Actualizada'}: {uatf}")


# ════════════════════════════════════════════════════════════
# PASO 2 — FACULTADES
# ════════════════════════════════════════════════════════════
print("\n[2/6] Creando Facultades...")

FACULTADES = [
    # (nombre_corto_para_lookup, nombre_completo, sigla, telefono)
    ('ARTES',        'Facultad de Artes',                                          'FART',  '62-27310'),
    ('AGRICOLAS',    'Facultad de Ciencias Agrícolas y Pecuarias',                 'FCAP',  '6247414'),
    ('SALUD',        'Facultad de Ciencias de la Salud',                           'FCS',   '62-27585'),
    ('ECONOMICAS',   'Facultad de Ciencias Económicas, Financieras y Administrativas', 'FCEFA', '6227315'),
    ('PURAS',        'Facultad de Ciencias Puras',                                 'FCP',   '6227305'),
    ('SOCIALES',     'Facultad de Ciencias Sociales y Humanísticas',               'FCSH',  '6227302'),
    ('DERECHO',      'Facultad de Derecho',                                        'FD',    '6227309'),
    ('GEOLOGICA',    'Facultad de Ingeniería Geológica',                            'FIG',   '6247445'),
    ('MINERA',       'Facultad de Ingeniería Minera',                              'FIM',   '6227320'),
    ('TECNOLOGICA',  'Facultad de Ingeniería Tecnológica',                         'FIT',   '62-27331'),
    ('INGENIERIA',   'Facultad de Ingeniería',                                     'FI',    '6227314'),
    ('MEDICINA',     'Facultad de Medicina',                                       'FM',    '6225706'),
    ('DSA',          'Dirección de Servicios Académicos',                          'DSA',   ''),
]

fac_map = {}  # clave corta → objeto Facultad
for clave, nombre, sigla, tel in FACULTADES:
    obj, created = Facultad.objects.update_or_create(
        universidad=uatf,
        sigla=sigla,
        defaults={
            'nombre':   nombre,
            'telefono': tel,
        }
    )
    fac_map[clave] = obj
    print(f"  {'✅' if created else '🔄'} {sigla} — {nombre}")


# ════════════════════════════════════════════════════════════
# PASO 3 — SEDES
# ════════════════════════════════════════════════════════════
print("\n[3/6] Creando Sedes...")

# Estructura: (facultad_clave, nombre_sede, tipo, ciudad, departamento,
#              direccion, telefono, latitud, longitud)
SEDES_DATA = [
    # Artes
    ('ARTES',     'Facultad de Artes — Potosí',                   'CENTRAL',   'Potosí',      'Potosí',   'Calle Bolívar s/n (entre calles Sucre y Junín)',         '62-27310',  -19.5836, -65.7536),
    # Agrícolas
    ('AGRICOLAS', 'Facultad de Cs. Agrícolas y Pecuarias — Potosí','CENTRAL',  'Potosí',      'Potosí',   'Ciudadela Universitaria, Bloque 1, Primer Piso',         '6247414',   -19.5601, -65.7440),
    ('AGRICOLAS', 'Facultad de Cs. Agrícolas y Pecuarias — Tupiza','EXTENSION','Tupiza',      'Potosí',   'Av. La Paz s/n, Tupiza',                                 '02-694-3164',-21.4387, -65.7184),
    ('AGRICOLAS', 'Facultad de Cs. Agrícolas y Pecuarias — Villazón','EXTENSION','Villazón',  'Potosí',   'Av. Bolívar esq. calle Capitán Sarapura, Villazón',      '597-4825',  -22.0868, -65.5966),
    # Salud
    ('SALUD',     'Facultad de Cs. de la Salud — Potosí',         'CENTRAL',   'Potosí',      'Potosí',   'Calle Nogales N° 449',                                   '62-27585',  -19.5836, -65.7536),
    ('SALUD',     'Facultad de Cs. de la Salud — Villazón',       'EXTENSION', 'Villazón',    'Potosí',   'Av. Boliviar entre Capitan Sarapura',                    '597-4825',  -22.0868, -65.5966),
    ('SALUD',     'Facultad de Cs. de la Salud — Llica',          'EXTENSION', 'Llica',       'Potosí',   'Calle Daniel Campos y Avaroa',                           '75792157',  -19.8514, -68.2460),
    # Económicas
    ('ECONOMICAS','Facultad de Cs. Económicas — Potosí',          'CENTRAL',   'Potosí',      'Potosí',   'Av. del Maestro (Ed. Central, 3er y 4to piso)',          '6227315',   -19.5836, -65.7536),
    ('ECONOMICAS','Facultad de Cs. Económicas — Tupiza',          'EXTENSION', 'Tupiza',      'Potosí',   'Av. Gualberto Villarroel entre calle Bolívar y 4 de Junio','2-694-3233',-21.4387, -65.7184),
    ('ECONOMICAS','Facultad de Cs. Económicas — Villazón',        'EXTENSION', 'Villazón',    'Potosí',   'Av. Boliviar entre Capitan Sarapura',                    '72445000',  -22.0868, -65.5966),
    ('ECONOMICAS','Facultad de Cs. Económicas — Uncía',           'EXTENSION', 'Uncía',       'Potosí',   'Calle Campos s/n',                                       '72425186',  -18.4667, -66.6167),
    ('ECONOMICAS','Facultad de Cs. Económicas — Uyuni',           'EXTENSION', 'Uyuni',       'Potosí',   'Calle Quijarro s/n Esq. Calle Sucre',                    '6932183',   -20.4627, -66.8251),
    ('ECONOMICAS','Facultad de Cs. Económicas — Río Grande',      'EXTENSION', 'Río Grande',  'Potosí',   'Río Grande, Potosí',                                     '',          -20.0000, -67.0000),
    # Puras
    ('PURAS',     'Facultad de Ciencias Puras — Potosí',          'CENTRAL',   'Potosí',      'Potosí',   'Av. del Maestro s/n (Ed. Central) / 2do. Bloque',        '6227305',   -19.5836, -65.7536),
    ('PURAS',     'Facultad de Ciencias Puras — Uyuni',           'EXTENSION', 'Uyuni',       'Potosí',   'Av. Bolivar entre Calle Tomas Frias y Bustillo',         '68770777',  -20.4627, -66.8251),
    # Sociales
    ('SOCIALES',  'Facultad de Cs. Sociales y Humanísticas — Potosí','CENTRAL','Potosí',      'Potosí',   'Av. Wenceslao Alba Esq. Antofagasta 3er piso',           '6227302',   -19.5601, -65.7440),
    ('SOCIALES',  'Facultad de Cs. Sociales y Humanísticas — Uncía','EXTENSION','Uncía',      'Potosí',   'Calle Campos s/n',                                       '71854302',  -18.4667, -66.6167),
    ('SOCIALES',  'Facultad de Cs. Sociales y Humanísticas — Uyuni','EXTENSION','Uyuni',      'Potosí',   'Calle Bolívar s/n entre Tomás Frías y Bustillos, Uyuni', '6933616',   -20.4627, -66.8251),
    # Derecho
    ('DERECHO',   'Facultad de Derecho — Potosí',                 'CENTRAL',   'Potosí',      'Potosí',   'Av. del Maestro s/n, Edif. Central 2do piso',            '6227309',   -19.5836, -65.7536),
    ('DERECHO',   'Facultad de Derecho — Tupiza',                 'EXTENSION', 'Tupiza',      'Potosí',   'Calle Bolívar esq. Plazuela Villarroel, Tupiza',         '65479786',  -21.4387, -65.7184),
    ('DERECHO',   'Facultad de Derecho — Uncía',                  'EXTENSION', 'Uncía',       'Potosí',   'Calle Campos s/n',                                       '71854302',  -18.4667, -66.6167),
    # Geológica
    ('GEOLOGICA', 'Facultad de Ing. Geológica — Potosí',          'CENTRAL',   'Potosí',      'Potosí',   'Ciudadela Universitaria, Bloque Aulas 5',                '6247445',   -19.5601, -65.7440),
    # Minera
    ('MINERA',    'Facultad de Ingeniería Minera — Potosí',        'CENTRAL',  'Potosí',      'Potosí',   'Av. Villazón esq. Av. Arce',                             '6227320',   -19.5836, -65.7536),
    # Tecnológica
    ('TECNOLOGICA','Facultad de Ing. Tecnológica — Potosí',       'CENTRAL',   'Potosí',      'Potosí',   'Calle Millares Nro. 81',                                 '62-27331',  -19.5836, -65.7536),
    ('TECNOLOGICA','Facultad de Ing. Tecnológica — San Cristóbal', 'EXTENSION','San Cristóbal','Potosí',  'Calle Litoral entre Oruro y Copacabana',                 '68145471',  -21.0333, -67.1167),
    # Ingeniería
    ('INGENIERIA','Facultad de Ingeniería — Potosí',              'CENTRAL',   'Potosí',      'Potosí',   'Av. Sevilla s/n',                                        '6227314',   -19.5836, -65.7536),
    # Medicina
    ('MEDICINA',  'Facultad de Medicina — Potosí',                'CENTRAL',   'Potosí',      'Potosí',   'Calle Hoyos Nro. 36',                                    '6225706',   -19.5836, -65.7536),
    # DSA
    ('DSA',       'Dirección de Servicios Académicos — Potosí',   'CENTRAL',   'Potosí',      'Potosí',   'Ciudadela Universitaria, Edificio Central',              '',          -19.5836, -65.7536),
    ('DSA',       'Dirección de Servicios Académicos — Tupiza',   'EXTENSION', 'Tupiza',      'Potosí',   'Av. La Paz s/n, Tupiza',                                 '',          -21.4387, -65.7184),
    ('DSA',       'Dirección de Servicios Académicos — Uncía',    'EXTENSION', 'Uncía',       'Potosí',   'Calle Campos s/n',                                       '',          -18.4667, -66.6167),
]

sede_map = {}  # (fac_clave, ciudad) → objeto Sede
for fac_clave, nombre, tipo, ciudad, depto, direccion, telefono, lat, lon in SEDES_DATA:
    obj, created = Sede.objects.update_or_create(
        facultad=fac_map[fac_clave],
        ciudad=ciudad,
        nombre=nombre,
        defaults={
            'tipo':        tipo,
            'departamento': depto,
            'direccion':   direccion,
            'telefono':    telefono,
            'latitud':     lat,
            'longitud':    lon,
            'activa':      True,
        }
    )
    sede_map[(fac_clave, ciudad)] = obj
    print(f"  {'✅' if created else '🔄'} {nombre}")


def get_sede(fac_clave, ciudad='Potosí'):
    """Helper: devuelve la sede más cercana o la central si no existe."""
    key = (fac_clave, ciudad)
    if key in sede_map:
        return sede_map[key]
    # fallback a sede central de la facultad
    central = (fac_clave, 'Potosí')
    if central in sede_map:
        return sede_map[central]
    # último recurso: primera sede de esa facultad
    return Sede.objects.filter(facultad=fac_map[fac_clave]).first()


# ════════════════════════════════════════════════════════════
# PASO 4 — CARRERAS OFICIALES
# ════════════════════════════════════════════════════════════
print("\n[4/6] Creando Carreras oficiales...")

# Mapeo de grado: código del excel → choices del modelo
GRADO_MAP = {
    'LIC': 'LIC', 'TUS': 'TUS', 'TUM': 'TEC', 'TEC': 'TEC',
}
ENFOQUE_MAP = {
    'COMPETENCIAS': 'COMPETENCIAS',
    'OBJETIVOS':    'OBJETIVOS',
    'OTRO':         'OTRO',
    '':             '',
}

# (fac_clave, ciudad, nombre, grado, area, diploma, titulo,
#  enfoque, en_funcionamiento, numero_sub, anio_plan, resolucion)
CARRERAS_DATA = [
    # ── ARTES ────────────────────────────────────────────────────────────────
    ('ARTES','Potosí','Artes Plásticas','LIC',5,'Licenciado en Artes Plásticas','Licenciado en Artes Plásticas','COMPETENCIAS',True,537,'1999 2003 2010 2018','IXC.UABJB R:X C. UAP R:II-XI UAJMS R:I-XIIIUAJMS'),
    ('ARTES','Potosí','Artes Plásticas','TUS',5,'Técnico Universitario Superior en Artes Plásticas','Técnico Universitario Superior en Artes Plásticas','COMPETENCIAS',True,538,'1999 2003','IXC.UABJB R:X C. UAP'),
    ('ARTES','Potosí','Artes Musicales','LIC',5,'Licenciado en Artes Musicales','Licenciado en Artes Musicales','COMPETENCIAS',True,539,'1999 2003 2023','IXC.UABJB R:X C. UAP R:II-XIII UAGRM'),
    ('ARTES','Potosí','Artes Musicales','TUS',5,'Técnico Universitario Superior en Artes Musicales','Técnico Universitario Superior en Artes Musicales','COMPETENCIAS',True,540,'2003','X C. UAP'),
    ('ARTES','Potosí','Arquitectura','LIC',5,'Licenciado en Arquitectura','Arquitecto','COMPETENCIAS',True,541,'2015','II-XII UTO'),
    # ── CIENCIAS AGRÍCOLAS Y PECUARIAS ───────────────────────────────────────
    ('AGRICOLAS','Tupiza','Medicina Veterinaria y Zootecnia','LIC',3,'Licenciado en Medicina Veterinaria y Zootecnia','Médico Veterinario Zootecnista','COMPETENCIAS',True,543,'1999 2003 2025','IXC.UABJB R:X C. UAP R:IV-XIIIUAJMS'),
    ('AGRICOLAS','Potosí','Ingeniería en Desarrollo Territorial','LIC',2,'Licenciado en Ingeniería en Desarrollo Territorial','Ingeniero en Desarrollo Territorial','COMPETENCIAS',True,545,'2025','R:IV-XIIIUAJMS'),
    ('AGRICOLAS','Villazón','Ingeniería en Agropecuaria','LIC',3,'Licenciado en Ingeniería Agropecuaria','Ingeniero Agropecuario','COMPETENCIAS',True,546,'2012','IV-XI UABJB'),
    ('AGRICOLAS','Villazón','Ingeniería en Agropecuaria','TUS',3,'Técnico Universitario Superior en Ingeniería Agronómica','Técnico Universitario Superior en Agropecuaria','COMPETENCIAS',True,547,'2012','IV-XI UABJB'),
    ('AGRICOLAS','Potosí','Ingeniería Agronómica','LIC',3,'Licenciado en Ingeniería Agronómica','Ingeniero Agrónomo','COMPETENCIAS',True,548,'1999 2003 2018','IXC.UABJB R:X C. UAP R:I-XIIIUAJMS'),
    ('AGRICOLAS','Potosí','Ingeniería Agroindustrial','LIC',3,'Licenciado en Ingeniería Agroindustrial','Ingeniero Agroindustrial','COMPETENCIAS',True,550,'2010 2023','II-XI UAJMS R:II-XIIIUAGRM'),
    # ── CIENCIAS DE LA SALUD ─────────────────────────────────────────────────
    ('SALUD','Potosí','Enfermería','LIC',4,'Licenciado en Enfermería','Licenciado en Enfermería','COMPETENCIAS',True,552,'1999 2003 2018','IXC.UABJB R:X C. UAP R:I-XIIIUAJMS'),
    ('SALUD','Villazón','Enfermería','LIC',4,'Licenciado en Enfermería','Licenciado en Enfermería','COMPETENCIAS',True,553,'2010 2018','II-XI UAJMS R:I-XIIIUAJMS'),
    # ── CIENCIAS ECONÓMICAS, FINANCIERAS Y ADMINISTRATIVAS ───────────────────
    ('ECONOMICAS','Potosí','Ingeniería Comercial','LIC',6,'Licenciado en Ingeniería Comercial','Ingeniero Comercial','COMPETENCIAS',True,556,'2018','I-XIII UAJMS'),
    ('ECONOMICAS','Potosí','Economía','LIC',6,'Licenciado en Economía','Economista','COMPETENCIAS',True,558,'1999 2003','IXC.UABJB R:X C. UAP'),
    ('ECONOMICAS','Uncía','Economía','LIC',6,'Licenciado en Economía','Economista','COMPETENCIAS',True,559,'2003','X C. UAP'),
    ('ECONOMICAS','Uyuni','Economía','LIC',6,'Licenciado en Economía','Economista','COMPETENCIAS',True,560,'2003','X C. UAP'),
    ('ECONOMICAS','Potosí','Auditoría - Contaduría Pública','LIC',6,'Licenciado en Auditoría Contaduría Pública','Auditor Financiero','COMPETENCIAS',True,561,'1999 2003 2018','IXC.UABJB R:X C. UAP R:I-XIIIUAJMS'),
    ('ECONOMICAS','Potosí','Auditoría - Contaduría Pública','TUS',6,'Técnico Universitario Superior en Contabilidad','Contador General','COMPETENCIAS',True,562,'1999 2003','IXC.UABJB R:X C. UAP'),
    ('ECONOMICAS','Tupiza','Contaduría Pública-Auditoría','LIC',6,'Licenciado en Contaduría Pública-Auditoría','Auditor Financiero','COMPETENCIAS',True,570,'2003 2018 2025','X C. UAP R:I-XIIIUAJMS R:IV-XIIIUAJMS'),
    ('ECONOMICAS','Potosí','Contabilidad y Finanzas','LIC',6,'Licenciado en Contabilidad y Finanzas','Contador Financiero','COMPETENCIAS',True,573,'2009','I-XI UATF'),
    ('ECONOMICAS','Potosí','Administración de Empresas','LIC',6,'Licenciado en Administración de Empresas','Administrador de Empresas','OTRO',True,574,'1999 2003 2024','IXC.UABJB R:X C. UAP R: III-XIII UMRPSFX'),
    ('ECONOMICAS','Río Grande','Administración de Empresas','LIC',6,'Licenciado en Administración de Empresas','Administrador de Empresas','OTRO',True,575,'2025','IV-XIIIUAJMS'),
    # ── CIENCIAS PURAS ───────────────────────────────────────────────────────
    ('PURAS','Potosí','Ciencias Químicas','LIC',1,'Licenciado en Ciencias Químicas','Licenciado en Ciencias Químicas','COMPETENCIAS',True,591,'2025','R:IV-XIIIUAJMS'),
    ('PURAS','Uyuni','Ciencias Químicas','LIC',1,'Licenciado en Ciencias Químicas','Licenciado en Ciencias Químicas','COMPETENCIAS',True,592,'2025','R:IV-XIIIUAJMS'),
    ('PURAS','Potosí','Matemáticas','LIC',1,'Licenciado en Matemáticas','Matemático','COMPETENCIAS',True,593,'1999 2003 2025','IXC.UABJB R:X C. UAP R:IV-XIIIUAJMS'),
    ('PURAS','Potosí','Ingeniería Informática','LIC',2,'Licenciado en Ingeniería Informática','Ingeniero Informático','COMPETENCIAS',True,594,'2003 2023 2025','X C. UAP R:II-XIIIUAGRM R:IV-XIIIUAJMS'),
    ('PURAS','Potosí','Física','LIC',1,'Licenciado en Física','Licenciado en Física','COMPETENCIAS',True,600,'1999 2003','IXC.UABJB R:X C. UAP'),
    ('PURAS','Potosí','Estadística','LIC',1,'Licenciado en Estadística','Licenciado en Estadística','COMPETENCIAS',True,601,'1999 2003 2018','IXC.UABJB R:X C. UAP R:I-XIII UAJMS'),
    # ── CIENCIAS SOCIALES Y HUMANÍSTICAS ─────────────────────────────────────
    ('SOCIALES','Potosí','Turismo','LIC',5,'Licenciado en Turismo','Licenciado en Turismo','COMPETENCIAS',True,602,'1999 2003 2018','IXC. UABJB R:X C. UAP R:I-XIIIUAJMS'),
    ('SOCIALES','Potosí','Turismo','TUS',5,'Técnico Universitario Superior en Turismo','Técnico Universitario Superior en Turismo','COMPETENCIAS',True,603,'1999 2003 2018','IXC. UABJB R:X C. UAP R:I-XIIIUAJMS'),
    ('SOCIALES','Uyuni','Turismo','LIC',5,'Licenciado en Turismo','Licenciado en Turismo','COMPETENCIAS',True,604,'1999 2003 2018 2026','IXC. UABJB R:X C. UAP R:I-XIIIUAJMS V-XIII UAGRM'),
    ('SOCIALES','Uyuni','Turismo','TUS',5,'Técnico Universitario Superior en Turismo','Técnico Universitario Superior en Turismo','COMPETENCIAS',True,605,'1999 2003 2018 2026','V-XIII UAGRM'),
    ('SOCIALES','Potosí','Trabajo Social','LIC',5,'Licenciado en Trabajo Social','Licenciado en Trabajo Social','COMPETENCIAS',True,606,'1999 2003 2023','IXC. UABJB R:X C. UAP R:II-XIIIUAGRM'),
    ('SOCIALES','Uncía','Trabajo Social','LIC',5,'Licenciado en Trabajo Social','Licenciado en Trabajo Social','COMPETENCIAS',True,607,'2003 2018','X C. UAP R:I-XIIIUAJMS'),
    ('SOCIALES','Potosí','Lingüística e Idiomas','LIC',5,'Licenciado en Lingüística e Idiomas','Licenciado en Lingüística e Idiomas','COMPETENCIAS',True,608,'1999 2003 2018 2025','IXC. UABJB R:X C. UAP R:I-XIII UAJMS R:IV-XIIIUAJMS'),
    ('SOCIALES','Uyuni','Lingüística e Idiomas','LIC',5,'Licenciado en Lingüística e Idiomas','Licenciado en Lingüística e Idiomas','COMPETENCIAS',True,614,'2003 2018','X C. UAP R:I-XIII UAJMS'),
    ('SOCIALES','Potosí','Ciencias de la Comunicación Social','LIC',5,'Licenciado en Ciencias de la Comunicación','Licenciado en Ciencias de la Comunicación','COMPETENCIAS',True,616,'2015 2026','II-XII UTO V-XIII UAGRM'),
    # ── DERECHO ──────────────────────────────────────────────────────────────
    ('DERECHO','Potosí','Derecho','LIC',5,'Licenciado en Derecho','Abogado','COMPETENCIAS',True,617,'1999 2003 2018','IXC.UABJB R:X C. UAP R:I-XIII UAJMS'),
    ('DERECHO','Uncía','Derecho','LIC',5,'Licenciado en Derecho','Abogado','COMPETENCIAS',True,618,'2003 2018','X C. UAP R:I-XIIIUAJMS'),
    ('DERECHO','Tupiza','Derecho','LIC',5,'Licenciado en Derecho','Abogado','COMPETENCIAS',True,619,'2018','R:I-XIIIUAJMS'),
    # ── INGENIERÍA GEOLÓGICA ──────────────────────────────────────────────────
    ('GEOLOGICA','Potosí','Ingeniería Geológica','LIC',2,'Licenciado en Ingeniería Geológica','Ingeniero Geólogo','COMPETENCIAS',True,620,'1999 2003 2018','IXC.UABJB R:X C. UAP R:I-XIIIUAJMS'),
    ('GEOLOGICA','Potosí','Ingeniería Ambiental','LIC',2,'Licenciado en Ingeniería Ambiental','Ingeniero Ambiental','COMPETENCIAS',True,623,'2023','R:II-XIII UAGRM'),
    # ── INGENIERÍA MINERA ─────────────────────────────────────────────────────
    ('MINERA','Potosí','Ingeniería de Procesos de Materias Primas Minerales','LIC',2,'Licenciado en Ingeniería de Procesos de Materias Primas Minerales','Ingeniero de Procesos de Materias Primas Minerales','COMPETENCIAS',True,624,'2003','X C. UAP'),
    ('MINERA','Potosí','Ingeniería de Minas','LIC',2,'Licenciado en Ingeniería de Minas','Ingeniero de Minas','COMPETENCIAS',True,625,'2003 2024','X C. UAP R: III-XIII UMRPSFX'),
    # ── INGENIERÍA TECNOLÓGICA ────────────────────────────────────────────────
    ('TECNOLOGICA','Potosí','Mecánica Automotriz','TUM',2,'Técnico Universitario Medio en Mecánica Automotriz','Técnico Universitario Medio en Mecánica Automotriz','COMPETENCIAS',True,627,'2003','X C. UAP'),
    ('TECNOLOGICA','Potosí','Mecánica Automotriz','TUS',2,'Técnico Universitario Superior en Mecánica Automotriz','Técnico Universitario Superior en Mecánica Automotriz','COMPETENCIAS',True,628,'1999 2003','IXC.UABJB R.X C. UAP'),
    ('TECNOLOGICA','Potosí','Ingeniería Mecánica','LIC',2,'Licenciado en Ingeniería Mecánica','Ingeniero Mecánico','COMPETENCIAS',True,630,'2003 2023','X C. UAP R.II-XIII UAGRM'),
    ('TECNOLOGICA','Potosí','Ingeniería Mecánica','TUS',2,'Técnico Universitario Superior en Mecánica General','Técnico Universitario Superior en Mecánica General','COMPETENCIAS',True,631,'2003 2023','X C. UAP R:II-XIII UAGRM'),
    ('TECNOLOGICA','Potosí','Ingeniería Mecánica','TUM',2,'Técnico Universitario Medio en Mecánica General','Técnico Universitario Medio en Mecánica General','COMPETENCIAS',True,632,'2003','X C. UAP'),
    ('TECNOLOGICA','San Cristóbal','Ingeniería Mecánica','LIC',2,'Licenciado en Ingeniería Mecánica','Ingeniero Mecánico','COMPETENCIAS',True,634,'2025','IV-XIIIUAJMS'),
    ('TECNOLOGICA','Potosí','Ingeniería Mecatrónica','LIC',2,'Licenciado en Ingeniería Mecatrónica','Ingeniero Mecatrónico','COMPETENCIAS',True,636,'2023','R:II-XIII UAGRM'),
    ('TECNOLOGICA','Potosí','Ingeniería Mecatrónica','TUS',2,'Técnico Universitario Superior en Mecatrónica','Técnico Universitario Superior en Mecatrónica','COMPETENCIAS',True,637,'2023','R:II-XIII UAGRM'),
    ('TECNOLOGICA','Potosí','Ingeniería Electrónica','LIC',2,'Licenciado en Ingeniería Electrónica','Ingeniero Electrónico','COMPETENCIAS',True,638,'2003 2023','X C. UAP R:II-XIII UAGRM'),
    ('TECNOLOGICA','Potosí','Ingeniería Electrónica','TUS',2,'Técnico Universitario Superior en Electrónica','Técnico Universitario Superior en Electrónica','COMPETENCIAS',True,639,'2003 2023','X C. UAP R.II-XIII UAGRM'),
    ('TECNOLOGICA','Potosí','Ingeniería Electrónica','TUM',2,'Técnico Universitario Medio en Electrónica','Técnico Universitario Medio en Electrónica','COMPETENCIAS',True,640,'2003','X C. UAP'),
    ('TECNOLOGICA','Potosí','Ingeniería Eléctrica','LIC',2,'Licenciado en Ingeniería Eléctrica','Ingeniero Eléctrico','COMPETENCIAS',True,642,'2003 2023','X C. UAP R:II-XIIIUAGRM'),
    ('TECNOLOGICA','Potosí','Ingeniería Eléctrica','TUS',2,'Técnico Universitario Superior en Electricidad','Técnico Universitario Superior en Electricidad','COMPETENCIAS',True,643,'2003 2023','X C. UAP R:IIXIII UAGRM'),
    ('TECNOLOGICA','Potosí','Ingeniería Eléctrica','TUM',2,'Técnico Universitario Medio en Electricidad','Técnico Universitario Medio en Electricidad','COMPETENCIAS',True,644,'2003','X C. UAP'),
    ('TECNOLOGICA','San Cristóbal','Ingeniería Eléctrica','LIC',2,'Licenciado en Ingeniería Eléctrica','Ingeniero Eléctrico','COMPETENCIAS',True,646,'2025','IV-XIIIUAJMS'),
    ('TECNOLOGICA','Potosí','Ingeniería Industrial','LIC',2,'Licenciado en Ingeniería Industrial','Ingeniero Industrial','COMPETENCIAS',True,648,'2025','IV-XIIIUAJMS'),
    # ── INGENIERÍA ────────────────────────────────────────────────────────────
    ('INGENIERIA','Potosí','Geodesia y Topografía','LIC',2,'Licenciado en Geodesia y Topografía','Ingeniero en Geodesia y Topografía','COMPETENCIAS',True,650,'2009 2018','I-XI UATF R:I-XIII UAJMS'),
    ('INGENIERIA','Potosí','Geodesia y Topografía','TUS',2,'Técnico Universitario Superior en Topografía','Técnico Universitario Superior en Topografía','COMPETENCIAS',True,651,'1999 2003 2018','IV-VIII UABJB R:X C. UAP R:I-XIII UAJMS'),
    ('INGENIERIA','Potosí','Ingeniería Civil','LIC',2,'Licenciado en Ingeniería Civil','Ingeniero Civil','COMPETENCIAS',True,652,'1999 2003 2018','IV-VIIIUABJB R.X C. UAP R:I-XIIIUAJMS'),
    ('INGENIERIA','Potosí','Construcciones Civiles','TUS',2,'Técnico Universitario Superior en Construcciones Civiles','Técnico Universitario Superior en Construcciones Civiles','COMPETENCIAS',True,653,'1999 2003','IV-VIII UABJB R:X C. UAP'),
    # ── MEDICINA ─────────────────────────────────────────────────────────────
    ('MEDICINA','Potosí','Medicina','LIC',4,'Médico Cirujano','Médico Cirujano','COMPETENCIAS',True,654,'1999 2003 2024','IXC.UABJB R:X C. UAP R: III-XIII UMRPSFX'),
    # ── DSA (Dirección de Servicios Académicos) ───────────────────────────────
    ('DSA','Potosí','Odontología','LIC',4,'Licenciado en Odontología','Odontólogo','COMPETENCIAS',True,655,'2018','I-XIII UAJMS'),
    ('DSA','Potosí','Ingeniería de Sistemas','LIC',2,'Licenciado en Ingeniería de Sistemas','Ingeniero de Sistemas','COMPETENCIAS',True,656,'2018','R:I-XIII UAJMS'),
    ('DSA','Tupiza','Ingeniería de Sistemas','LIC',2,'Licenciado en Ingeniería de Sistemas','Ingeniero de Sistemas','COMPETENCIAS',True,657,'2018','R:I-XIII UAJMS'),
]

carrera_map = {}  # (fac_clave, ciudad, nombre, grado) → Carrera
for row in CARRERAS_DATA:
    (fac_clave, ciudad, nombre, grado, area,
     diploma, titulo, enfoque, en_func, num_sub,
     anio_str, resolucion) = row

    sede = get_sede(fac_clave, ciudad)
    if not sede:
        print(f"  ⚠️  Sede no encontrada: {fac_clave}/{ciudad} para {nombre}")
        continue

    grado_val = GRADO_MAP.get(grado, 'LIC')
    tipo_val  = 'C' if ciudad == 'Potosí' else 'D'
    enfoque_val = ENFOQUE_MAP.get(enfoque, '')

    obj, created = Carrera.objects.update_or_create(
        sede=sede,
        nombre=nombre,
        grado=grado_val,
        defaults={
            'area':               area,
            'tipo':               tipo_val,
            'diploma_academico':  diploma,
            'titulo_profesional': titulo,
            'enfoque_curricular': enfoque_val,
            'en_funcionamiento':  en_func,
            'numero_sub':         num_sub,
            'observaciones':      f'Resolución: {resolucion}',
        }
    )
    carrera_map[(fac_clave, ciudad, nombre, grado)] = obj
    print(f"  {'✅' if created else '🔄'} [{grado}] {nombre} — {ciudad}")

    # Crear plan de estudio con el último año de la cadena
    anios = [a.strip() for a in anio_str.split() if a.strip().isdigit()]
    if anios:
        ultimo_anio = int(anios[-1])
        PlanEstudio.objects.update_or_create(
            carrera=obj,
            anio_aprobacion=ultimo_anio,
            defaults={
                'evento_aprobacion': resolucion[:100] if resolucion else '',
                'activo':            True,
            }
        )


# ════════════════════════════════════════════════════════════
# PASO 5 — PROGRAMAS (en proceso, no son carreras oficiales)
# ════════════════════════════════════════════════════════════
print("\n[5/6] Creando Programas en proceso...")

# (fac_clave, ciudad, nombre, area, grado_previsto,
#  estado, responsable, anio_inicio, observaciones)
PROGRAMAS_DATA = [
    # Programas DSA — en implementación o aprobación
    ('DSA','Potosí','Programa de Pedagogía Intercultural',5,'LIC','IMPLEMENTACION','DSA UATF',2023,'Programa cíclico - II-XIII UAGRM'),
    ('DSA','Potosí','Programa Ingeniería en Diseño y Programación Digital',2,'LIC','IMPLEMENTACION','DSA UATF',2023,'Programa cíclico autofinanciado - II-XIII UAGRM'),
    # Programas nuevos Auditoría
    ('ECONOMICAS','Potosí','Tributación (Prog. TUM)',6,'TEC','IMPLEMENTACION','Fac. Cs. Económicas',2025,'IV-XIIIUAJMS'),
    ('ECONOMICAS','Potosí','Exportación de Minerales e Importación de Insumos Mineros',6,'TEC','IMPLEMENTACION','Fac. Cs. Económicas',2025,'IV-XIIIUAJMS'),
    ('ECONOMICAS','Potosí','Control Gubernamental (Prog. TUM)',6,'TEC','IMPLEMENTACION','Fac. Cs. Económicas',2025,'IV-XIIIUAJMS'),
    ('ECONOMICAS','Potosí','Operaciones Bancarias (Prog. TUM)',6,'TEC','IMPLEMENTACION','Fac. Cs. Económicas',2025,'IV-XIIIUAJMS'),
    ('ECONOMICAS','Potosí','Gestión Pública (Prog. TUS)',6,'TUS','IMPLEMENTACION','Fac. Cs. Económicas',2024,'III-XIII UMRPSFX'),
    ('ECONOMICAS','Potosí','Gestión de Marketing (Prog. TUS)',6,'TUS','IMPLEMENTACION','Fac. Cs. Económicas',2024,'III-XIII UMRPSFX'),
    ('ECONOMICAS','Potosí','Gestión de Recursos Humanos (Prog. TUS)',6,'TUS','IMPLEMENTACION','Fac. Cs. Económicas',2024,'III-XIII UMRPSFX'),
    ('ECONOMICAS','Potosí','Gestión de Finanzas (Prog. TUS)',6,'TUS','IMPLEMENTACION','Fac. Cs. Económicas',2024,'III-XIII UMRPSFX'),
    ('ECONOMICAS','Potosí','Gestión de Empresas Turísticas (Prog. TUS)',6,'TUS','IMPLEMENTACION','Fac. Cs. Económicas',2024,'III-XIII UMRPSFX'),
    ('ECONOMICAS','Villazón','Comercio Internacional',6,'LIC','IMPLEMENTACION','Fac. Cs. Económicas',2025,'IV-XIIIUAJMS'),
    # Programas Ingeniería Informática
    ('PURAS','Potosí','Desarrollo de Sistemas Informáticos (TUS)',2,'TUS','IMPLEMENTACION','Fac. Cs. Puras',2025,'IV-XIIIUAJMS'),
    ('PURAS','Potosí','Administrador de Bases de Datos (TUS)',2,'TUS','IMPLEMENTACION','Fac. Cs. Puras',2025,'IV-XIIIUAJMS'),
    ('PURAS','Potosí','Redes y Ciberseguridad (TUS)',2,'TUS','IMPLEMENTACION','Fac. Cs. Puras',2025,'IV-XIIIUAJMS'),
    # Programas Lingüística
    ('SOCIALES','Potosí','Competencia Comunicativa Multilingüe (TUS)',5,'TUS','IMPLEMENTACION','Fac. Cs. Sociales',2025,'IV-XIIIUAJMS'),
    # Programas Ing. Tecnológica San Cristóbal
    ('TECNOLOGICA','San Cristóbal','Mecánica Automotriz (TUS)',2,'TUS','IMPLEMENTACION','Fac. Ing. Tecnológica',2025,'IV-XIIIUAJMS'),
    ('TECNOLOGICA','San Cristóbal','Mecánica (TUS)',2,'TUS','IMPLEMENTACION','Fac. Ing. Tecnológica',2025,'IV-XIIIUAJMS'),
    ('TECNOLOGICA','San Cristóbal','Ingeniería Eléctrica (TUS)',2,'TUS','IMPLEMENTACION','Fac. Ing. Tecnológica',2025,'IV-XIIIUAJMS'),
    # Programas en formulación
    ('ARTES','Potosí','Restauración',5,'LIC','FORMULACION','Fac. Artes',2015,'II-XII UTO — en formulación'),
    ('AGRICOLAS','Potosí','Ingeniería en Desarrollo Rural',3,'LIC','FORMULACION','Fac. Agrícolas',2010,'Carrera suspendida temporalmente'),
    ('ECONOMICAS','Tupiza','Contaduría Pública (anterior)',6,'LIC','FORMULACION','Fac. Cs. Económicas',2003,'Reemplazada por Contaduría Pública-Auditoría'),
    ('DSA','Potosí','Programa Cíclico: Pedagogía Intercultural',5,'LIC','APROBACION','DSA UATF',2023,'II-XIII UAGRM'),
    ('TECNOLOGICA','Potosí','Ingeniería Autotrónica (Prog. Complementación)',2,'LIC','FORMULACION','Fac. Ing. Tecnológica',2026,'V-XIIIUAGRM — en formulación'),
    # Río Grande
    ('ECONOMICAS','Río Grande','Administración de Empresas — Río Grande',6,'LIC','IMPLEMENTACION','Fac. Cs. Económicas',2025,'IV-XIIIUAJMS'),
    # Tupiza DSA
    ('DSA','Tupiza','Programa Derecho — Tupiza',5,'LIC','IMPLEMENTACION','DSA Tupiza',2018,'R:I-XIIIUAJMS'),
    # Uncía DSA
    ('DSA','Uncía','Programa Ingeniería de Sistemas — Uncía',2,'LIC','APROBACION','DSA Uncía',2018,'R:I-XIII UAJMS'),
]

ESTADO_MAP = {
    'FORMULACION':   'FORMULACION',
    'APROBACION':    'APROBACION',
    'IMPLEMENTACION':'IMPLEMENTACION',
    'SUSPENDIDO':    'SUSPENDIDO',
}
GRADO_PROG_MAP = {'LIC':'LIC','TUS':'TUS','TUM':'TEC','TEC':'TEC','':''}

for row in PROGRAMAS_DATA:
    (fac_clave, ciudad, nombre, area, grado_prev,
     estado, responsable, anio, obs) = row

    sede = get_sede(fac_clave, ciudad)
    if not sede:
        print(f"  ⚠️  Sede no encontrada: {fac_clave}/{ciudad} para prog. {nombre}")
        continue

    obj, created = Programa.objects.update_or_create(
        sede=sede,
        nombre=nombre,
        defaults={
            'area':             area,
            'grado_previsto':   GRADO_PROG_MAP.get(grado_prev, ''),
            'estado':           ESTADO_MAP.get(estado, 'FORMULACION'),
            'responsable':      responsable,
            'fecha_inicio':     None,
            'observaciones':    obs,
            'activo':           True,
        }
    )
    print(f"  {'✅' if created else '🔄'} [{estado}] {nombre} — {ciudad}")


# ════════════════════════════════════════════════════════════
# PASO 6 — TIPOS DE FASE + PROCESOS DE REDISEÑO
# ════════════════════════════════════════════════════════════
print("\n[6/6] Creando Tipos de Fase y Procesos de Rediseño...")

# Tipos de fase del proceso de rediseño curricular UATF/CEUB
TIPOS_FASE = [
    ('F01', 'Solicitud Jornada Académica',      'Solicitud formal para iniciar el proceso de rediseño ante la Jornada Académica.',        'Acta de solicitud firmada por el Director de Carrera',  1),
    ('F02', 'Diagnóstico Inicial',               'Análisis del estado actual del currículo vigente.',                                        'Informe de diagnóstico curricular',                      2),
    ('F03', 'Estudio de Contexto',               'Investigación del contexto social, laboral y académico.',                                  'Documento de estudio de contexto',                       3),
    ('F04', 'Mesa Multisectorial',               'Reunión con actores externos: empleadores, egresados, sociedad.',                          'Acta y memorias de la Mesa Multisectorial',              4),
    ('F05', 'Macro Currículum',                  'Definición del perfil profesional, objetivos y estructura general.',                       'Documento de Macro Currículo aprobado',                  5),
    ('F06', 'Reunión Académica de Carrera (RAC)','Reunión con CEUB para revisión y aprobación del Macro Currículo.',                        'Resolución de la RAC - CEUB',                            6),
    ('F07', 'Comisión Académica',                'Revisión técnica por parte de la Comisión Académica del HCU.',                             'Informe de la Comisión Académica',                       7),
    ('F08', 'Homologación HCU',                  'Aprobación formal del rediseño por el Honorable Consejo Universitario.',                   'Resolución HCU de homologación',                         8),
    ('F09', 'Reunión Académica Nacional (RAN)',  'Aprobación a nivel nacional del Sistema de la Universidad Boliviana.',                     'Resolución de la RAN - CEUB',                            9),
    ('F10', 'Micro Currículum',                  'Elaboración de los programas analíticos de cada materia.',                                 'Programas analíticos aprobados por la Comisión Docente', 10),
]

for codigo, nombre, desc, medio, orden in TIPOS_FASE:
    obj, created = TipoFase.objects.update_or_create(
        codigo=codigo,
        defaults={
            'nombre':                      nombre,
            'descripcion':                 desc,
            'medio_verificacion_default':  medio,
            'orden':                       orden,
            'activa':                      True,
        }
    )
    print(f"  {'✅' if created else '🔄'} {codigo} — {nombre}")

# Mapa de tipos de fase
tf = {c: TipoFase.objects.get(codigo=c) for c, *_ in TIPOS_FASE}

# Carreras con progreso de rediseño según el documento DSA (junio 2025)
# Formato: (fac_clave, ciudad, nombre_carrera, grado,
#           fases_completadas_lista, estado_proceso)
# Las fases completadas son los códigos de fase que tienen ">>" en el doc DSA.
REDISENOS = [
    ('ARTES',    'Potosí','Artes Plásticas','LIC',
     ['F01','F02','F03','F04','F05','F06','F09','F10'], 'EN_PROCESO'),
    ('ARTES',    'Potosí','Artes Musicales','LIC',
     ['F01','F02','F03'], 'EN_PROCESO'),
    ('AGRICOLAS','Potosí','Ingeniería Agronómica','LIC',
     ['F01','F02','F03','F04','F05','F06','F09','F10'], 'EN_PROCESO'),
    ('AGRICOLAS','Potosí','Ingeniería Agroindustrial','LIC',
     ['F01'], 'EN_PROCESO'),
    ('ECONOMICAS','Potosí','Auditoría - Contaduría Pública','LIC',
     ['F01','F02','F03','F04','F05','F06','F09','F10'], 'EN_PROCESO'),
    ('ECONOMICAS','Potosí','Administración de Empresas','LIC',
     ['F01','F02','F03'], 'EN_PROCESO'),
    ('PURAS',    'Potosí','Estadística','LIC',
     ['F01','F02','F03','F04','F05','F06','F09'], 'EN_PROCESO'),
    ('PURAS',    'Potosí','Física','LIC',
     ['F01','F02','F03','F04'], 'EN_PROCESO'),
    ('PURAS',    'Potosí','Ingeniería Informática','LIC',
     ['F01','F02','F03'], 'EN_PROCESO'),
    ('SOCIALES', 'Uncía','Trabajo Social','LIC',
     ['F01','F02','F03','F04','F05','F06','F09'], 'EN_PROCESO'),
    ('SOCIALES', 'Potosí','Lingüística e Idiomas','LIC',
     ['F01','F02','F03','F04','F05','F06','F09'], 'EN_PROCESO'),
    ('SOCIALES', 'Potosí','Trabajo Social','LIC',
     ['F01','F02','F03'], 'EN_PROCESO'),
    ('SOCIALES', 'Potosí','Turismo','LIC',
     ['F01','F02','F03','F04','F05','F06','F09','F10'], 'EN_PROCESO'),
    ('SOCIALES', 'Uyuni','Turismo','LIC',
     ['F01','F02','F03','F04','F05','F06'], 'EN_PROCESO'),
    ('DERECHO',  'Potosí','Derecho','LIC',
     ['F01','F02','F03','F04','F05','F06','F09','F10'], 'EN_PROCESO'),
    ('DERECHO',  'Uncía','Derecho','LIC',
     ['F01','F02','F03','F04','F05','F06'], 'EN_PROCESO'),
    ('INGENIERIA','Potosí','Ingeniería Civil','LIC',
     ['F01','F02','F03','F04','F05','F06','F09'], 'EN_PROCESO'),
    ('INGENIERIA','Potosí','Geodesia y Topografía','LIC',
     ['F01','F02','F03','F04','F05','F06','F09','F10'], 'EN_PROCESO'),
    ('GEOLOGICA','Potosí','Ingeniería Geológica','LIC',
     ['F01','F02','F03','F04','F05','F06','F09','F10'], 'EN_PROCESO'),
    ('GEOLOGICA','Potosí','Ingeniería Ambiental','LIC',
     ['F01','F02','F03','F04','F05'], 'EN_PROCESO'),
    ('SALUD',    'Potosí','Enfermería','LIC',
     ['F01','F02','F03','F04','F05','F06','F09','F10'], 'EN_PROCESO'),
    ('SALUD',    'Villazón','Enfermería','LIC',
     ['F01','F02','F03','F04','F05','F06','F10'], 'EN_PROCESO'),
    ('DSA',      'Potosí','Ingeniería de Sistemas','LIC',
     ['F01','F02','F03','F04','F05','F06','F09'], 'EN_PROCESO'),
]

for fac_clave, ciudad, nombre_c, grado, fases_comp, estado_proc in REDISENOS:
    grado_val = GRADO_MAP.get(grado, 'LIC')
    carrera = Carrera.objects.filter(
        sede__facultad=fac_map[fac_clave],
        sede__ciudad=ciudad,
        nombre=nombre_c,
        grado=grado_val,
    ).first()

    if not carrera:
        print(f"  ⚠️  Carrera no encontrada para proceso: {nombre_c} ({ciudad})")
        continue

    proceso, p_created = ProcesoCurricular.objects.update_or_create(
        carrera=carrera,
        tipo_proceso='REDISENO',
        anio_inicio=2024,
        defaults={
            'nombre_proceso': f'Rediseño Curricular {nombre_c} — UATF 2024-2025',
            'estado':         estado_proc,
            'observaciones':  'Seguimiento según tabla DSA-UATF noviembre 2025',
        }
    )
    print(f"  {'✅' if p_created else '🔄'} Proceso: {nombre_c} — {len(fases_comp)} fases")

    # Crear fases
    for codigo_fase in ['F01','F02','F03','F04','F05','F06','F07','F08','F09','F10']:
        estado_fase = 'COMPLETADO' if codigo_fase in fases_comp else 'PENDIENTE'
        FaseProceso.objects.update_or_create(
            proceso=proceso,
            tipo_fase=tf[codigo_fase],
            defaults={
                'estado':               estado_fase,
                'medio_verificacion':   tf[codigo_fase].medio_verificacion_default,
                'observaciones':        '',
            }
        )


# ════════════════════════════════════════════════════════════
# RESUMEN FINAL
# ════════════════════════════════════════════════════════════
print("\n" + "=" * 60)
print("✅ CARGA COMPLETADA")
print("=" * 60)
print(f"  Universidades:  {Universidad.objects.count()}")
print(f"  Facultades:     {Facultad.objects.count()}")
print(f"  Sedes:          {Sede.objects.count()}")
print(f"  Carreras:       {Carrera.objects.count()}")
print(f"  Planes estudio: {PlanEstudio.objects.count()}")
print(f"  Programas:      {Programa.objects.count()}")
print(f"  Tipos de fase:  {TipoFase.objects.count()}")
print(f"  Procesos:       {ProcesoCurricular.objects.count()}")
print(f"  Fases:          {FaseProceso.objects.count()}")
print("=" * 60)
print("\nPara ejecutar:")
print("  python manage.py shell < cargar_datos_uatf.py")
print("\nO copia el archivo a la raíz del proyecto y ejecuta:")
print("  python manage.py shell")
print("  >>> exec(open('cargar_datos_uatf.py').read())")