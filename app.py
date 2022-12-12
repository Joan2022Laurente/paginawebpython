import os
import pymysql
from flask import Flask, current_app, url_for
from flask import render_template, request, redirect, session
from flaskext.mysql import MySQL
from datetime import datetime, date 
from flask import send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.secret_key ="llaveSecreta"
mysql=MySQL()



# CONFIGURACION PARA LA BASE DE DATOS
app.config['MYSQL_DATABASE_HOST']='sql10.freemysqlhosting.net'
app.config['MYSQL_DATABASE_USER']='sql10581834'
app.config['MYSQL_DATABASE_PASSWORD']='aA47J6WH1Z'
app.config['MYSQL_DATABASE_DB']='sql10581834'
mysql.init_app(app)


# LINKS sitio usuario

@app.route('/') 
def inicio():
    try:
        conn = mysql.connect() #CONEXION A LA BASE DE DATOS
        cursor = conn.cursor(pymysql.cursors.DictCursor) #COMO UNA CABLE QUE CONECTA CON LA BASEDEDATOS
        cursor.execute("SELECT * FROM populares") #EJECUTAR Y TRAER LOS DATOS 
        rows = cursor.fetchall()
        lon = len(rows)
        return render_template('sitio/index.html', capss=rows,lon=lon)
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()

#carrito

@app.route('/carrito')
def carrito():
    return render_template('sitio/carrito.html')


#CATEGORIAS
@app.route('/CAP')
def carnesavespescado():
    try:
        print(session)
        conn = mysql.connect() #CONEXION A LA BASE DE DATOS
        cursor = conn.cursor(pymysql.cursors.DictCursor) #COMO UNA CABLE QUE CONECTA CON LA BASEDEDATOS
        cursor.execute("SELECT * FROM cap") #EJECUTAR Y TRAER LOS DATOS 
        rows = cursor.fetchall() #RECORRER TODOS LOS DATOS Y LOS DEVUELVE->[{{prod1:values},{prod2:values}...}}]
        lon = len(rows)
        return render_template('sitio/CAP.html', capss=rows, lon=lon)
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()


@app.route('/frescos')
def frescos():
    try:
        conn = mysql.connect() #CONEXION A LA BASE DE DATOS
        cursor = conn.cursor(pymysql.cursors.DictCursor) #COMO UNA CABLE QUE CONECTA CON LA BASEDEDATOS
        cursor.execute("SELECT * FROM frescos") #EJECUTAR Y TRAER LOS DATOS 
        rows = cursor.fetchall()
        lon = len(rows)
        return render_template('sitio/frescos.html', capss=rows,lon=lon)
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()

@app.route('/congelados')
def congelados():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM congelados")
        rows = cursor.fetchall()
        lon = len(rows)
        return render_template('sitio/congelados.html', capss=rows,lon=lon)
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()






#sessiones
@app.route('/iniciarsesion')
def iniciarsesion():
    return render_template('sitio/iniciarsesion.html')



# LINKS SITIO DE ADMINISTRADORRR

@app.route('/admin/login')
def adminLogin():
    return render_template('admin/login.html')



@app.route('/admin/login', methods=['POST'])
def adminLoginPost():
    _usuario=request.form['txtUsuario']
    _password=request.form['txtPassword']
        
    if _usuario=="admin" and _password=="123":
        session["login"]=True
        session["usuario"]="administrador"
        return redirect('/admin')

    return render_template('admin/login.html')


@app.route('/admin/')
def admin():
    print("sesiones al entrar al admin")
    print(session)
    if not "login" in session:
        return redirect("/admin/login")
    return render_template('admin/index.html')


#CATEGORIAS
@app.route('/admin/CAP')
def adminCAP():
    if not "login" in session:
        return redirect("/admin/login")

    conexion = mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("SELECT * FROM `cap`")
    cap = cursor.fetchall()
    conexion.commit()
    return render_template('admin/CAP.html', caps=cap)



