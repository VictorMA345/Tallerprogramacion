import sys
import requests
import json
import cognitive_face as CF
import ast
from PIL import Image, ImageDraw, ImageFont


SUBSCRIPTION_KEY = None
SUBSCRIPTION_KEY = '2da64ff4594e4e05bfe4a77973079b9a'
BASE_URL = 'https://miscaras.cognitiveservices.azure.com/face/v1.0/'
CF.BaseUrl.set(BASE_URL)
CF.Key.set(SUBSCRIPTION_KEY)
def transformarDict(x):
    z = eval(x)
    return z
def emotions(picture):
    headers = {'Ocp-Apim-Subscription-Key': 'e70e11c9cb684f21b8b37313fd60e5bc'}
    image_path = picture
    #https://docs.microsoft.com/en-us/azure/cognitive-services/computer-vision/quickstarts/python-disk
    # Read the image into a byte array
    image_data = open(image_path, "rb").read()
    headers = {'Ocp-Apim-Subscription-Key': SUBSCRIPTION_KEY,
    'Content-Type': 'application/octet-stream'}
    params = {
        'returnFaceId': 'true',
        'returnFaceLandmarks': 'false',
        'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise',
    }
    response = requests.post(
                             BASE_URL + "detect/", headers=headers, params=params, data=image_data)
    analysis = response.json()
    return(analysis)

def recognize_person(foto,id_grupo):
    print(foto, " ", id_grupo)
    response = CF.face.detect(foto)
    face_ids = [d['faceId'] for d in response]  
    identified_faces = CF.face.identify(face_ids, id_grupo)
    personas = identified_faces[0]
    candidates_list = personas['candidates']
    candidates = candidates_list[0]
    person = candidates['personId']
    person_data = CF.person.get(id_grupo, person)
    person_name = person_data['name']
    response = CF.face.detect(foto)
    dic = response[0]
    faceRectangle = dic['faceRectangle']
    width = faceRectangle['width']
    top = faceRectangle['top']
    height = faceRectangle['height']
    left = faceRectangle['left']
    image=Image.open(foto)
    draw = ImageDraw.Draw(image)
    draw.rectangle((left,top,left + width,top+height), outline='red')
    font = ImageFont.truetype('C:public_semana-9_Arial_Unicode.ttf', 50)
    draw.text((50, 50), person_name, font=font,  fill="white")
    image.show()
def print_people(group_id):
    #Imprimir la lista de personas del grupo
    print(CF.person.lists(group_id))


def creargrupo(id_grupo,group_name):
    CF.person_group.create(id_grupo,group_name)
    print("El grupo ha sido creado exitosamente")
def crearpersona(nombre,profesion,foto,id_grupo):
    f = {'profesion': profesion}
    a = emotions(foto)
    z = a[0]
    f.update(z)
    respuesta = CF.person.create(id_grupo,nombre,str(f))
    id_persona = respuesta['personId']
    CF.person.add_face(foto,id_grupo,id_persona)
    CF.person_group.train(id_grupo)
    respuesta = CF.person_group.get_status(id_grupo)
    estado = respuesta['status']
    print(estado)
