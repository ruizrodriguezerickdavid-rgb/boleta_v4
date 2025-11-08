import flet as ft
import csv

def main(page: ft.Page):
    page.title = "Boleta de calificaciones"
    page.bgcolor = "grey"
    page.window_width = 1600
    page.window_height = 600

    lista_alumnos = ft.Dropdown(
        width=150,
        label="Alumnos",
        options=[
            ft.dropdown.Option("pipepino"),
            ft.dropdown.Option("titanhhamer"),
            ft.dropdown.Option("elmaau"),
            ft.dropdown.Option("aimp3"),
            ft.dropdown.Option("capitan cp"),
            ft.dropdown.Option("xiaro"),
        ],
    )

    esp = ft.Dropdown(
        width=150,
        label="Español",
        options=[ft.dropdown.Option(str(i)) for i in range(10, 101, 10)]
    )

    mat = ft.Dropdown(
        width=160,
        label="Matemáticas",
        options=[ft.dropdown.Option(str(i)) for i in range(10, 101, 10)]
    )

    ing = ft.Dropdown(
        width=130,
        label="Inglés",
        options=[ft.dropdown.Option(str(i)) for i in range(10, 101, 10)]
    )

    info = ft.Dropdown(
        width=140,
        label="Informática",
        options=[ft.dropdown.Option(str(i)) for i in range(10, 101, 10)]
    )

    hist = ft.Dropdown(
        width=135,
        label="Historia",
        options=[ft.dropdown.Option(str(i)) for i in range(10, 101, 10)]
    )

    bio = ft.Dropdown(
        width=180,
        label="Biología",
        options=[ft.dropdown.Option(str(i)) for i in range(10, 101, 10)]
    )

    art = ft.Dropdown(
        width=180,
        label="Artes",
        options=[ft.dropdown.Option(str(i)) for i in range(10, 101, 10)]
    )

    label_promedio = ft.Text(value="", size=20, width=100, color="white")

    tabla_calificaciones = ft.DataTable(
        columns=[
            ft.DataColumn(label=ft.Text("Alumno")),
            ft.DataColumn(label=ft.Text("Español")),
            ft.DataColumn(label=ft.Text("Matemáticas")),
            ft.DataColumn(label=ft.Text("Inglés")),
            ft.DataColumn(label=ft.Text("Informática")),
            ft.DataColumn(label=ft.Text("Historia")),
            ft.DataColumn(label=ft.Text("Biología")),
            ft.DataColumn(label=ft.Text("Artes")),
            ft.DataColumn(label=ft.Text("Promedio")),
        ],
        rows=[]
    )

    # ---- FUNCIONES ----
    def calcular_promedio(e):
        alumno = lista_alumnos.value
        if not alumno:
            page.snack_bar = ft.SnackBar(ft.Text("Selecciona un alumno."), bgcolor="red")
            page.snack_bar.open = True
            page.update()
            return

        # Verificar si el alumno ya está en la tabla
        for fila in tabla_calificaciones.rows:
            if fila.cells[0].content.value == alumno:
                page.snack_bar = ft.SnackBar(ft.Text(f"El alumno '{alumno}' ya fue registrado."), bgcolor="orange")
                page.snack_bar.open = True
                page.update()
                return

        # Calcular promedio
        notas = [
            int(esp.value or 0),
            int(mat.value or 0),
            int(ing.value or 0),
            int(info.value or 0),
            int(hist.value or 0),
            int(bio.value or 0),
            int(art.value or 0),
        ]

        promedio = sum(notas) / len(notas)
        label_promedio.value = f"{promedio:.2f}"

        # Asignar color según el promedio
        if promedio >= 80:
            color_fila = ft.Colors.GREEN_200
        elif 60 <= promedio < 80:
            color_fila = ft.Colors.ORANGE_200
        else:
            color_fila = ft.Colors.RED_200

        nueva_fila = ft.DataRow(
            cells=[
                ft.DataCell(ft.Text(alumno)),
                ft.DataCell(ft.Text(esp.value or "")),
                ft.DataCell(ft.Text(mat.value or "")),
                ft.DataCell(ft.Text(ing.value or "")),
                ft.DataCell(ft.Text(info.value or "")),
                ft.DataCell(ft.Text(hist.value or "")),
                ft.DataCell(ft.Text(bio.value or "")),
                ft.DataCell(ft.Text(art.value or "")),
                ft.DataCell(ft.Text(f"{promedio:.2f}")),
            ],
            color=color_fila  # 👈 Color de fondo según el promedio
        )

        tabla_calificaciones.rows.append(nueva_fila)
        page.update()

    def eliminar_ultimo_promedio(e):
        if tabla_calificaciones.rows:
            tabla_calificaciones.rows.pop()
            page.update()

    def eliminar_todos_los_promedios(e):
        if tabla_calificaciones.rows:
            tabla_calificaciones.rows.clear()
            page.update()

    def exportar_csv(e):
        if not tabla_calificaciones.rows:
            page.snack_bar = ft.SnackBar(ft.Text("No hay datos para exportar."), bgcolor="red")
            page.snack_bar.open = True
            page.update()
            return

        encabezados = [
            "Alumno", "Español", "Matemáticas", "Inglés",
            "Informática", "Historia", "Biología", "Artes", "Promedio"
        ]

        with open("calificaciones.csv", mode="w", newline="", encoding="utf-8") as archivo:
            escritor = csv.writer(archivo)
            escritor.writerow(encabezados)

            for fila in tabla_calificaciones.rows:
                datos = [celda.content.value for celda in fila.cells]
                escritor.writerow(datos)

        page.snack_bar = ft.SnackBar(ft.Text("✅ Datos exportados a 'calificaciones.csv'."), bgcolor="green")
        page.snack_bar.open = True
        page.update()

    # ---- BOTONES ----
    boton_calcular = ft.ElevatedButton(
        text="Calcular Promedio", on_click=calcular_promedio
    )

    boton_eliminar_ultimo = ft.ElevatedButton(
        text="Borrar Último Promedio", on_click=eliminar_ultimo_promedio
    )

    boton_eliminar_todos = ft.ElevatedButton(
        text="Eliminar Todos los Promedios", on_click=eliminar_todos_los_promedios
    )

    boton_exportar = ft.ElevatedButton(
        text="Exportar a CSV", on_click=exportar_csv,
    )

    fila_dropdowns = ft.Row(
        [
            lista_alumnos,
            esp,
            mat,
            ing,
            info,
            hist,
            bio,
            art,
            label_promedio
        ],
        alignment=ft.MainAxisAlignment.SPACE_AROUND
    )

    fila_boton = ft.Row(
        [boton_calcular, boton_eliminar_ultimo, boton_eliminar_todos, boton_exportar],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=20
    )

    page.add(
        ft.Column(
            [
                fila_dropdowns,
                fila_boton,
                tabla_calificaciones
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20
        )
    )

ft.app(target=main, view=ft.WEB_BROWSER)
