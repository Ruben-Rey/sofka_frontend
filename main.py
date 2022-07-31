from flask import Flask, redirect, request, render_template, url_for
import requests


app = Flask(__name__)

url = 'http://127.0.0.1:3000/naves'


@app.route('/', methods=['GET'])
def listar_naves():
    
    response = requests.get(f"{url}/lanzadera")

    if response.status_code == 200:
        naves = response.json()
        naves = naves['naves']
    
    
        return render_template('index.html', naves=naves)


@app.route('/form', methods=['GET'])
def form_naves():

    # opcion=[{'name':'lanzadera'}, {'name':'tripulada'}, {'name':'no tripulada'}]

    return render_template('form.html')


@app.route('/agregar', methods=['POST'])
def agregar_naves():
        
    nave = {
        "nombre": request.form['nombre'],
        "situacion": request.form['situacion'],
        "peso": request.form['peso'],
        "empuje": request.form['empuje'],
        "combustible": request.form['combustible'],
        "objetivo": request.form['objetivo'],
        "pais": request.form['pais'],
        "fases": request.form['fases'],
    }

    print(nave)
    response = requests.post(f"{url}/lanzadera", json=nave)
    return redirect(url_for('listar_naves'))

@app.route('/editar/<int:id>')
def editar_nave(id):
    response = requests.get(f"{url}/lanzadera/{id}")
    data = response.json()
    print(data)
    return render_template('edit.html', nave=data['naves'])

    
@app.route('/actualizar/<int:id>', methods=['POST'])
def actualizar(id):
    nave = {
        "nombre": request.form['nombre'],
        "situacion": request.form['situacion'],
        "peso": request.form['peso'],
        "empuje": request.form['empuje'],
        "combustible": request.form['combustible'],
        "objetivo": request.form['objetivo'],
        "pais": request.form['pais'],
        "fases": request.form['fases'],
    }
    
    response = requests.put(f"{url}/lanzadera/{id}", json=nave)
    return redirect(url_for('listar_naves'))


@app.route('/eliminar/<int:id>', methods=['GET'])
def eliminar_nave(id):
    response = requests.delete(f"{url}/lanzadera/{id}")
    print(response)
    return redirect(url_for('listar_naves'))

# -----------------------------------------------

@app.route('/search', methods=['POST', 'GET'])
def search():
    opcion=[{'name':'lanzadera'}, {'name':'tripulada'}, {'name':'No tripula'}]


    select = request.form.get('comp_select')

    response = requests.get(f"{url}/lanzadera")

    if response.status_code == 200:
        nave = response.json()
        nave = nave['naves']

    return render_template('search.html', nave=nave, options=opcion)
    
   
if __name__ == '__main__':
    app.run(debug=True, port=3001)