@app.route('/admin/CAP/guardar', methods=['POST'])
def adminCAPGuardar():

    if not "login" in session:
        return redirect("/admin/login")


    _nombre=request.form['txtNombre']
    _fabricante=request.form['txtFabricante']
    _codigo=request.form['txtCodigo']
    _imagen=request.form['txtImagen']
    _precio=request.form['txtPrecio']
    # tiempo= datetime.now()
    # horaActual=tiempo.strftime('%Y%H%M%S')

    # if _imagen.filename!="":
    #     nuevoNombre=horaActual+"_"+_imagen.filename
    #     _imagen.save("templates/sitio/img/"+nuevoNombre)


    sql="INSERT INTO `cap` (`id`, `nombre`,`fabricante`,`codigo`, `imagen`, `precio`) VALUES (NULL, %s,%s, %s, %s, %s);"
    datos=(_nombre, _fabricante ,_codigo ,_imagen, _precio)
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql,datos)
    conexion.commit()
    print(session)
    return redirect('/admin/CAP')



@app.route('/img/<imagen>')
def imagenes(imagen):
    print(imagen)
    return send_from_directory(os.path.join('templates/sitio/img'),imagen)



@app.route('/admin/CAP/borrar', methods=['POST'])
def adminCAPborrar():
    _id=request.form['txtID']

    conexion = mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("SELECT imagen FROM `cap` WHERE id = %s",(_id))
    caps = cursor.fetchall()
    conexion.commit()

    if os.path.exists("templates/sitio/img/"+str(caps[0][0])):
        os.unlink("templates/sitio/img/"+str(caps[0][0]))

    conexion = mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("DELETE FROM cap WHERE id = %s",(_id))
    conexion.commit()


    return redirect('/admin/CAP')



#FRESCOSSSSS

@app.route('/admin/frescos')
def adminFrescos():
    if not "login" in session:
        return redirect("/admin/login")

    conexion = mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("SELECT * FROM `frescos`")
    cap = cursor.fetchall()
    conexion.commit()
    return render_template('admin/frescos.html', caps=cap)


@app.route('/admin/frescos/guardar', methods=['POST'])
def adminFrescosGuardar():

    if not "login" in session:
        return redirect("/admin/login")

    _nombre=request.form['txtNombre']
    _fabricante=request.form['txtFabricante']
    _codigo=request.form['txtCodigo']
    _imagen=request.form['txtImagen']
    _precio=request.form['txtPrecio']
    sql="INSERT INTO `frescos` (`id`, `nombre`,`fabricante`,`codigo`, `imagen`, `precio`) VALUES (NULL, %s,%s, %s, %s, %s);"
    datos=(_nombre, _fabricante ,_codigo ,_imagen, _precio)
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql,datos)
    conexion.commit()
    print(session)
    return redirect('/admin/frescos')


@app.route('/admin/frescos/borrar', methods=['POST'])
def adminFrescosBorrar():
    _id=request.form['txtID']

    conexion = mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("SELECT imagen FROM `frescos` WHERE id = %s",(_id))
    caps = cursor.fetchall()
    conexion.commit()

    if os.path.exists("templates/sitio/img/"+str(caps[0][0])):
        os.unlink("templates/sitio/img/"+str(caps[0][0]))

    conexion = mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("DELETE FROM frescos WHERE id = %s",(_id))
    conexion.commit()

    return redirect('/admin/frescos')




#CONGELADOSSS
@app.route('/admin/congelados')
def adminCongelados():
    if not "login" in session:
        return redirect("/admin/login")
    conexion = mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("SELECT * FROM `congelados`")
    cap = cursor.fetchall()
    conexion.commit()
    return render_template('admin/congelados.html', caps=cap)


@app.route('/admin/congelados/guardar', methods=['POST'])
def adminCongeladosGuardar():

    if not "login" in session:
        return redirect("/admin/login")

    _nombre=request.form['txtNombre']
    _fabricante=request.form['txtFabricante']
    _codigo=request.form['txtCodigo']
    _imagen=request.form['txtImagen']
    _precio=request.form['txtPrecio']
    sql="INSERT INTO `congelados` (`id`, `nombre`,`fabricante`,`codigo`, `imagen`, `precio`) VALUES (NULL, %s,%s, %s, %s, %s);"
    datos=(_nombre, _fabricante ,_codigo ,_imagen, _precio)
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql,datos)
    conexion.commit()
    print(session)
    return redirect('/admin/congelados')


@app.route('/admin/congelados/borrar', methods=['POST'])
def adminCongeladosBorrar():
    _id=request.form['txtID']

    conexion = mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("SELECT imagen FROM `congelados` WHERE id = %s",(_id))
    caps = cursor.fetchall()
    conexion.commit()

    if os.path.exists("templates/sitio/img/"+str(caps[0][0])):
        os.unlink("templates/sitio/img/"+str(caps[0][0]))

    conexion = mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("DELETE FROM congelados WHERE id = %s",(_id))
    conexion.commit()

    return redirect('/admin/congelados')





