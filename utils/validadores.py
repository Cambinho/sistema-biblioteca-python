import re

def validar_email(email):
    
    # Um padrão de regex comum para validação de e-mail
    padrao_regex = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,7}$"
    
    # re.fullmatch garante que toda a string corresponda ao padrão
    if re.fullmatch(padrao_regex, email):
        return True
    else:
        return False

def teste_campos_vazios(parametro1=1, parametro2=1, parametro3=1, parametro4=1, parametro5=1, parametro6=1):
    if parametro1 == "" or parametro2 == "" or parametro3 == "" or parametro4 == "" or parametro5 == "" or parametro6 == "":
        return False
    return True

