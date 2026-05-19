import sqlite3
from datetime import datetime
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty
from kivymd.uix.card import MDCard
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout

KV = '''
ScreenManager:
    MenuScreen:
    ExamenScreen:
    DiagnosticoScreen:

<MenuScreen>:
    name: 'menu'
    MDFloatLayout:
        md_bg_color: 0.1, 0.11, 0.15, 1
        MDLabel:
            text: "🔍 AUTOEXAMEN"
            halign: "center"
            font_style: "H4"
            theme_text_color: "Custom"
            text_color: 1, 1, 1, 1
            pos_hint: {"center_y": 0.65}
            bold: True
        MDLabel:
            text: "Guarda tu corazón, porque de él mana la vida.\\nProverbios 4:23"
            halign: "center"
            font_style: "Subtitle1"
            theme_text_color: "Custom"
            text_color: 0.7, 0.7, 0.7, 1
            pos_hint: {"center_y": 0.53}
        MDRaisedButton:
            text: "INICIAR EXAMEN DIARIO"
            size_hint: 0.7, 0.08
            pos_hint: {"center_x": 0.5, "center_y": 0.35}
            md_bg_color: 0.26, 0.50, 0.93, 1
            on_release: 
                app.iniciar_examen()
                root.manager.current = 'examen'

<ExamenScreen>:
    name: 'examen'
    MDFloatLayout:
        md_bg_color: 0.1, 0.11, 0.15, 1
        MDTopAppBar:
            title: root.modulo_titulo
            anchor_title: "center"
            pos_hint: {"top": 1}
            md_bg_color: 0.15, 0.16, 0.21, 1
            elevation: 4
            left_action_items: [["arrow-left", lambda x: app.volver_menu()]]
        ScrollView:
            size_hint_y: 0.73
            pos_hint: {"top": 0.88}
            bar_width: 4
            MDBoxLayout:
                id: container_preguntas
                orientation: 'vertical'
                adaptive_height: True
                padding: dp(20)
                spacing: dp(20)
        MDRaisedButton:
            id: btn_siguiente
            text: "SIGUIENTE MÓDULO"
            size_hint: 0.9, 0.07
            pos_hint: {"center_x": 0.5, "center_y": 0.06}
            md_bg_color: 0.26, 0.50, 0.93, 1
            on_release: app.siguiente_modulo()

<DiagnosticoScreen>:
    name: 'diagnostico'
    MDFloatLayout:
        md_bg_color: 0.1, 0.11, 0.15, 1
        MDTopAppBar:
            title: "🚨 PUNTOS CIEGOS DETECTADOS"
            anchor_title: "center"
            pos_hint: {"top": 1}
            md_bg_color: 0.75, 0.22, 0.17, 1
            elevation: 4
        ScrollView:
            size_hint_y: 0.65
            pos_hint: {"top": 0.88}
            bar_width: 4
            MDBoxLayout:
                id: container_diagnostico
                orientation: 'vertical'
                adaptive_height: True
                padding: dp(20)
                spacing: dp(15)
        MDCard:
            size_hint: 0.9, 0.12
            pos_hint: {"center_x": 0.5, "center_y": 0.17}
            padding: dp(10)
            md_bg_color: 0.15, 0.16, 0.21, 1
            radius: [10,]
            MDBoxLayout:
                orientation: 'vertical'
                MDLabel:
                    text: "📖 REFLEXIÓN DE CIERRE:"
                    font_style: "Caption"
                    theme_text_color: "Custom"
                    text_color: 0.26, 0.50, 0.93, 1
                    bold: True
                MDLabel:
                    text: "Presenta estas áreas en oración. La fuerza de voluntad humana no basta; pide renovación y define una acción correctiva para mañana."
                    font_style: "Body2"
                    theme_text_color: "Custom"
                    text_color: 0.9, 0.9, 0.9, 1
                    halign: "justify"
        MDRaisedButton:
            text: "FINALIZAR Y GUARDAR"
            size_hint: 0.9, 0.07
            pos_hint: {"center_x": 0.5, "center_y": 0.06}
            md_bg_color: 0.26, 0.50, 0.93, 1
            on_release: app.finalizar_examen()
'''

class MenuScreen(Screen):
    pass

class ExamenScreen(Screen):
    modulo_titulo = StringProperty("")

class DiagnosticoScreen(Screen):
    pass

