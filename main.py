import flet as ft
import pystray
from pystray import MenuItem as Item, Icon
from PIL import Image
import asyncio
import threading
import pyshorteners

shortener = pyshorteners.Shortener()

class ShortLinkRow(ft.Row):
    def __init__(self, shortened_link, link_source):
        super().__init__()
        self.tooltip = link_source
        self.alignment = "center"
        self.controls = [
            ft.Text(value=shortened_link, size=16, selectable=True, italic=True),
            ft.IconButton(
                icon=ft.icons.COPY,
                on_click=lambda e: self.copy(shortened_link),
                bgcolor=ft.colors.PURPLE_700,
                tooltip="Copiar"
            ),
            ft.IconButton(
                icon=ft.icons.OPEN_IN_BROWSER_OUTLINED,
                tooltip="Abrir en el navegador web",
                on_click=lambda e: e.page.launch_url(shortened_link)
            )
        ]

    def copy(self, value):
        self.page.set_clipboard(value)
        snack_bar = ft.SnackBar(ft.Text("Link copiado al portapapeles!"), open=True)
        self.page.overlay.append(snack_bar)  # Añadir el SnackBar a la página
        self.page.update()  # Actualizar la página para que se muestre el SnackBar


async def hide_splash(page, splash_image):
    await asyncio.sleep(3)  # Esperar 3 segundos
    splash_image.visible = False
    page.update()

def on_quit(page):
    page.window.close()

def create_tray_icon(page):
    def quit_action(icon, item):
        icon.stop()
        on_quit(page)

    image = Image.open("./assets/icons/loading-animation.png")  # Ajusta a tu icono deseado
    icon = pystray.Icon("URL Shortener", image, menu=pystray.Menu(
        Item('Mostrar ventana', lambda: None),  # Puedes añadir más acciones aquí
        Item('Salir', lambda icon, item: quit_action(icon, item))
    ))
    
    def run_tray():
        icon.run()

    tray_thread = threading.Thread(target=run_tray, daemon=True)
    tray_thread.start()