#POPULAREEEES
@app.route('/admin/populares')
def adminPopulares():
    if not "login" in session:
        return redirect("/admin/login")
    conexion = mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("SELECT * FROM `populares`")
    cap = cursor.fetchall()
    conexion.commit()
    return render_template('admin/populares.html', caps=cap)


@app.route('/admin/populares/guardar', methods=['POST'])
def adminPopularesGuardar():

    if not "login" in session:
        return redirect("/admin/login")

    _nombre=request.form['txtNombre']
    _fabricante=request.form['txtFabricante']
    _codigo=request.form['txtCodigo']
    _imagen=request.form['txtImagen']
    _precio=request.form['txtPrecio']
    sql="INSERT INTO `populares` (`id`, `nombre`,`fabricante`,`codigo`, `imagen`, `precio`) VALUES (NULL, %s,%s, %s, %s, %s);"
    datos=(_nombre, _fabricante ,_codigo ,_imagen, _precio)
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql,datos)
    conexion.commit()
    print(session)
    return redirect('/admin/populares')


@app.route('/admin/populares/borrar', methods=['POST'])
def adminPopularesBorrar():
    _id=request.form['txtID']

    conexion = mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("SELECT imagen FROM `populares` WHERE id = %s",(_id))
    caps = cursor.fetchall()
    conexion.commit()

    if os.path.exists("templates/sitio/img/"+str(caps[0][0])):
        os.unlink("templates/sitio/img/"+str(caps[0][0]))

    conexion = mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("DELETE FROM populares WHERE id = %s",(_id))
    conexion.commit()

    return redirect('/admin/populares')



@app.route('/admin/cerrar')
def adminCerrar():
    session.clear()
    return redirect('/admin/login')



















#CARRITO DE COMPRAS
@app.route('/CAP/add', methods=['POST'])
def añadirAlCarro():
    cursor = None
    try:
        cantidad = int(request.form['cantidad'])
        codigo = request.form['txtCodigo']
        # validate the received values
        if cantidad and codigo and request.method == 'POST':
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute("SELECT * FROM cap WHERE codigo=%s", codigo)
    
            row = cursor.fetchone()


            itemArray = { row['codigo'] : 
            {'nombre' : row['nombre'], 
            'codigo' : row['codigo'], 
            'cantidad' : cantidad, 
            'precio' : row['precio'], 
            'imagen' : row['imagen'], 
            'precioTotal': cantidad * row['precio']}} #se agrega una nueva key y valor en el dict


            todoPrecioTotal = 0
            todoCantidadTotal = 0

            session.modified = True

            if 'sesion_carro' in session:
                if row['codigo'] in session['sesion_carro']:
                    for key, value in session['sesion_carro'].items():
                        if row['codigo'] == key:
                            vieja_cantidad = session['sesion_carro'][key]['cantidad']
                            cantidad_total = vieja_cantidad + cantidad
                            session['sesion_carro'][key]['cantidad'] = cantidad_total
                            session['sesion_carro'][key]['precioTotal'] = cantidad_total * row['precio']
                else:
                    session['sesion_carro'] = array_merge(session['sesion_carro'], itemArray)

                for key, value in session['sesion_carro'].items():

                    cantidadIndividual = int(session['sesion_carro'][key]['cantidad'])
                    precioIndividual = float(session['sesion_carro'][key]['precioTotal'])

                    todoCantidadTotal = todoCantidadTotal + cantidadIndividual
                    todoPrecioTotal = todoPrecioTotal + precioIndividual
            else:
                session['sesion_carro'] = itemArray
                todoCantidadTotal = todoCantidadTotal + cantidad
                todoPrecioTotal = todoPrecioTotal + cantidad * row['precio']
            
            session['todoCantidadTotal'] =todoCantidadTotal #se inserta una nueva key value al dict
            session['todoPrecioTotal'] = f"{(todoPrecioTotal):.2f}"
            # return redirect(url_for(request.referrer))
            return redirect(request.referrer)
        else:			
            return 'Error while adding item to cart'
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()


