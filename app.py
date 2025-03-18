from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
import yfinance as yf

app = Flask(__name__)

# CONEXION A LA BASE DE DATOS:
app.config['MYSQL_HOST'] = 'bj7l3xtoftrlpschwtah-mysql.services.clever-cloud.com'
app.config['MYSQL_USER'] = 'u28owjanx91fbbgg'
app.config['MYSQL_PASSWORD'] = 'Hib9YhOmKLh3xa3MMPMZ'
app.config['MYSQL_DB'] = 'bj7l3xtoftrlpschwtah'
app.config['MYSQL_PORT'] = 3306
mysql = MySQL(app)

app.secret_key = 'mysecretkey'


@app.route('/')
def index():
    fibras = ['DANHOS','FNOVA','FMTY']
    data1 = []
    caja_1 = []
    precio_fibras = []

    


    # TABLA 1:
    sql_inv = """SELECT SUM(titulos), SUM(inversion)
        FROM inversiones"""

    sql_div = """SELECT SUM(ganancia)
        FROM dividendos"""
    
    cur = mysql.connection.cursor()
    cur.execute(sql_inv)
    dt1 = cur.fetchall()

    for x in dt1:
        for y in x:
            if y == None:
                data1.append(0.00)
            else:
                data1.append(y)

    cur.execute(sql_div)
    dt2 = cur.fetchall()

    for x in dt2:
        for y in x:
            if y == None:
                data1.append(0.00)
            else:
                data1.append(y)



    # TABLA 2:
    for f in fibras:
        sql1 = f"""SELECT SUM(titulos), SUM(inversion)
        FROM inversiones
        WHERE fibra = '{f}'
        """

        cur = mysql.connection.cursor()
        cur.execute(sql1)
        tb1 = cur.fetchall()

        for x in tb1:
            for y in x:
                if y == None:
                    caja_1.append(0.00)
                else:
                    caja_1.append(y)


    for f in fibras:
        sql2 = f"""SELECT SUM(ganancia), SUM(impuesto)
        FROM dividendos
        WHERE fibra = '{f}'
        """

        cur = mysql.connection.cursor()
        cur.execute(sql2)
        tb2 = cur.fetchall()
    
        for x in tb2:
            for y in x:
                if y == None:
                    caja_1.append(0.00)
                else:
                    caja_1.append(y)
    
    porcentaje = (float(data1[2])/125.95) * 100

    return render_template('index.html',precio=porcentaje, perfil=data1, datos=caja_1)


@app.route('/registrar-inversion', methods=['GET','POST'])
def inversion():
    if request.method=='POST':
        fecha = request.form['fecha_name']
        fibra = request.form['fibra_name']
        precio = request.form['precio_name']
        titulos = request.form['titulos_name']
        total = request.form['total_name']

        datos = [fecha, fibra, precio, titulos, total]

        # INSERTAR INFORMACION EN LA BASE DE DATOS:
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO inversiones (fecha, fibra, precio_compra, titulos, inversion) VALUES (%s,%s,%s,%s,%s)",(
            fecha, fibra, precio, titulos, total
        ))
        mysql.connection.commit()

        # REDIRIGE A LA PAGINA DE CONFIRMACION
        return render_template('registro_inversion_exitoso.html', dt=datos)

    else:
        # OBTENER DATOS DE LA BD INVERSIONES:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM inversiones")
        invers = cur.fetchall()

        return render_template('registro_inversion.html', inversiones=invers)


@app.route('/registrar-dividendo', methods=['GET','POST'])
def dividendo():
    if request.method=='POST':
        fecha = request.form['fecha_name']
        fibra = request.form['fibra_name']
        titulos = request.form['titulos_name']
        dividendo = request.form['dividendo_name']
        impuesto = request.form['impuesto_name']
        ganancia = request.form['ganancia_name']

        datos = [fecha, fibra, titulos, dividendo, impuesto, ganancia]

        # INSERTAR INFORMACION EN LA BASE DE DATOS:
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO dividendos (fecha, fibra, titulos, dividendo, impuesto, ganancia) VALUES (%s,%s,%s,%s,%s,%s)",(
            fecha, fibra, titulos, dividendo, impuesto, ganancia
        ))
        mysql.connection.commit()

        # REDIRIGE A LA PAGINA DE CONFIRMACION
        return render_template('registro_dividendo_exitoso.html', dt=datos)

    else:
        # OBTENER DATOS DE LA BD DIVIDENDOS:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM dividendos")
        divid = cur.fetchall()

        return render_template('registro_dividendo.html', dividendos=divid)



@app.route('/retornar', methods=['GET','POST'])
def regresar():
    if request.method=='POST':
        retornar = request.form['ok_name']

        if retornar == "ok":
            return redirect(url_for('index'))


# DIRECCION DEL MENU PRINCIPAL:
@app.route('/direccionar_menu', methods=['GET','POST'])
def direccionar_menu():
    if request.method=='POST':
        opcion = request.form['selec_menu']

        if opcion == 'inversion':
            return redirect(url_for('inversion'))
        else:
            return redirect(url_for('dividendo'))



# *** EDITAR Y ELIMINAR ***

# ELIMINAR TABLA INVERSIONES:
@app.route('/eliminar_inversion/<string:id>')
def eliminar_inversion(id):
    
    cur = mysql.connection.cursor()
    cur.execute(f"DELETE FROM inversiones WHERE id={id}")
    mysql.connection.commit()

    return redirect(url_for('inversion'))


# ELIMINAR TABLA DIVIDENDOS:
@app.route('/eliminar_dividendo/<string:id>')
def eliminar_dividendo(id):
    
    cur = mysql.connection.cursor()
    cur.execute(f"DELETE FROM dividendos WHERE id={id}")
    mysql.connection.commit()

    return redirect(url_for('dividendo'))



# REGRESAR AL PERFIL:
@app.route('/regresar_perfil/<string:id>')
def regresar_perfil(id):
    
    if id == 'perfil':
        return redirect(url_for('index'))


if __name__=='__main__':
    app.run(debug=True)