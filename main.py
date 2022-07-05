import datetime
from flask import Flask, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
import hashlib


app = Flask(__name__)
app.config.from_pyfile('config.py')

from models import db
from models import Usuario, Receta, Ingrediente


@app.route('/', methods= ['GET','POST'])
def inicio():
    if request.method == 'POST':
        if request.form['email'] and request.form['contra']:  ### Se comprueba que en el objeto encapsulado request esten dichos datos
            clave = request.form['contra']
            resultclave = hashlib.md5(bytes(clave, encoding='utf-8'))
            usuariodb = Usuario.query.filter_by(correo=request.form['email']).first()
            if usuariodb != None:
                if resultclave.hexdigest() == usuariodb.clave:
                    session['idusuario'] = usuariodb.id  ### Guarda el id en sesion
                    return render_template('panelUsuario.html',nombre=usuariodb.nombre)  ### Parametros, se pasan los datos que usara el HTML.
                else:
                    return render_template('error.html', error='La clave ingresada es incorrecta.')
            else:
                return render_template('error.html', error='El correo proporcionado no esta registrado.')
        else:
            return render_template('index.html')
    else:
        return render_template('index.html')

@app.route('/compartirReceta',methods= ['POST','GET']) ### Forma de resolverlo: Pedir el mail para de ahi sacar el usuario con la db, y la receta ya la tengo, buscarla en la db y ponerle el id a los ingredientes.
def compartirReceta():
    if request.method == 'POST':
        if request.form['nomreceta'] and request.form['tiemporeceta'] and request.form['elaboracion']:
            nuevaReceta = Receta(nombre=request.form['nomreceta'], tiempo=int(request.form['tiemporeceta']),
                                elaboracion=request.form['elaboracion'], cantidadmegusta=0,
                                fecha=datetime.date.today(), usuarioid=int(session['idusuario'])) ### Completar
            db.session.add(nuevaReceta)
            db.session.commit()
            cantingredientes = int(request.form['cantingr'])
            recetadb = Receta.query.filter_by(nombre=request.form['nomreceta']).first()
            return render_template('/agregarIngredientes.html',receta=recetadb,cant=cantingredientes) ### Buscar la id de la receta recien creada
        else:
            return render_template('/error.html',error='No ingreso los datos de la receta.')
    else:
        return render_template('compartirReceta.html',usuario=Usuario.query.filter_by(id=int(session['idusuario'])).first())

@app.route('/agregarIngredientes', methods= ['POST','GET'])
def agregarIngredientes():
    if request.method == 'POST':
        if request.form['nombreing[]'] and request.form['cant[]'] and request.form['unimedida[]'] and request.form['idreceta']:
            total = int(request.form['totingr']) ### Total de ingredientes en esta receta
            if total <= 10:
                nombreing = request.form.getlist('nombreing[]')
                canting = request.form.getlist('cant[]') ### Cantidad de cada ingrediente
                unimed = request.form.getlist('unimedida[]') ### Unidad de medida
                for i in range(total):
                    if nombreing[i] != '' and canting[i] != '' and unimed[i] != '':
                        nuevoIngrediente = Ingrediente(nombre=nombreing[i],cantidad=int(canting[i]),unidad=unimed[i],recetaid=request.form['idreceta'])
                        db.session.add(nuevoIngrediente)
                        db.session.commit()
                return render_template('panelUsuario.html')
        else:
            return render_template('/error.html',error='No ingreso los datos de los ingredientes.')
    else:
        return render_template('agregarIngredientes.html')

@app.route('/ranking')
def ranking():
    recetasdb = Receta.query.all()
    recetasdb.sort()
    return render_template('ranking.html',recetas=recetasdb)

@app.route('/ConsultaRecetasTiempo', methods= ['POST','GET'])
def ConsultaRecetasTiempo():
    if request.method == 'POST':
        tiempo = int(request.form['tiempo'])
        recetasdb = Receta.query.all()
        listaRecetas = []
        for receta in recetasdb:
            if receta.tiempo < tiempo:
                listaRecetas.append(receta)
        return render_template('muestraRecetasTiempo.html',recetas=listaRecetas,tiempo=tiempo)
    else:
        return render_template('ConsultaRecetasTiempo.html')

@app.route('/ConsultaRecetasIngrediente', methods= ['POST','GET'])
def ConsultaRecetasIngrediente():
    if request.method == 'POST':
        ingrediente = request.form['ingrediente'].lower()
        recetasdb = Receta.query.all()
        listaRecetasIngr = []
        for i in range(len(recetasdb)):
            for j in range(len(recetasdb[i].ingredientes)):
                if ingrediente in recetasdb[i].ingredientes[j].nombre.lower():
                    listaRecetasIngr.append(recetasdb[i])
        return render_template('muestraRecetasIngrediente.html',ingrediente=ingrediente,recetas=listaRecetasIngr)
    else:
        return render_template('ConsultaRecetasIngrediente.html')

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)