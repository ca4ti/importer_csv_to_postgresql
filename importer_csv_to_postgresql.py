import FreeSimpleGUI as sg
import psycopg2
import csv

# Define o layout da interface
layout = [
    [sg.Text("Arquivo CSV:"), sg.In('/home/file_test.csv',size=(25, 1), enable_events=True, key="CSV_FILE"), sg.FileBrowse(file_types=(("CSV Files", "*.csv"),))],
    [sg.Text("Database Name:"), sg.InputText('DB', key="DB_NAME")],
    [sg.Text("Host:"), sg.InputText('localhost', key="HOST")],
    [sg.Text("Port:"), sg.InputText('5432', key="PORT")],
    [sg.Text("Username:"), sg.InputText('login',key="USER")],
    [sg.Text("Password:"), sg.InputText('pass',key="PASS", password_char="*")],
    [sg.Text("PARAMETER1:"), sg.InputText('1',key="PARAMETER1")],
    [sg.Text("DPARAMETER2:"), sg.InputText('127.0.0.1',key="DPARAMETER2")],
    [sg.Button("Importar"), sg.Button("Fechar")]
]

# Cria a janela
window = sg.Window("Importar CSV para PostgreSQL", layout, modal=True)

def install_libraries():
    import sys
    import subprocess
    requirements = ['pandas', 'psycopg2-binary', 'PySimpleGUI','FreeSimpleGUI']
    for r in requirements:
        subprocess.call([sys.executable, "-m", "pip", "install", r])
    
install_libraries()

def insert_data_to_db(data, db_name, host, port, user, password, csvfile, PARAMETER1, DPARAMETER2):
    # Conecta ao banco de dados
    conn = psycopg2.connect(database=db_name, user=user, host=host, port=port, password=password)
    cur = conn.cursor()
    # Gera e executa o comando de insert
    insert_statement2 = f"INSERT INTO public.TABLE_A (name_file) " \
                        f"VALUES ('{csvfile}') RETURNING id;"
    cur.execute(insert_statement2)

    # Atribui o ID retornado ao variável
    id = cur.fetchone()[0]

    conn.commit()

    # Gera e executa o comando de insert
    print(data)
    for row in data:
        insert_statement = f"INSERT INTO public.TABLE_B (parm1, param2, param3, param4, param5) " \
                           f"VALUES ('{list(row)[3]}', '{id}', '{",".join(list(row))}', '{PARAMETER1}','{DPARAMETER2}')"
        cur.execute(insert_statement)
   
    # Confirma a transação e fecha a conexão
    conn.commit()
    cur.close()
    conn.close()



try:
    while True:
        event, values = window.read()
        
        if event in (sg.WIN_CLOSED, "Fechar"):
            break    
        if event == "Importar":
            if not values["CSV_FILE"] or not values["DB_NAME"] or not values["USER"] or not values["PASS"]:
                sg.popup('Faltam campos obrigatórios')
            else:
                csvfile = values["CSV_FILE"]
                db_name = values["DB_NAME"]
                host = values["HOST"]
                port = values["PORT"]
                user = values["USER"]
                password = values["PASS"]
                PARAMETER1 = values["PARAMETER1"]
                DPARAMETER2 = values["DPARAMETER2"]
                
                # Lê o arquivo CSV
                with open(csvfile) as csv_file:
                    reader = csv.DictReader(csv_file)
                    data = []
                    for row in reader:
                        data.append(row.values())
                print( PARAMETER1, DPARAMETER2)
                # Insere os dados
                insert_data_to_db(data, db_name, host, port, user, password, csvfile, PARAMETER1, DPARAMETER2)
                sg.popup('Importação Concluída!')
finally:
    window.close()