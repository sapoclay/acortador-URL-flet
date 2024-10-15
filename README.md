# Acortador de URL's con Flet y Python

![about-acortador-urls](https://github.com/user-attachments/assets/b349ccbc-4c1d-4551-ab0c-02471ac0327b)

Este proyecto es una pequeña aplicación de escritorio construida con **Flet** que permite acortar URLs largas a versiones más cortas utilizando varios servicios gratuitos de acortamiento de URLs.

## Características

- Con esta aplicación el usuario podrá acortar URLs utilizando servicios como **TinyURL**, **clck.ru**, **is.gd** y **dagd**, entre otros. Todos estos servicios son los que aparecen incluidos en el paquete [pyshorteners](https://pyshorteners.readthedocs.io/en/latest/apis.html#da-gd) que no requieren una API Key.
- Una vez generadas las URL acortadas, podremos opiar el enlace acortado al portapapeles con un solo clic. Además también nos permitirá abrir el enlace acortado directamente en el navegador (que no tiene mucho sentido, pero ahí está!!)
- También podremos cambiar entre temas claro y oscuro.
- Bandeja del sistema con icono. Actualmente este icono solo sirve para ver que la aplicación está abierta.
- Cuenta con una ventana 'Acerca de' con una pequeña información sobre la aplicación.
- Además, antes de cerrar la aplicación aparecerá una ventana de confirmación, ya que una vez cerrada perderemos las URL's cortas que tengamos generadas.

## Servicios de acortamiento de URLs utilizados

La aplicación utiliza el módulo `pyshorteners` para interactuar con varios servicios de acortamiento de URLs que por el momento no requieren API KEY:

- [TinyURL](https://tinyurl.com)
- [clck.ru](https://clck.ru)
- [is.gd](https://is.gd)
- [dagd](https://da.dg)
- [osdb.link](https://osdb.link)

## Capturas de pantalla

![pantalla-inicio](https://github.com/user-attachments/assets/940471cd-60dc-4a43-8dbc-7c9801389a40)

![mensaje-url-acortadas](https://github.com/user-attachments/assets/78aed082-5ada-44b9-9f5e-0df6ba93cb04)

![urls-acortadas](https://github.com/user-attachments/assets/16bdf5b8-443d-4882-8ca0-b53712f08146)

### Pantalla principal
Muestra un campo de texto donde el usuario escribiŕa la URL que se desea acortar. Tan solo hay que pulsar el botón "Acortar!" y comenzará a aparecer una lista de URLs acortadas con opciones para copiar y abrirlas. En algunas ocasiones es posible que alguno de los servicios de acortamiento no funcione por motivos ajenos a la aplicación. En este caso, debería aparecer un mensaje en la parte inferior de la aplicación.


## Cómo ejecutar el proyecto

>[NOTA!]
>Al iniciar por pimera vez la aplicación, puede tardar un poco por que la primera vez se tiene que crear el entorno virtual y se tienen que instalar las dependencias. La segunda vez el inicio ya debería ser mucho más rápido.

### Requisitos previos

- Python 3.10+
- Entorno virtual configurado con las dependencias listadas en `requirements.txt`.
- Flet instalado, junto con otras bibliotecas necesarias como `pyshorteners`, `Pillow` y `pystray`.

### Instalación y ejecución

1. Clona este repositorio:
    ```bash
    git clone https://github.com/sapoclay/acortador-URL-flet
    cd acortador-URL-flet
    ```

2. Ejecuta el script `run_app.py`, que automáticamente verificará la existencia de un entorno virtual y las dependencias. Si no existen, las instalará antes de lanzar la aplicación.

    ```bash
    python run_app.py
    ```

----- Paquete .DEB -----

1. Descarga el paquete .deb abriendo una terminal (Ctrl+Alt+T) y ejecuta:

```
wget https://github.com/sapoclay/acortador-URL-flet/releases/download/0.5/acortadorURLs.deb
```

2. El siguiente paso es proceder a la instalación del paquete descargado:

```
sudo dpkg -i acortadorURLs.deb
```

3. Tras la instalación ya tiene que poder ejecutar el programa buscando el lanzador en tu equipo.

![acortadorURLs-icono](https://github.com/user-attachments/assets/1f314386-5e84-4ede-9f8f-888f0042c9ae)

#### Próximamente 

- Esta aplicación me va a resultar útil para algunas cosas, por lo que más pronto que tarde estará disponible también como paquete .EXE. Pero esto lo haré cuando tenga tiempo.

### Notas

- La aplicación carga un ícono de `assets/icons/loading-animation.png` que aparece al iniciar la aplicación como una pantalla de carga.
- El ícono de la bandeja del sistema utiliza una imagen desde el mismo directorio de `assets/icons`.

### Personalización

- Para cambiar el ícono de la bandeja, simplemente reemplaza `loading-animation.png` por tu propia imagen en el directorio `assets/icons/`.
- Si deseas añadir más servicios de acortamiento de URLs, puedes modificar el archivo `main.py` y añadir más métodos de `pyshorteners` o cualquier otro servicio de tu elección.

## Contribuciones

¡Las contribuciones son bienvenidas! Si encuentras algún problema o tienes alguna sugerencia, no dudes en abrir un issue o enviar un pull request.

## Licencia

Este proyecto está bajo la licencia MIT. Para más detalles, revisa el archivo [LICENSE](LICENSE).