async def main(page: ft.Page):
    page.title = "Acortador de URL"
    page.theme_mode = "dark"
    page.horizontal_alignment = "center"
    page.window.width = 540
    page.window.height = 640
    page.scroll = "hidden"
    # Hacer que la ventana no sea redimensionable
    #page.window.resizable = False

    # Splash image (loading)
    splash_image = ft.Image(
        src="./assets/icons/loading-animation.png",
        width=page.window.width,
        height=page.window.height,
        visible=True
    )
    page.overlay.append(splash_image)
    page.update()

    await hide_splash(page, splash_image)

    page.fonts = {
        "sf-simple": "/fonts/San-Francisco/SFUIDisplay-Light.ttf",
        "sf-bold": "/fonts/San-Francisco/SFUIDisplay-Bold.ttf"
    }
    
    page.theme = ft.Theme(font_family="sf-simple")

    def mostrar_snackbar(mensaje):
        snack_bar = ft.SnackBar(ft.Text(mensaje), open=True)
        page.overlay.append(snack_bar)
        page.update()

    def change_theme(e):
        page.theme_mode = "light" if page.theme_mode == "dark" else "dark"
        theme_icon_button.selected = not theme_icon_button.selected
        page.update()

    def shorten(e: ft.ControlEvent):
        user_link = text_field.value
        if user_link:
            page.add(ft.Text(f"URL Larga: {text_field.value}", italic=False, weight=ft.FontWeight.BOLD))
            try:
                page.add(ShortLinkRow(shortener.tinyurl.short(text_field.value), "Source: tinyurl.com"))
                page.add(ShortLinkRow(shortener.osdb.short(text_field.value), "Source: osdb.link"))
                page.add(ShortLinkRow(shortener.clckru.short(text_field.value), "Source: clck.ru"))
                page.add(ShortLinkRow(shortener.dagd.short(text_field.value), "Source: da.dg"))
                page.add(ShortLinkRow(shortener.isgd.short(text_field.value), "Source: is.gd"))
                mostrar_snackbar("URL acortada con éxito!")
                
            except Exception as exception:
                print(exception)
                mostrar_snackbar(f"Ocurrió un error: {str(exception)}")
            page.update()

    close_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("¿Estás seguro de que quieres salir?"),
        content=ft.Text("Cualquier progreso no guardado se perderá."),
        actions=[
            ft.TextButton("Sí", on_click=lambda e: page.window.destroy()),  # Cerrar la aplicación
            ft.TextButton("No", on_click=lambda e: page.close(close_dialog)),  # Cerrar el diálogo
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    
    # Diálogo Acerca de
    def show_about_dialog(e):
        about_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Acerca de", color=ft.colors.WHITE10),
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Image(src="./assets/icons/logo.png", width=100, height=100),
                        ft.Text(
                            "Esta es una pequeña aplicación\n que permite acortar URL's largas\n a URL's cortas utilizando\n servicios gratuitos que hay en Internet.",
                            text_align=ft.TextAlign.CENTER,
                            color=ft.colors.WHITE
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=10
                ),
                padding=ft.padding.all(10),  # Padding ajustado correctamente
                width=300,  # Ancho fijo para el diálogo
                height=250,  # Altura máxima controlada
                alignment=ft.alignment.center  # Centrar contenido dentro del contenedor
            ),
            actions=[
                ft.TextButton("Cerrar", on_click=lambda e: page.close(about_dialog))
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            bgcolor=ft.colors.BLACK,
            inset_padding=ft.Padding(20, 20, 20, 20),  # Padding externo ajustado
        )
        page.overlay.append(about_dialog)
        about_dialog.open = True
        page.update()
    
    # Mostrar el cuadro de diálogo cuando se selecciona "Salir" del menú
    def confirm_exit(e):
        page.overlay.append(close_dialog)   # Asigna el diálogo a la página
        close_dialog.open = True  # Abre el diálogo
        page.update()

    # Cambiar tema
    theme_icon_button = ft.IconButton(
        ft.icons.DARK_MODE,
        selected=False,
        selected_icon=ft.icons.LIGHT_MODE,
        icon_size=35,
        tooltip="Cambiar tema",
        on_click=change_theme,
        style=ft.ButtonStyle(color={"": ft.colors.BLACK, "seleccionado": ft.colors.WHITE}),
    )

    # Crear el menú
    menu = ft.PopupMenuButton(
        items=[
            ft.PopupMenuItem(text="Acerca de", on_click=show_about_dialog),  # Opción Acerca de
            ft.PopupMenuItem(text="Ver código fuente", on_click=lambda e: page.launch_url("https://github.com/sapoclay/acortador-URL-flet")),
            ft.PopupMenuItem(text="Salir", on_click=confirm_exit),
        ]
    )

    # Asignar el appbar con el menú
    page.appbar = ft.AppBar(
        title=ft.Text("Acortador URL", color="white"),
        center_title=True,
        bgcolor="purple",
        actions=[theme_icon_button, menu],
    )

    # Añadir el campo de texto para la URL y el texto explicativo
    page.add(
        text_field := ft.TextField(
            value='https://github.com/sapoclay',
            label="URL Larga",
            hint_text="Escribe la URL larga aquí",
            max_length=200,
            width=800,
            keyboard_type=ft.KeyboardType.URL,
            suffix=ft.FilledButton("Acortar!", on_click=shorten),
            on_submit=shorten
        ),
        ft.Text("URL's generadas:", weight=ft.FontWeight.BOLD, size=23, font_family="sf-bold")
    )

    # Crear el icono en la bandeja del sistema
    create_tray_icon(page)

    # Manejar el evento de cierre de la ventana
    def handle_window_event(e):
        if e.data == "close":
            page.open(close_dialog)  # Abrir el diálogo de confirmación

    page.window.prevent_close = True  # Evitar el cierre directo
    page.window.on_event = handle_window_event  # Asignar el manejador al evento de ventana


    page.update()

# Ejecutar la aplicación
ft.app(target=main, view=ft.AppView.FLET_APP, assets_dir='assets')