#CARRITO DE COMPRAS FRESCOSSSSS
@app.route('/frescos/add', methods=['POST'])
def añadirAlCarroFrescos():
    cursor = None
    try:
        cantidad = int(request.form['cantidad'])
        codigo = request.form['txtCodigo']
        # validate the received values
        if cantidad and codigo and request.method == 'POST':
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute("SELECT * FROM frescos WHERE codigo=%s", codigo)
    
            row = cursor.fetchone()


            itemArray = { row['codigo'] : 
            {'nombre' : row['nombre'], 
            'codigo' : row['codigo'], 
            'cantidad' : cantidad, 
            'precio' : row['precio'], 
            'imagen' : row['imagen'], 
            'precioTotal': cantidad * row['precio']}} #se agrega una nueva key y valor en el dict


            todoPrecioTotal = 0
            todoCantidadTotal = 0

            session.modified = True

            if 'sesion_carro' in session:
                if row['codigo'] in session['sesion_carro']:
                    for key, value in session['sesion_carro'].items():
                        if row['codigo'] == key:
                            vieja_cantidad = session['sesion_carro'][key]['cantidad']
                            cantidad_total = vieja_cantidad + cantidad
                            session['sesion_carro'][key]['cantidad'] = cantidad_total
                            session['sesion_carro'][key]['precioTotal'] = cantidad_total * row['precio']
                else:
                    session['sesion_carro'] = array_merge(session['sesion_carro'], itemArray)

                for key, value in session['sesion_carro'].items():

                    cantidadIndividual = int(session['sesion_carro'][key]['cantidad'])
                    precioIndividual = float(session['sesion_carro'][key]['precioTotal'])

                    todoCantidadTotal = todoCantidadTotal + cantidadIndividual
                    todoPrecioTotal = todoPrecioTotal + precioIndividual
            else:
                session['sesion_carro'] = itemArray
                todoCantidadTotal = todoCantidadTotal + cantidad
                todoPrecioTotal = todoPrecioTotal + cantidad * row['precio']
            
            session['todoCantidadTotal'] =todoCantidadTotal #se inserta una nueva key value al dict
            session['todoPrecioTotal'] = f"{(todoPrecioTotal):.2f}"
            # return redirect(url_for(request.referrer))
            return redirect(request.referrer)
        else:			
            return 'Error while adding item to cart'
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()


#CARRITO DE COMPRAS FRESCOSSSSS
@app.route('/congelados/add', methods=['POST'])
def añadirAlCarroCongelados():
    cursor = None
    try:
        cantidad = int(request.form['cantidad'])
        codigo = request.form['txtCodigo']
        # validate the received values
        if cantidad and codigo and request.method == 'POST':
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute("SELECT * FROM congelados WHERE codigo=%s", codigo)
    
            row = cursor.fetchone()


            itemArray = { row['codigo'] : 
            {'nombre' : row['nombre'], 
            'codigo' : row['codigo'], 
            'cantidad' : cantidad, 
            'precio' : row['precio'], 
            'imagen' : row['imagen'], 
            'precioTotal': cantidad * row['precio']}} #se agrega una nueva key y valor en el dict


            todoPrecioTotal = 0
            todoCantidadTotal = 0

            session.modified = True

            if 'sesion_carro' in session:
                if row['codigo'] in session['sesion_carro']:
                    for key, value in session['sesion_carro'].items():
                        if row['codigo'] == key:
                            vieja_cantidad = session['sesion_carro'][key]['cantidad']
                            cantidad_total = vieja_cantidad + cantidad
                            session['sesion_carro'][key]['cantidad'] = cantidad_total
                            session['sesion_carro'][key]['precioTotal'] = cantidad_total * row['precio']
                else:
                    session['sesion_carro'] = array_merge(session['sesion_carro'], itemArray)

                for key, value in session['sesion_carro'].items():

                    cantidadIndividual = int(session['sesion_carro'][key]['cantidad'])
                    precioIndividual = float(session['sesion_carro'][key]['precioTotal'])

                    todoCantidadTotal = todoCantidadTotal + cantidadIndividual
                    todoPrecioTotal = todoPrecioTotal + precioIndividual
            else:
                session['sesion_carro'] = itemArray
                todoCantidadTotal = todoCantidadTotal + cantidad
                todoPrecioTotal = todoPrecioTotal + cantidad * row['precio']
            
            session['todoCantidadTotal'] =todoCantidadTotal #se inserta una nueva key value al dict
            session['todoPrecioTotal'] = f"{(todoPrecioTotal):.2f}"
            # return redirect(url_for(request.referrer))
            return redirect(request.referrer)
        else:			
            return 'Error while adding item to cart'
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()




