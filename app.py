from flask import Flask, render_template, request , redirect
import sqlite3

app = Flask(__name__)

database_path = './database.db'

@app.route('/')
@app.route('/home')
def index():
	connect = sqlite3.connect(database_path)
	cursor = connect.cursor()
	cursor.execute('SELECT * FROM ARTIGOS')
	data = cursor.fetchall()
	return render_template('index.html', data=data)


@app.route('/adicionar', methods=['GET', 'POST']) 
def adicionar(): 
	if request.method == 'POST':
		nome = request.form['nome']
		quantidade = request.form['quantidade']

		with sqlite3.connect(database_path) as compras:
			cursor = compras.cursor()
			# verificar já existe artigo com este nome (ignorar maiúsculas)
			cursor.execute('SELECT * FROM ARTIGOS WHERE LOWER(nome) = LOWER(?)', (nome,) )
			data = cursor.fetchall()			

			if data :
				# este nome já existe
				return render_template('aviso.html', msg="Artigo já existente")
			else:
				cursor.execute('INSERT INTO ARTIGOS(nome,quantidade,estado) VALUES (?,?,?)', (nome, quantidade,0))
				compras.commit()

		return redirect('/home')
	else:
		return render_template('adicionar.html')


@app.route('/confirmar')
def confirmar():
	nome = request.args.get('nome')
	with sqlite3.connect(database_path) as compras:
		cursor = compras.cursor()
		cursor.execute('UPDATE ARTIGOS SET estado = 1 WHERE nome = ?', (nome,) )
		compras.commit()

	return redirect('/home')


@app.route('/remover')
def remover():
	nome = request.args.get('nome')
	with sqlite3.connect(database_path) as compras: 
		cursor = compras.cursor() 
		cursor.execute('DELETE FROM ARTIGOS WHERE nome = ?', (nome,) )
		compras.commit() 	

	return redirect('/home')


@app.route('/alterarqtd', methods=['GET', 'POST'])
def alterarqtd():
	nome = request.args.get('nome')	
	if request.method == 'POST': 
		quantidade = request.form['quantidade']

		with sqlite3.connect(database_path) as compras: 
			cursor = compras.cursor()
			cursor.execute('UPDATE ARTIGOS SET quantidade = ? WHERE nome = ?', (quantidade, nome) )
			compras.commit()
		return redirect('/home')

	else:
		# this will not work correctly if there are several items with
		# the same name

		connect = sqlite3.connect(database_path)
		cursor = connect.cursor()
		cursor.execute('SELECT * FROM ARTIGOS WHERE nome = ?', (nome,))
		data = cursor.fetchall()
		connect.close()
		return render_template('alterarqtd.html', data=data)


if __name__ == '__main__':
	app.run(debug=False)