if __name__ == "__main__":
    flag = True
    while flag == True: 
        flag2 = True
        print("Bienvenido a Cognitive Face")
        print("Digite 1 para crear un grupo")
        print("Digite 2 para agregar una persona")
        print("Digite 3 para eliminar una persona de un grupo")
        print("Digite 4 para eliminar un grupo")
        print("Digite 5 para realizar una consulta")
        print("Digite 6 si desea salir")
        respuesta = int(input("Digite una opcion: "))
        if respuesta == 2:
            print("Digite el nombre de la persona")
            nombre =str(input())
            print("Digite la profesion de la persona")
            profesion = str(input())
            print("¿A que número grupo desea agregar a la persona?")
            id_grupo = str(input())
            print("Digite la dirección de la imagen de la persona")
            path = str(input()) 
            crearpersona(nombre,profesion,path,id_grupo)
            for x in CF.person.lists(id_grupo):
                if x['name'] == nombre:
                    personid = x['personId']
            person_data = CF.person.get(id_grupo,personid)
            CF.person_group.train(id_grupo)
            print("Persona Creada")
        if respuesta == 1:
            print("¿Comó desea llamar al grupo?")
            nombre_grupo = str(input())
            print("digite el numero del grupo")
            id_grupo = int(input())
            creargrupo(id_grupo,nombre_grupo)
            print("Grupo Creado Exitosamente")
        if respuesta == 4:
            print("Introduzca el numero del grupo que desea eliminar:")
            grupo_eliminado = int(input())
            CF.person_group.delete(grupo_eliminado)
            print("Grupo Eliminado")
        if respuesta == 3:
                print("¿En que grupo se encuentra esa persona?")
                id_grupo = int(input())
                print("¿Cual es el nombre de la persona?")
                nombre = str(input()) 
                for x in CF.person.lists(id_grupo):
                    if x['name'] == nombre:
                        personid = x['personId']
                CF.person.delete(id_grupo,personid)
                print("Persona Eliminada")
        if respuesta == 6:
            flag = False
        if respuesta == 8:
            for x in CF.person_group.lists():
                        z = x['personGroupId']
                        CF.person_group.delete(z)
        if respuesta == 5:
            historial_nombres = []
            historial_info = []
            while flag2 == True: 
                print("Elija una opcion: ")
                print("1--> Identificar personas dada una imagen (Rectangulo)")
                print("2--> Mostrar la información de todas las personas")
                print("3--> Buscar una persona")
                print("4--> Mostrar todas las personas por genero (hombre o mujer)")
                print("5--> Mostrar los atributos de su cara dada una imagen")
                print("6--> Mostrar el historial de consultas")
                print("7--> Mostrar emociones, accesorios y color de cabello dada una imagen")
                print("8--> Salir del menù de consultas")
                respuesta2 = int(input("Digite una opcion: "))
                if respuesta2 == 1:
                    group_id = int(input("Digite el numero del grupo: "))
                    path = str(input("Coloque la direccion de la imagen: "))
                    recognize_person(path, group_id)
                    print("análisis realizado correctamente")
                    print("¿desea realizar otra consulta?(y/n)")
                    respuesta2 = str(input())
                    if respuesta2 == "y":
                        flag2 = True
                    if respuesta2 == "n":
                        flag2 = False 
                if respuesta2 == 2:
                    nombres_ = []
                    for i in CF.person_group.lists():
                        g1 = i ['personGroupId']
                        for t in CF.person.lists(g1):
                            nombre_extraido = t['name']
                            nombres_.append(nombre_extraido)
                    nombres_1 = sorted(nombres_,key=str.lower)
                    print("¿Desea ver la informaciòn de forma ascendente o descendente(Digite a ascendente y d para descendente)")
                    respuesta_2 = str(input())
                    if respuesta_2 == "d":
                        for i in nombres_1:
                            for x in CF.person_group.lists():
                                z = x['personGroupId']
                                for y in CF.person.lists(z):
                                    if y['name'] == i:
                                        datos = y['userData'] 
                                        atributos = transformarDict(datos)
                                        profesion = atributos['profesion']
                                        nombre = y['name']
                                        print("nombre: ",nombre)  
                                        print("profesion: ",profesion)
                                        print("")
                                        datos = 0
                    if respuesta_2 == "a":
                        nombres_1.reverse()
                        for i in nombres_1:
                            for x in CF.person_group.lists():
                                z = x['personGroupId']
                                for y in CF.person.lists(z):
                                    if y['name'] == i:
                                        datos = y['userData'] 
                                        atributos = transformarDict(datos)
                                        profesion = atributos['profesion']
                                        nombre = y['name']
                                        print("nombre: ",nombre)  
                                        print("profesion: ",profesion)
                                        print("")
                                        datos = 0
                    print("¿desea realizar otra consulta?(y/n)")
                    respuesta2 = str(input())
                    if respuesta2 == "y":
                        flag2 = True
                    if respuesta2 == "n":
                        flag2 = False 
                if respuesta2 == 3:
                    print("digite el nombre de la persona")
                    nombre = str(input())
                    print("¿Desea buscarla en un grupo en específico?(y/n)")
                    respuesta1 =str(input())
                    if respuesta1 == "y":
                        id_grupo = int(int(input("digite el grupo en el que se encuentra la persona")))
                        for x in CF.person.lists(id_grupo):
                            if x['name'] == nombre :
                                print("Los datos de ",nombre,"son:")
                                print("los numeros de identificacion de ",nombre,"son:")
                                print("personId:",x['personId'])
                                print("persistedFaceIds:",x['persistedFaceIds'])
                    elif respuesta1 == "n":
                        for x in CF.person_group.lists():
                            id_grupo = x['personGroupId']
                            for y in CF.person.lists(id_grupo):
                                if y['name'] == nombre :
                                    print("Los datos de ",nombre,"son:")
                                    print("los numeros de identificacion de ",nombre,"son:")
                                    print("personId:",y['personId'])
                                    print("persistedFaceIds:",y['persistedFaceIds'])
                                    print("se encuentra en el grupo numero:",id_grupo)
                    else: 
                        print("error, digite una respuesta válida")
                    print("¿desea realizar otra consulta?(y/n)")
                    respuesta2 = str(input())
                    if respuesta2 == "y":
                        flag2 = True
                    if respuesta2 == "n":
                        flag2 = False 
                if respuesta2 == 4:
                    print("¿Desea buscarla en un grupo en específico?(y/n)")
                    respuesta2 =str(input())
                    if respuesta2 == "y":
                        id_grupo = int(int(input("digite el grupo en el que se encuentra la persona")))
                        for x in CF.person.lists(id_grupo):
                            datos = x['userData']
                            atributos = ast.literal_eval(datos)
                            faceAttributes = atributos['faceAttributes']
                            genero = faceAttributes['gender']
                            nombre = x['name']
                            if genero == "male":
                                genero = "masculino"
                            if genero == "female":
                                genero = "femenino"
                            print("nombre: ",nombre,"género: ",genero)
                            atributos = 0
                    if respuesta2 == "n":
                        for x in CF.person_group.lists():
                            id_grupo = x['personGroupId']
                            for y in CF.person.lists(id_grupo):
                                datos = y['userData']
                                atributos = transformarDict(datos)
                                faceAttributes = atributos['faceAttributes']
                                genero = faceAttributes['gender']
                                nombre = y['name']
                                if genero == "male":
                                    genero = "masculino"
                                if genero == "female":
                                    genero = "femenino"
                                print("nombre: ",nombre,"género: ",genero)
                                atributos = 0
                    else: 
                        print("error, digite una respuesta válida")
                    print("¿desea realizar otra consulta?(y/n)")
                    respuesta2 = str(input())
                    if respuesta2 == "y":
                        flag2 = True
                    if respuesta2 == "n":
                        flag2 = False 
                if respuesta2 == 5:
                    print("¿Como se llame esta persona?")
                    nombre = str(input())
                    historial_nombres.append(nombre)
                    nombres_consulta = sorted(historial_nombres,key= str.lower)
                    path = str(input("Coloque la direccion de la imagen: "))
                    persona = emotions(path)
                    diccionario = persona[0]
                    atributos = diccionario['faceAttributes']
                    sonrisa,bellofacial,genero,edad,maquillaje=atributos['smile']*100,atributos['facialHair'],atributos['gender'],atributos['age'],atributos['makeup']
                    bigote,barba,patillas = bellofacial['moustache']*100,bellofacial['beard']*100,bellofacial['sideburns']*100
                    maquillaje_ojo,maquillaje_labios = maquillaje['eyeMakeup'],maquillaje['lipMakeup']
                    pelo = atributos['hair']
                    calvicie = pelo['bald']*100
                    colordepelo = pelo['hairColor']
                    colordepelo = colordepelo[0]
                    color,seguridad =colordepelo['color'],colordepelo['confidence'] *100
                    print("nombre: ",nombre)
                    print("edad:",edad)
                    print("genero: ",genero)
                    print("sonrisa: ", sonrisa ,"%")
                    print("bello facial:"," patillas",patillas,"% ","bigote: ",bigote,"% "," barba: ",barba,"%")
                    print("maquillaje: ","maquillaje de ojos: ",maquillaje_ojo,", maquillaje de labios: ",maquillaje_labios)
                    print("su color de pelo es:",color,"con:",seguridad,"%"" de certeza ")
                    print("porcentaje de calvicie: ",calvicie,"%")
                    dicionario_consultas = {'nombre: ':nombre,'edad: ':edad,'genero: ':genero,'sonrisa: ':sonrisa,'patillas':patillas,'bigote: ':bigote,'barba':barba,'color de pelo: ':color,'calvicie':calvicie,"maquillaje de labios":maquillaje_labios,"maquillaje de ojos":maquillaje_ojo }
                    historial_info.append(dicionario_consultas.copy())
                    print("¿desea realizar otra consulta?(y/n)")
                    respuesta2 = str(input())
                    if respuesta2 == "y":
                        flag2 = True
                    if respuesta2 == "n":
                        flag2 = False 
                if respuesta2 == 6:
                    if len(historial_nombres)== 0:
                        print("no se ha hecho ninguna consulta")
                    else:
                        print("¿Desea ver la informaciòn de forma ascendente o descendente(Digite a ascendente y d para descendente)")
                        respuesta_6 = str(input())
                        if respuesta_6 == "d":
                            for x in historial_nombres:
                                for y in historial_info:
                                    if y['nombre: '] == x:
                                        for x,y in y.items():
                                            print(x,y)
                                        print("")
                        if respuesta_6 == "a":
                            historial_nombres.reverse()
                            for x in historial_nombres:
                                for y in historial_info:
                                    if y['nombre: '] == x:
                                        for x,y in y.items():
                                            print(x,y)
                                        print("")
                    print("¿desea realizar otra consulta?(y/n)")
                    respuesta2 = str(input())
                    if respuesta2 == "y":
                        flag2 = True
                    if respuesta2 == "n":
                        flag2 = False 
                if respuesta2 == 7:
                    path = str(input("Coloque la direccion de la imagen: "))
                    persona = emotions(path)
                    diccionario = persona[0]
                    atributos = diccionario['faceAttributes']
                    Cabello = (atributos['hair'])
                    Color = Cabello['hairColor']
                    Color1 = Color[0]
                    Color2 = Color1['color']
                    print("El color del cabello es: ",Color2)
                    Accesorios = atributos['accessories']
                    if Accesorios == []:
                        print("La foto no tiene accesorios")
                    else:
                        print("Los accesorios de la persona son: ", Accesorios)
                    emociones = atributos['emotion']
                    print("Las emociones son:")
                    for x,y in emociones.items():
                        print(x, y)
                    print("¿desea realizar otra consulta?(y/n)")
                    respuesta2 = str(input())
                    if respuesta2 == "y":
                        flag2 = True
                    if respuesta2 == "n":
                        flag2 = False 
                if respuesta2 == 8:
                    flag2= False
                else:
                    print("digite una opciòn que no existe")
            else:
                print("Digitó una opcion que no existe")