class PreguntaCard(MDCard):
    def __init__(self, id_pregunta, texto_pregunta, callback_check, **kwargs):
        super().__init__(**kwargs)
        self.id_pregunta = id_pregunta
        self.orientation = "horizontal"
        self.size_hint_y = None
        self.height = "120dp"
        self.padding = "15dp"
        self.spacing = "10dp"
        self.radius = [12,]
        self.md_bg_color = [0.15, 0.16, 0.21, 1]
        self.elevation = 2
        
        self.label = MDLabel(
            text=texto_pregunta,
            theme_text_color="Custom",
            text_color=[0.9, 0.9, 0.9, 1],
            font_style="Body1",
            halign="left"
        )
        
        box_check = MDBoxLayout(orientation="vertical", size_hint=(None, 1), width="48dp")
        self.checkbox = MDCheckbox(
            size_hint=(None, None),
            size=("48dp", "48dp"),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            selected_color=[0.75, 0.22, 0.17, 1],
            unselected_color=[0.6, 0.6, 0.6, 1]
        )
        self.checkbox.bind(active=lambda checkbox, value: callback_check(self.id_pregunta, value))
        box_check.add_widget(self.checkbox)
        
        self.add_widget(self.label)
        self.add_widget(box_check)

class AutoexamenApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"
        self.init_database()
        
        self.banco_preguntas = {
            1: {
                "titulo": "M1: DIOS Y SOBERANÍA",
                "items": [
                    (1, "¿Atribuí mis éxitos del día a mis propias capacidades omitiendo dar gracias a Dios?"),
                    (2, "¿Puse mi seguridad mental en cosas temporales (dinero, planes, aprobación) antes que en Dios?"),
                    (3, "¿Actué como si Dios no existiera en mis decisiones, sin orar ni buscar dirección divina?"),
                    (4, "¿Permití que la queja dominara mis pensamientos sobre las bendiciones que me rodean?"),
                    (5, "¿Traté las bendiciones diariamente como obligaciones y no con gratitud?"),
                    (6, "¿Exigí a Dios que las cosas se hicieran bajo mis propios términos y mis tiempos?"),
                    (7, "¿Realicé disciplinas espirituales por mera rutina con la mente completamente dispersa?"),
                    (8, "¿Busqué una relación de conveniencia con lo divino solo para pedir resolver problemas?")
                ]
            },
            2: {
                "titulo": "M2: TRATO CON EL PRÓJIMO",
                "items": [
                    (9, "¿Fui hipócrita al adular a alguien por fuera mientras por dentro sentía desprecio?"),
                    (10, "¿Hice favores o buenas acciones esperando reconocimiento o un favor de vuelta?"),
                    (11, "¿Exageré o alteré historias para proyectar una imagen más exitosa o inteligente de mí?"),
                    (12, "¿Retuve ofensas del día alimentando el resentimiento en lugar de decidir perdonar?"),
                    (13, "¿Practiqué hostilidad pasiva (ley del hielo, sarcasmo) con quien me ofendió?"),
                    (14, "¿Deseé secretamente que le fuera mal o que fuera expuesta una persona que me hirió?"),
                    (15, "¿Hablé de los defectos o vida privada de alguien que no estaba presente para defenderse?"),
                    (16, "¿Disfrazé el chisme/murmuración como preocupación legítima o 'motivo de oración'?"),
                    (17, "¿Fui áspero, hiriente o impaciente con empleados, subordinados, pareja o familia?"),
                    (18, "¿Sentí molestia, celos o incomodidad ante el éxito o prosperidad de otra persona?"),
                    (19, "¿Me alegré secretamente del fracaso o de una equivocación cometida por mi competencia?"),
                    (20, "¿Eclipsé el logro de alguien hablando inmediatamente de mí para recuperar la atención?")
                ]
            },
            3: {
                "titulo": "M3: PUREZA DE LA MENTE",
                "items": [
                    (21, "¿Permití que mi mente se deleitara en pensamientos impuros, lujuria o pornografía mental?"),
                    (22, "¿Maquiné discusiones o venganzas imaginarias ensayando peleas en mi cabeza?"),
                    (23, "¿Consumí contenido visual/auditivo dañino (morbo, violencia, chismes) que alteró mi paz?")
                ]
            },
            4: {
                "titulo": "M4: ESTABILIDAD ANTE UNO MISMO",
                "items": [
                    (24, "¿Abracé el desánimo o victimismo diciendo que todo me sale mal y nadie me quiere?"),
                    (25, "¿Utilicé la autocompasión para evadir mis responsabilidades y culpar a mis circunstancias?"),
                    (26, "¿Dudé del amor y la fidelidad de Dios permitiendo que la ansiedad ahogara mi fe?")
                ]
            },
            5: {
                "titulo": "M5: HONESTIDAD INTELECTUAL",
                "items": [
                    (27, "¿Justifiqué mis malas acciones excusándome en el cansancio, el tráfico o la provocación?"),
                    (28, "¿Fui estricto para juzgar fallos ajenos pero permisivo e indulgente con los míos?"),
                    (29, "¿Intenté esconder un mal comportamiento del día sin intención real de enmendarlo?")
                ]
            },
            6: {
                "titulo": "M6: USO DE LOS RECURSOS",
                "items": [
                    (30, "¿Desperdicié horas valiosas en procrastinación destructiva (redes, teléfono compulsivo)?"),
                    (31, "¿Trabajé o estudié con desgano o mediocridad sabiendo que podía dar un esfuerzo honesto?"),
                    (32, "¿Maltraté mi cuerpo mediante glotonería, sustancias dañinas o privación extrema de sueño?")
                ]
            }
        }
        
        return Builder.load_string(KV)
        
    def init_database(self):
        self.conn = sqlite3.connect('autoexamen.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS registro_puntos_ciegos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha TEXT,
                id_pregunta INTEGER
            )
        ''')
        self.conn.commit()

    def iniciar_examen(self):
        self.modulo_actual = 1
        self.respuestas = {}
        self.cargar_modulo()
        
    def cargar_modulo(self):
        screen = self.root.get_screen('examen')
        container = screen.ids.container_preguntas
        container.clear_widgets()
        
        datos_modulo = self.banco_preguntas[self.modulo_actual]
        screen.modulo_titulo = datos_modulo["titulo"]
        
        if self.modulo_actual == 6:
            screen.ids.btn_siguiente.text = "VER DIAGNÓSTICO"
        else:
            screen.ids.btn_siguiente.text = "SIGUIENTE MÓDULO"
            
        for id_preg, texto in datos_modulo["items"]:
            self.respuestas[id_preg] = False
            card = PreguntaCard(id_pregunta=id_preg, texto_pregunta=texto, callback_check=self.registrar_respuesta)
            container.add_widget(card)

    def registrar_respuesta(self, id_pregunta, completado):
        self.respuestas[id_pregunta] = completado

    def siguiente_modulo(self):
        if self.modulo_actual < 6:
            self.modulo_actual += 1
            self.cargar_modulo()
        else:
            self.generar_diagnostico()
            self.root.current = 'diagnostico'

    def generar_diagnostico(self):
        screen = self.root.get_screen('diagnostico')
        container = screen.ids.container_diagnostico
        container.clear_widgets()
        
        puntos_ciegos_detectados = False
        
        for num_mod, info in self.banco_preguntas.items():
            for id_preg, texto in info["items"]:
                if self.respuestas.get(id_preg, False):
                    puntos_ciegos_detectados = True
                    card_alerta = MDCard(
                        size_hint_y=None,
                        height="90dp",
                        padding="12dp",
                        md_bg_color=[0.24, 0.13, 0.14, 1],
                        radius=[8,],
                        line_color=[0.75, 0.22, 0.17, 1]
                    )
                    lbl = MDLabel(
                        text=f"⚠️ {texto}",
                        theme_text_color="Custom",
                        text_color=[1, 0.8, 0.8, 1],
                        font_style="Body2"
                    )
                    card_alerta.add_widget(lbl)
                    container.add_widget(card_alerta)
                    
        if not puntos_ciegos_detectados:
            lbl_limpio = MDLabel(
                text="✨ ¡Excelente examen! Hoy no se detectaron puntos ciegos activos en tu corazón. Mantente vigilante.",
                halign="center",
                theme_text_color="Custom",
                text_color=[0.4, 0.8, 0.4, 1],
                font_style="Body1"
            )
            container.add_widget(lbl_limpio)

    def finalizar_examen(self):
        fecha_hoy = datetime.now().strftime("%Y-%m-%d")
        
        for id_preg, marcado in self.respuestas.items():
            if marcado:
                self.cursor.execute(
                    "INSERT INTO registro_puntos_ciegos (fecha, id_pregunta) VALUES (?, ?)",
                    (fecha_hoy, id_preg)
                )
        self.conn.commit()
        self.root.current = 'menu'

    def volver_menu(self):
        self.root.current = 'menu'

if __name__ == '__main__':
    AutoexamenApp().run()