#CARRITO DE COMPRAS populares
@app.route('/populares/add', methods=['POST'])
def añadirAlCarroPopulares():
    cursor = None
    try:
        cantidad = int(request.form['cantidad'])
        codigo = request.form['txtCodigo']
        # validate the received values
        if cantidad and codigo and request.method == 'POST':
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute("SELECT * FROM populares WHERE codigo=%s", codigo)
    
            row = cursor.fetchone()


            itemArray = { row['codigo'] : 
            {'nombre' : row['nombre'], 
            'codigo' : row['codigo'], 
            'cantidad' : cantidad, 
            'precio' : row['precio'], 
            'imagen' : row['imagen'], 
            'precioTotal': cantidad * row['precio']}} #se agrega una nueva key y valor en el dict


            todoPrecioTotal = 0
            todoCantidadTotal = 0

            session.modified = True

            if 'sesion_carro' in session:
                if row['codigo'] in session['sesion_carro']:
                    for key, value in session['sesion_carro'].items():
                        if row['codigo'] == key:
                            vieja_cantidad = session['sesion_carro'][key]['cantidad']
                            cantidad_total = vieja_cantidad + cantidad
                            session['sesion_carro'][key]['cantidad'] = cantidad_total
                            session['sesion_carro'][key]['precioTotal'] = cantidad_total * row['precio']
                else:
                    session['sesion_carro'] = array_merge(session['sesion_carro'], itemArray)

                for key, value in session['sesion_carro'].items():

                    cantidadIndividual = int(session['sesion_carro'][key]['cantidad'])
                    precioIndividual = float(session['sesion_carro'][key]['precioTotal'])

                    todoCantidadTotal = todoCantidadTotal + cantidadIndividual
                    todoPrecioTotal = todoPrecioTotal + precioIndividual
            else:
                session['sesion_carro'] = itemArray
                todoCantidadTotal = todoCantidadTotal + cantidad
                todoPrecioTotal = todoPrecioTotal + cantidad * row['precio']
            
            session['todoCantidadTotal'] =todoCantidadTotal #se inserta una nueva key value al dict
            session['todoPrecioTotal'] = f"{(todoPrecioTotal):.2f}"
            # return redirect(url_for(request.referrer))
            return redirect(request.referrer)
        else:			
            return 'Error while adding item to cart'
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()














#BORRAR
@app.route('/delete/<string:borrarr>')
def delete_product(borrarr):
    try:
        todoPrecioTotal = 0
        todoCantidadTotal = 0
        session.modified = True
        
        for item in session['sesion_carro'].items():
            if item[0] == borrarr:				
                session['sesion_carro'].pop(item[0], None)
                if 'sesion_carro' in session:
                    for key, value in session['sesion_carro'].items():
                        cantidadIndividual = int(session['sesion_carro'][key]['cantidad'])
                        precioIndividual = float(session['sesion_carro'][key]['precioTotal'])
                        todoCantidadTotal = todoCantidadTotal + cantidadIndividual
                        todoPrecioTotal = todoPrecioTotal + precioIndividual
                break
        
        if todoCantidadTotal == 0:
            session.clear()
        else:
            session['todoCantidadTotal'] = todoCantidadTotal
            session['todoPrecioTotal'] = todoPrecioTotal
        
        #return redirect('/')
        return redirect(request.referrer)
    except Exception as e:
        print(e)












#VACIAR
@app.route('/empty')
def empty_cart():
    try:
        session.clear()
        return redirect(request.referrer)
    except Exception as e:
        print(e)


        
        
#UN DEF QUE UNE UN ARRAY CON OTRO
def array_merge( first_array , second_array ):
    if isinstance( first_array , list ) and isinstance( second_array , list ):
        return first_array + second_array
    elif isinstance( first_array , dict ) and isinstance( second_array , dict ):
        return dict( list( first_array.items() ) + list( second_array.items() ) )
    elif isinstance( first_array , set ) and isinstance( second_array , set ):
        return first_array.union( second_array )
    return False		





if __name__ == '__main__':
    app.run()
