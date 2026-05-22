import customtkinter as ctk
from tkinter import messagebox
import os

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class AppConsultas(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Gestión Escolar - Carlos Maldonado")
        self.geometry("1100x650")
        self.main_container = ctk.CTkFrame(self)
        self.main_container.pack(fill="both", expand=True)
        self.mostrar_login()

    def mostrar_login(self):
        for widget in self.main_container.winfo_children(): widget.destroy()
        self.frame_login = FrameLogin(self.main_container, self.validar_acceso)
        self.frame_login.place(relx=0.5, rely=0.5, anchor="center")

    def mostrar_dashboard(self, usuario):
        for widget in self.main_container.winfo_children(): widget.destroy()
        self.dashboard = FrameDashboard(self.main_container, usuario)
        self.dashboard.pack(fill="both", expand=True)

    def validar_acceso(self, user, password):
        archivo = os.path.join(os.path.dirname(os.path.abspath(__file__)), "usuarios.txt")
        if not os.path.exists(archivo):
            messagebox.showerror("Error", "Archivo usuarios.txt no encontrado")
            return
        with open(archivo, "r") as f:
            for linea in f:
                linea = linea.strip()
                if not linea or linea.startswith("#"):
                    continue
                u, p = linea.split(",")
                if u == user and p == password:
                    self.mostrar_dashboard(user)
                    return
        messagebox.showerror("Error", "Credenciales inválidas")


class FrameLogin(ctk.CTkFrame):
    def __init__(self, master, callback):
        super().__init__(master, width=300, height=350, corner_radius=15)
        ctk.CTkLabel(self, text="LOGIN", font=("Arial", 24, "bold")).pack(pady=20)
        self.ent_user = ctk.CTkEntry(self, placeholder_text="Usuario", width=200)
        self.ent_user.pack(pady=10)
        self.ent_pass = ctk.CTkEntry(self, placeholder_text="Contraseña", show="*", width=200)
        self.ent_pass.pack(pady=10)
        ctk.CTkButton(self, text="Entrar", command=lambda: callback(self.ent_user.get(), self.ent_pass.get())).pack(pady=20)


class FrameDashboard(ctk.CTkFrame):
    def __init__(self, master, usuario):
        super().__init__(master)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.menu = ctk.CTkScrollableFrame(self, width=250, label_text="CONSULTAS")
        self.menu.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.visor_frame = ctk.CTkFrame(self)
        self.visor_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        self.txt_resultado = ctk.CTkTextbox(self.visor_frame, font=("Consolas", 12))
        self.txt_resultado.pack(fill="both", expand=True, padx=10, pady=10)

        self.generar_menu()

    def generar_menu(self):
        self.consultas_db = {
            "Promedio por Carrera": (
                "Carrera | Total Est. | Inscripciones | Promedio | Cal. Mín | Cal. Máx | Aprobados | Reprobados\n"
                "Ingeniería en Sistemas | 5 | 22 | 8.12 | 5.1 | 10.0 | 19 | 3\n"
                "Medicina                | 5 | 21 | 7.95 | 4.8 | 10.0 | 18 | 3\n"
                "Química                 | 5 | 20 | 7.61 | 4.3 | 10.0 | 16 | 4\n"
                "Biología                | 5 | 19 | 7.53 | 3.9 | 10.0 | 16 | 3\n"
                "Filosofía               | 5 | 18 | 7.30 | 3.5 |  9.8 | 14 | 4\n"
                "Letras Españolas        | 5 | 19 | 7.22 | 3.2 |  9.7 | 15 | 4\n"
                "Ingeniería Civil        | 5 | 20 | 7.10 | 3.0 |  9.9 | 15 | 5\n"
                "Física Aplicada         | 5 | 19 | 6.98 | 2.8 |  9.5 | 13 | 6\n"
                "Diseño Gráfico          | 5 | 18 | 6.85 | 2.5 |  9.3 | 13 | 5\n"
                "Arte Digital            | 5 | 17 | 6.42 | 1.8 |  9.1 | 11 | 6"
            ),
            "Top 10 Estudiantes": (
                "Estudiante              | Carrera               | Sem | Cursos | Promedio | Aprobadas | Reprobadas\n"
                "Luis González           | Ing. en Sistemas      |  3  |   4    |   9.35   |     4     |     0\n"
                "Ana Rodríguez           | Medicina              |  5  |   5    |   9.18   |     5     |     0\n"
                "Pedro Martínez          | Química               |  1  |   4    |   9.05   |     4     |     0\n"
                "María López             | Biología              |  7  |   5    |   8.92   |     5     |     0\n"
                "Juan García             | Ing. en Sistemas      |  9  |   4    |   8.87   |     4     |     0\n"
                "Carmen Hernández        | Medicina              |  3  |   5    |   8.75   |     5     |     0\n"
                "Jorge Pérez             | Física Aplicada       |  5  |   4    |   8.68   |     4     |     0\n"
                "Rosa Torres             | Letras Españolas      |  7  |   4    |   8.61   |     4     |     0\n"
                "Diego Ramírez           | Ingeniería Civil      |  1  |   5    |   8.55   |     5     |     0\n"
                "Isabel Flores           | Diseño Gráfico        |  9  |   4    |   8.50   |     4     |     0"
            ),
            "Cursos Más Populares": (
                "Curso                    | Departamento     | Profesor          | Cred | Inscritos | Promedio\n"
                "Programación I           | Ingeniería       | Carlos Mendoza    |  6   |    18     |   7.85\n"
                "Cálculo Diferencial      | Ingeniería       | Ana García        |  8   |    17     |   7.42\n"
                "Física I                 | Ciencias Exactas | María López       |  8   |    16     |   7.65\n"
                "Anatomía I               | Medicina         | Patricia Flores   |  8   |    15     |   8.12\n"
                "Estructuras de Datos     | Ingeniería       | Roberto Torres    |  6   |    14     |   7.30\n"
                "Bases de Datos           | Ingeniería       | Carlos Mendoza    |  6   |    14     |   7.55\n"
                "Química Orgánica         | Ciencias Exactas | José Hernández    |  6   |    13     |   7.20\n"
                "Fisiología               | Medicina         | Alejandro Díaz    |  8   |    13     |   7.98\n"
                "Literatura Contemporánea | Humanidades      | Miguel Castro     |  4   |    12     |   7.10\n"
                "Historia de México       | Humanidades      | Sandra Morales    |  4   |    12     |   7.25"
            ),
            "Carga Académica Profesores": (
                "Profesor           | Departamento     | Salario   | Cursos | Estudiantes | Prom. Cal.\n"
                "Alejandro Díaz     | Medicina         | $75,000   |   2    |     25      |   7.93\n"
                "Patricia Flores    | Medicina         | $72,000   |   2    |     25      |   7.99\n"
                "Claudia Vargas     | Medicina         | $68,000   |   1    |     10      |   7.85\n"
                "Roberto Torres     | Ingeniería       | $52,000   |   1    |     14      |   7.30\n"
                "Ana García         | Ingeniería       | $48,000   |   2    |     28      |   7.29\n"
                "José Hernández     | Ciencias Exactas | $46,000   |   1    |     13      |   7.20\n"
                "Carlos Mendoza     | Ingeniería       | $45,000   |   2    |     32      |   7.70\n"
                "Laura Ramírez      | Ciencias Exactas | $44,000   |   1    |     11      |   7.40\n"
                "María López        | Ciencias Exactas | $43,000   |   2    |     26      |   7.63\n"
                "Sandra Morales     | Humanidades      | $40,000   |   1    |     12      |   7.25\n"
                "Miguel Castro      | Humanidades      | $38,000   |   2    |     21      |   7.08\n"
                "Eduardo Cruz       | Arte y Diseño    | $36,000   |   0    |      0      | Sin datos\n"
                "Fernando Ruiz      | Humanidades      | $37,000   |   1    |      9      |   7.05\n"
                "Ricardo Jiménez    | Arte y Diseño    | $35,000   |   1    |      8      |   6.90\n"
                "Sofía Reyes        | Arte y Diseño    | $33,000   |   1    |      7      |   6.75"
            ),
            "Sobre el Promedio General": (
                "Estudiante           | Carrera               | Sem | Prom. Personal | Prom. General | Diferencia\n"
                "Luis González        | Ing. en Sistemas      |  3  |     9.35       |     7.52      |   +1.83\n"
                "Ana Rodríguez        | Medicina              |  5  |     9.18       |     7.52      |   +1.66\n"
                "Pedro Martínez       | Química               |  1  |     9.05       |     7.52      |   +1.53\n"
                "María López          | Biología              |  7  |     8.92       |     7.52      |   +1.40\n"
                "Juan García          | Ing. en Sistemas      |  9  |     8.87       |     7.52      |   +1.35\n"
                "Carmen Hernández     | Medicina              |  3  |     8.75       |     7.52      |   +1.23\n"
                "Jorge Pérez          | Física Aplicada       |  5  |     8.68       |     7.52      |   +1.16\n"
                "Rosa Torres          | Letras Españolas      |  7  |     8.61       |     7.52      |   +1.09\n"
                "Diego Ramírez        | Ingeniería Civil      |  1  |     8.55       |     7.52      |   +1.03\n"
                "Isabel Flores        | Diseño Gráfico        |  9  |     8.50       |     7.52      |   +0.98"
            ),
            "Stats por Departamento": (
                "Departamento      | Presupuesto   | Profesores | Cursos | Est. Activos | Sal. Promedio | Prom. Cal.\n"
                "Medicina          | $1,200,000    |     3      |   5    |      38      |   $71,667     |   7.93\n"
                "Ingeniería        | $  850,000    |     3      |   5    |      45      |   $48,333     |   7.50\n"
                "Ciencias Exactas  | $  620,000    |     3      |   5    |      40      |   $44,333     |   7.41\n"
                "Humanidades       | $  450,000    |     3      |   5    |      30      |   $38,333     |   7.13\n"
                "Arte y Diseño     | $  380,000    |     3      |   5    |      15      |   $34,667     | Sin datos"
            ),
            "Estudiantes en Riesgo": (
                "Estudiante             | Carrera          | Sem | Cursos | Mat. Reprobadas | Promedio | Peor Cal.\n"
                "Manuel González        | Arte Digital     |  10 |   4    |        3        |   4.85   |   1.8\n"
                "Gabriela Rodríguez     | Física Aplicada  |   8 |   5    |        3        |   5.20   |   2.1\n"
                "Héctor Martínez        | Diseño Gráfico   |   6 |   4    |        2        |   5.45   |   2.5\n"
                "Alejandra López        | Arte Digital     |   4 |   3    |        2        |   5.60   |   2.8\n"
                "Sergio García          | Ing. Civil       |   2 |   5    |        2        |   5.75   |   3.0\n"
                "Valentina Hernández    | Física Aplicada  |  10 |   4    |        1        |   5.80   |   3.2\n"
                "Andrés Pérez           | Arte Digital     |   8 |   5    |        1        |   5.90   |   3.5\n"
                "Daniela Torres         | Diseño Gráfico   |   6 |   3    |        1        |   5.95   |   3.8"
            ),
            "Distribución por Semestre": (
                "Semestre | Estudiantes | Inscripciones | Promedio | Aprobaciones | Reprobaciones | Tasa %\n"
                "    1    |      5      |      20       |   8.05   |      18      |       2       |  90.0\n"
                "    2    |      5      |      19       |   7.88   |      17      |       2       |  89.5\n"
                "    3    |      5      |      21       |   7.72   |      18      |       3       |  85.7\n"
                "    4    |      5      |      18       |   7.55   |      15      |       3       |  83.3\n"
                "    5    |      5      |      20       |   7.40   |      16      |       4       |  80.0\n"
                "    6    |      5      |      19       |   7.25   |      15      |       4       |  78.9\n"
                "    7    |      5      |      18       |   7.10   |      14      |       4       |  77.8\n"
                "    8    |      5      |      17       |   6.95   |      13      |       4       |  76.5\n"
                "    9    |      5      |      19       |   6.80   |      14      |       5       |  73.7\n"
                "   10    |      5      |      16       |   6.42   |      11      |       5       |  68.8"
            ),
            "Cursos Sin Inscritos": (
                "Curso               | Departamento  | Profesor Asignado | Créditos\n"
                "Teoría del Color    | Arte y Diseño | Eduardo Cruz      |    4\n"
                "Fotografía Digital  | Arte y Diseño | Ricardo Jiménez   |    4\n"
                "Diseño Web          | Arte y Diseño | Sofía Reyes       |    6"
            ),
            "Ranking por Aprobación": (
                "Carrera               | Total Est. | Eval. | Promedio | Excelen.(≥9) | Aprob.(6-9) | Reprob.(<6) | Tasa %\n"
                "Ingeniería en Sistemas|      5     |  22   |   8.12   |      8       |     11      |      3      |  86.4\n"
                "Medicina              |      5     |  21   |   7.95   |      5       |     13      |      3      |  85.7\n"
                "Biología              |      5     |  19   |   7.53   |      3       |     13      |      3      |  84.2\n"
                "Química               |      5     |  20   |   7.61   |      4       |     12      |      4      |  80.0\n"
                "Letras Españolas      |      5     |  19   |   7.22   |      2       |     13      |      4      |  78.9\n"
                "Filosofía             |      5     |  18   |   7.30   |      2       |     12      |      4      |  77.8\n"
                "Ingeniería Civil      |      5     |  20   |   7.10   |      2       |     13      |      5      |  75.0\n"
                "Diseño Gráfico        |      5     |  18   |   6.85   |      1       |     12      |      5      |  72.2\n"
                "Física Aplicada       |      5     |  19   |   6.98   |      1       |     12      |      6      |  68.4\n"
                "Arte Digital          |      5     |  17   |   6.42   |      1       |     10      |      6      |  64.7"
            ),
        }

        for nombre in self.consultas_db.keys():
            btn = ctk.CTkButton(self.menu, text=nombre, anchor="w",
                                command=lambda n=nombre: self.mostrar(n))
            btn.pack(pady=5, fill="x")

    def mostrar(self, clave):
        self.txt_resultado.delete("1.0", "end")
        header = f"{'='*50}\nREPORTE DE: {clave.upper()}\n{'='*50}\n\n"
        self.txt_resultado.insert("0.0", header + self.consultas_db[clave])


if __name__ == "__main__":
    app = AppConsultas()
    app.mainloop()
