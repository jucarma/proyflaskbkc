Para empezar, abriremos un terminal, en el cual procederemos a crear el entorno virtual.
Introducir:
'''
    python -m venv venv
'''
Una vez creado procedemos a activarlo:
'''
    venv\Scripts\activate (WIN)
    .venv/bin/activate (MAC)
    source/venv/bin/activate (LINUX)
'''
Instalamos requirements.txt:

'''
    pip install requeriments.txt
'''
Rellenamos config_template.py y lo renombrarmos a config.py

Damos la instruccion para seleccionar:

'''
SET FLASK_APP=run.py
'''
Y finalmente ejecutamos:
'''
flask run
'''