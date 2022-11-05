# librerias
import psycopg2
from psycopg2 import extensions
from pickle import TRUE
import pandas as pd

# funciones


def menu():
    print("[1] Crear estudiante")
    print("[2] Crear curso")
    print("[3] Asignar estudiante a curso existente")
    print("[0] Salir")
    value = int(input("Ingrese la opción del menú \n"))
    return value

try:
    # parametros de conexión
    database = input("Ingrese el nombre de la base de datos\n")
    user = input("Ingrese el nombre de usuario\n")
    password = input("Ingrese el password del usuario\n")
    conn = psycopg2.connect("dbname=%s user=%s password=%s" % (database, user, password))

    # niveles de aislamiento
    nivel_aislamiento = extensions.ISOLATION_LEVEL_SERIALIZABLE
    conn.set_isolation_level(nivel_aislamiento)

    # conexion a base de datos
    cur = conn.cursor()
    print("Usuario conectado")
    # presentacion de menu y seleccion de usuario
    select = -1

    try:

        while select != 0:
            select = menu()

            if select == 1:  # ingresar un estudiante
                id = int(input("Ingrese el id/carnet del estudiante (dato numerico)\n"))
                nombre = input("Ingrese los nombres del estudiante\n")
                apellido = input("Ingrese los apellidos del estudiante\n")
                fecha = input("Ingrese la fecha de nacimiento del estudiante MM-DD-YYYY\n")
                script = 'INSERT INTO estudiante (id_est, nombres, apellidos, fechanacimiento) VALUES (%s,%s,%s,%s)'
                try:
                    cur.execute(script, (id, nombre, apellido, fecha))
                except psycopg2.errors.InsufficientPrivilege as e:
                    print(e)
                    conn.rollback()
                    pass
                conn.commit()
                print("Estudiante ingresado al sistema")
            elif select == 2:  # nuevo curso
                id = int(input("Ingrese el id del curso (dato numerico)\n"))
                codigo = input("Ingrese el código del curso\n")
                nombre = input("Ingrese el nombre del curso\n")
                cupo_maximo = int(input("Ingrese el cupo máximo\n"))
                print("Se colocará valor de 0 al cupo actual")
                script = 'INSERT INTO curso (id, cod_curso, nombre, cupo_actual, cupo_max) VALUES (%s,%s,%s,0,%s)'
                try:
                    cur.execute(script, (id, codigo, nombre, cupo_maximo))
                except psycopg2.errors.InsufficientPrivilege as e:
                    print(e)
                    conn.rollback()
                    pass
                conn.commit()
                print("Curso ingresado al sistema")

            elif select == 3:
                # asignar estudiante a un curso
                carnet = input("Ingrese el carnet del estudiante \n")
                curso = input("Ingrese el código del curso \n")
                fecha = input("Ingrese la fecha de asignación \n")

                try:
                    cur.execute('SELECT cupo_actual, cupo_max, nombre FROM curso WHERE cod_curso = %s', (curso,))
                    fila = cur.fetchone()
                    if fila is not None:
                        cupo_actual = fila[0]
                        cupo_maximo = fila[1]
                        nombre_curso = fila[2]

                        if cupo_actual < cupo_maximo:
                            cupo_actualizado = cupo_actual + 1
                            cur.execute("SELECT id FROM curso WHERE cod_curso=%s", (curso,))
                            id_curso = cur.fetchone()[0]
                            cur.execute("UPDATE curso SET cupo_actual = %s WHERE cod_curso = %s", (cupo_actualizado, curso))
                            cur.execute("INSERT INTO asignacion(id_est, id_curso, fechaasignacion) VALUES(%s, %s, %s)", (carnet, id_curso, fecha))
                        else:
                            print("Error: Se llegó al cupo máximo del curso %s", nombre_curso)
                            conn.rollback()

                        conn.commit()
                        script = "SELECT e.nombres||' '||e.apellidos estudiante, c.cod_curso curso, a.fechaasignacion "\
                                 "FROM asignacion a INNER JOIN curso c ON c.id = a.id_curso "\
                                 "INNER JOIN estudiante e ON e.id_est = a.id_est"
                        df = pd.read_sql(script, conn)
                        print(df)
                    else:
                        print("Ese codigo no ha sido encontrado")
                except psycopg2.errors.InsufficientPrivilege as e:
                    print(e)
                    conn.rollback()
                    pass

    except psycopg2.errors.RaiseException as e:
        print("ERROR:", e)
        cur.close()
        conn.rollback()
        pass

except ValueError:
    print("Ha ingresado erróneamente un dato del menu")
except psycopg2.OperationalError as e:
    print("ERROR:", e)
