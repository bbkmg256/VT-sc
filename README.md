# \[Vomiting-Things!]

Imageboard para vomitar y debatir ideas! :)

### \[Dependencias]
- django
- gunicorn
- pillow
- configparser (Obsoleto, pendiente remover)
- django-minify-html
- django-stubs (Para el servidor de lenguaje Pyrefly)
- python-dotenv

### \[Variables de entorno]

El proyecto tiene una serie de variables de entornos configurables que deben ir en un fichero de variables de entorno **.env** en la raiz del proyecto:

- SETTING_FILE: Para establecer el modulo de configuración del proyecto (Alojados en /src/core/settings/)

(Pendiente cargar el resto de variables...)

### \[Árbol de dirs.]
```text
.
├── capturas
├── requirements
├── src
│   ├── apps
│   │   ├── posts
│   │   │   └── migrations
│   │   └── tablon
│   │       └── migrations
│   └── core
│       └── settings
├── statics
│   ├── banners
│   └── css
├── templates
│   ├── core
│   ├── posts
│   └── tablon
└── tools
```
Nota: Actualmente existe un directorio pensado para alojar scripts de instalación y preparación del entorno para desplegar el proyecto, esto todvía está en desarrollo, porfavor no usar ni ejecutar nada de ahí :)

### \[Página inicial]

![Captura](./capturas/2026-08-14_05-02-22.jpg)
