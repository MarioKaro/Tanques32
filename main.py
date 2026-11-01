import flet
from flet import app
import math

def main(page: flet.Page):
    # Configuración de ventana compacta y estética para entorno móvil
    page.title = "Medidas Para Tanques De Combustible"
    page.window_width = 380
    page.window_height = 680
    page.scroll = flet.ScrollMode.AUTO
    page.padding = 15
    page.theme_mode = flet.ThemeMode.LIGHT
    page.horizontal_alignment = flet.CrossAxisAlignment.CENTER

    # --- LÓGICA DE VALIDACIÓN Y FORMATEO ---
    def auto_formatear_decimales(e):
        valor = e.control.value.strip() if e.control.value else ""
        if valor:
            try:
                valor_flotante = float(valor)
                e.control.value = f"{valor_flotante:.2f}"
            except ValueError:
                pass
        page.update()

    # --- FUNCIONES DE CONTROL DE COMPONENTES ---
    def evaluar_checkbox_dato(e):
        if radio_tiene_dato.value == "1":  # Tienes el dato de M²: Sí
            entry_metros4.disabled = False
            entry_lado1.disabled = True
            entry_lado2.disabled = True
            entry_lado1.value = ""
            entry_lado2.value = ""
        elif radio_tiene_dato.value == "2":  # Tienes el dato de M²: No
            entry_metros4.value = ""
            entry_metros4.disabled = True
            entry_lado1.disabled = False
            entry_lado2.disabled = False
        page.update()

    def evaluar_checkbox_di(e):
        if radio_tiene_di.value == "1":  # Tienes el dato de M³: Sí
            entry_metros.disabled = False
            combo_tipo.disabled = True
            combo_tipo.value = None
            deshabilitar_campos_dimensiones()
        elif radio_tiene_di.value == "2":  # Tienes el dato de M³: No
            entry_metros.value = ""
            entry_metros.disabled = True
            combo_tipo.disabled = False
            actualizacion_tipo(None)
        page.update()

    def deshabilitar_campos_dimensiones():
        entry_diametro.value = ""
        entry_altura.value = ""
        entry_ancho.value = ""
        entry_largo.value = ""
        entry_diametro.disabled = True
        entry_altura.disabled = True
        entry_ancho.disabled = True
        entry_largo.disabled = True

    def actualizacion_tipo(e):
        if radio_tiene_di.value == "1":
            return
        
        seleccion = combo_tipo.value
        deshabilitar_campos_dimensiones()
        
        if seleccion == "Cilíndrico":
            entry_diametro.disabled = False
            entry_altura.disabled = False
        elif seleccion == "Cuadrado":
            entry_altura.disabled = False
            entry_ancho.disabled = False
            entry_largo.disabled = False
        page.update()

    def limpiar_pantalla(e):
        combo_tipo.value = None
        combo_tipo.disabled = False
        radio_tiene_dato.value = None
        radio_tiene_di.value = None
        
        campos = [entry_diametro, entry_altura, entry_ancho, entry_largo, 
                  entry_metros, entry_metros4, entry_lado1, entry_lado2, 
                  entry_vr, entry_hv]
        
        for campo in campos:
            campo.value = ""
            campo.disabled = True
        page.update()

    # --- LÓGICA MATEMÁTICA PRINCIPAL ---
    def calcular_dimensiones(e):
        try:
            tipo = combo_tipo.value
            m2 = 0.0
            volumen = 0.0

            # 1. Calcular o Recibir Metros Cuadrados (Área)
            if radio_tiene_dato.value == "2":
                l1 = float(entry_lado1.value.strip() or 0)
                l2 = float(entry_lado2.value.strip() or 0)
                m2 = l1 * l2
                entry_metros4.value = f"{m2:.2f}"
            else:
                m2 = float(entry_metros4.value.strip() or 0)

            # 2. Calcular o Recibir Metros Cúbicos (Volumen)
            if radio_tiene_di.value == "1":
                volumen = float(entry_metros.value.strip() or 0)
            else:
                altura = float(entry_altura.value.strip() or 0)
                if tipo == "Cilíndrico":
                    diametro = float(entry_diametro.value.strip() or 0)
                    if diametro > 0 and altura > 0:
                        radio = diametro / 2
                        volumen = math.pi * (radio ** 2) * altura
                elif tipo == "Cuadrado":
                    ancho = float(entry_ancho.value.strip() or 0)
                    largo = float(entry_largo.value.strip() or 0)
                    if ancho > 0 and largo > 0 and altura > 0:
                        volumen = ancho * largo * altura
            
            if volumen > 0:
                entry_metros.value = f"{volumen:.2f}"

            # 3. Calcular Retención y Altura de Barda
            if volumen > 0:
                volumen_retencion = volumen * 1.1
                entry_vr.value = f"{volumen_retencion:.2f}"

                if m2 > 0:
                    altura_barda = volumen_retencion / m2
                    entry_hv.value = f"{altura_barda:.2f}"
                elif tipo == "Cilíndrico" and radio_tiene_di.value != "1":
                    diametro = float(entry_diametro.value.strip() or 0)
                    m2_circulo = math.pi * ((diametro / 2) ** 2)
                    if m2_circulo > 0:
                        altura_barda = volumen_retencion / m2_circulo
                        entry_hv.value = f"{altura_barda:.2f}"
            
            page.update()
        except ValueError:
            pass

    # --- DEFINICIÓN DE CONTROLES VISUALES ---
    combo_tipo = flet.Dropdown(
        label="Tipo de Tanque:",
        options=[flet.dropdown.Option("Cilíndrico"), flet.dropdown.Option("Cuadrado")],
        on_change=actualizacion_tipo,
    )
    
    radio_tiene_di = flet.RadioGroup(
        content=flet.Row([flet.Radio(value="1", label="Sí"), flet.Radio(value="2", label="No")]),
        on_change=evaluar_checkbox_di
    )
    
    radio_tiene_dato = flet.RadioGroup(
        content=flet.Row([flet.Row([flet.Radio(value="1", label="Sí"), flet.Radio(value="2", label="No")])]),
        on_change=evaluar_checkbox_dato
    )

    entry_diametro = flet.TextField(label="Diámetro (m):", disabled=True, keyboard_type=flet.KeyboardType.NUMBER, on_blur=auto_formatear_decimales)
    entry_altura = flet.TextField(label="Altura / Largo (m):", disabled=True, keyboard_type=flet.KeyboardType.NUMBER, on_blur=auto_formatear_decimales)
    entry_ancho = flet.TextField(label="Ancho (m):", disabled=True, keyboard_type=flet.KeyboardType.NUMBER, on_blur=auto_formatear_decimales)
    entry_largo = flet.TextField(label="Largo (m):", disabled=True, keyboard_type=flet.KeyboardType.NUMBER, on_blur=auto_formatear_decimales)
    
    entry_metros = flet.TextField(label="Volumen Tanque (m³):", disabled=True, keyboard_type=flet.KeyboardType.NUMBER, on_blur=auto_formatear_decimales)
    entry_metros4 = flet.TextField(label="Área Disponible (m²):", disabled=True, keyboard_type=flet.KeyboardType.NUMBER, on_blur=auto_formatear_decimales)
    
    entry_lado1 = flet.TextField(label="Lado #1 (m):", disabled=True, keyboard_type=flet.KeyboardType.NUMBER, on_blur=auto_formatear_decimales)
    entry_lado2 = flet.TextField(label="Lado #2 (m):", disabled=True, keyboard_type=flet.KeyboardType.NUMBER, on_blur=auto_formatear_decimales)
    
    entry_vr = flet.TextField(label="Volumen de Retención (m³):", disabled=True, read_only=True)
    entry_hv = flet.TextField(label="Altura de La Barda (m):", disabled=True, read_only=True)

    btn_calcular = flet.ElevatedButton("Calcular", bgcolor="#4CAF50", color="white", on_click=calcular_dimensiones, style=flet.ButtonStyle(shape=flet.RoundedRectangleBorder(radius=8)))
    btn_limpiar = flet.ElevatedButton("Limpiar", bgcolor="#FFC107", color="black", on_click=limpiar_pantalla, style=flet.ButtonStyle(shape=flet.RoundedRectangleBorder(radius=8)))

    # --- DISEÑO DE LA INTERFAZ DE USUARIO (UI) ---
    page.add(
        flet.Container(
            content=flet.Column([
                flet.Text("Medidas Para Tanques de Combustible", size=18, weight=flet.FontWeight.BOLD, color="#2196F3", text_align=flet.TextAlign.CENTER),
                
                # Bloque 1: Configuración de Volumen
                flet.Card(
                    content=flet.Container(
                        content=flet.Column([
                            flet.Text("1. Datos del Volumen", weight=flet.FontWeight.BOLD, size=14),
                            flet.Text("¿Tiene el dato en M³?", size=12),
                            radio_tiene_di,
                            entry_metros,
                            combo_tipo,
                            entry_diametro,
                            entry_altura,
                            entry_ancho,
                            entry_largo,
                        ], spacing=10),
                        padding=12
                    )
                ),
                
                # Bloque 2: Configuración del Área de Dique
                flet.Card(
                    content=flet.Container(
                        content=flet.Column([
                            flet.Text("2. Datos del Área Disponible", weight=flet.FontWeight.BOLD, size=14),
                            flet.Text("¿Tiene el dato en M²?", size=12),
                            radio_tiene_dato,
                            entry_metros4,
                            flet.Row([entry_lado1, entry_lado2], spacing=10),
                        ], spacing=10),
                        padding=12
                    )
                ),
                
                # Bloque 3: Resultados Requeridos
                flet.Card(
                    content=flet.Container(
                        content=flet.Column([
                            flet.Text("3. Resultados de Retención", weight=flet.FontWeight.BOLD, size=14, color="#4CAF50"),
                            entry_vr,
                            entry_hv,
                        ], spacing=10),
                        padding=12
                    )
                ),
                
                # Bloque 3: Resultados Requeridos
                flet.Card(
                    content=flet.Container(
                        content=flet.Column([
                            flet.Text("3. Resultados de Retención", weight=flet.FontWeight.BOLD, size=14, color="#4CAF50"),
                            entry_vr,
                            entry_hv,
                        ], spacing=10),
                        padding=12
                    )
                ),
                
                # Botones de Acción
                flet.Row([btn_calcular, btn_limpiar], alignment=flet.MainAxisAlignment.CENTER, spacing=15),
            ], spacing=15, horizontal_alignment=flet.CrossAxisAlignment.STRETCH),
            width=360
        )
    )

# 🍊 Se corrigió la sintaxis y se alineó por completo al ras izquierdo
if __name__ == "__main__":
    flet.app(target=main)
