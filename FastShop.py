from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://FrameLeo:12341848@127.0.0.1:3306/frameleo'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'usuario'
    CPF = db.Column('usu_CPF', db.String(256), primary_key=True)
    nome = db.Column('usu_nome', db.String(256))
    email = db.Column('usu_email', db.String(256))

    def __init__(self, nome, email, CPF):
        self.nome = nome
        self.email = email
        self.CPF = CPF

class Anuncio(db.Model):
    __tablename__ = 'anuncios'
    titulo = db.Column('titulo', db.String(256))
    categoria = db.Column('categoria', db.String(256))
    descricao = db.Column('descricao', db.String(256))
    id_anu = db.Column('id_anu', db.String(256), primary_key=True)
    preco = db.Column('preco', db.Float)
    quantidade = db.Column('quantidade', db.Integer)
    favorito = db.Column('favorito', db.Boolean, default=False)
    perguntas = db.Column('perguntas', db.Text)

    def __init__(self, titulo, categoria, descricao, id_anu, preco, quantidade, favorito=False, perguntas=''):
        self.titulo = titulo
        self.categoria = categoria
        self.descricao = descricao
        self.id_anu = id_anu
        self.preco = preco
        self.quantidade = quantidade
        self.favorito = favorito
        self.perguntas = perguntas

@app.route("/")
def index():
    anuncios = Anuncio.query.all()
    return render_template('index.html', anuncios=anuncios)

@app.route("/cadastros/user")
def cad_usuarios():
    usuarios = User.query.all()
    return render_template("cadastro_user.html", titulocaduser="Cadastrar Usuários", usuarios=usuarios)

@app.route("/cadastros/cad_user", methods=['POST'])
def cad_user():
    nome = request.form['user']
    email = request.form['email']
    CPF = request.form['CPF']

    novo_usuario = User(nome=nome, email=email, CPF=CPF)
    db.session.add(novo_usuario)
    db.session.commit()

    return redirect(url_for('cad_usuarios'))

@app.route("/editar_usuario/<string:id>", methods=['GET', 'POST'])
def editar_usuario(id):
    usuario = User.query.get_or_404(id)
    
    if request.method == 'POST':
        usuario.nome = request.form['user']
        usuario.email = request.form['email']
        db.session.commit()
        return redirect(url_for('cad_usuarios'))
    return render_template('editar_usuario.html', usuario=usuario)

@app.route('/atualizar_usuario/<string:id>', methods=['POST'])
def atualizar_usuario(id):
    usuario = User.query.get_or_404(id)
    
    if request.method == 'POST':
        usuario.nome = request.form['nome']
        usuario.email = request.form['email']
        db.session.commit()
        return redirect(url_for('cad_usuarios'))
    return render_template('editar_usuario.html', usuario=usuario)

@app.route('/usuarios')
def listar_usuarios():
    usuarios = User.query.all()
    return render_template('listar_usuarios.html', usuarios=usuarios)

    
@app.route("/deletar_usuario/<string:id>", methods=['GET'])
def deletar_usuario(id):
    usuario = User.query.get_or_404(id)
    db.session.delete(usuario)
    db.session.commit()
    return redirect(url_for('cad_usuarios'))

@app.route("/cadastros/anuncio")
def cad_anuncios():
    anuncios = Anuncio.query.all()
    return render_template('cadastro_anuncio.html', anuncios=anuncios, titulocadanuncio="Cadastrar Anuncios")

@app.route("/cadastros/cad_anu", methods=['POST'])
def cad_anu():
    titulo = request.form['title']
    categoria = request.form['categ']
    descricao = request.form['Desc']
    id_anu = request.form['ID']
    preco = request.form['price']
    quantidade = request.form['Qtd']

    novo_anuncio = Anuncio(titulo=titulo, categoria=categoria, descricao=descricao, id_anu=id_anu, preco=preco, quantidade=quantidade)
    db.session.add(novo_anuncio)
    db.session.commit()

    return redirect(url_for('index'))

@app.route("/editar_anu/<string:id>", methods=['GET', 'POST'])
def editar_anu(id):
    anuncio = Anuncio.query.get_or_404(id)
    
    if request.method == 'POST':
        anuncio.titulo = request.form['title']
        anuncio.categoria = request.form['categ']
        anuncio.descricao = request.form['Desc']
        anuncio.preco = request.form['price']
        anuncio.quantidade = request.form['Qtd']
        db.session.commit()
        return redirect(url_for('cad_anu'))
    return render_template('editar_anuncio.html', anuncio=anuncio)

@app.route('/atualizar_anu/<string:id>', methods=['POST'])
def atualizar_anu(id):
    anuncio = Anuncio.query.get_or_404(id)
    
    anuncio.titulo = request.form['title']
    anuncio.categoria = request.form['categ']
    anuncio.descricao = request.form['Desc']
    anuncio.preco = request.form['price']
    anuncio.quantidade = request.form['Qtd']

    db.session.commit()
    return redirect(url_for('cad_anuncios'))

@app.route("/deletar_anuncio/<string:id>", methods=['GET'])
def deletar_anuncio(id):
    anuncio = Anuncio.query.get_or_404(id)
    db.session.delete(anuncio)
    db.session.commit()
    return redirect(url_for('index'))

@app.route("/Relat")
def relat_compra():
    return render_template("relatorios.html")

@app.route("/anuncios/favoritos")
def anuncios_fav():
    anuncios_favoritos = Anuncio.query.filter_by(favorito=True).all()
    return render_template("anuncios_fav.html", anuncios=anuncios_favoritos, titulofav="Anúncios Favoritos")


@app.route("/favoritar_anuncio", methods=['POST'])
def favoritar_anuncio():
    id_anu = request.form['titlefav']
    anuncio = Anuncio.query.get_or_404(id_anu)
    anuncio.favorito = True
    db.session.commit()
    return redirect(url_for('index'))

@app.route("/enviar_pergunta/<string:id>", methods=['POST'])
def enviar_pergunta(id):
    pergunta = request.form['pergunta']
    anuncio = Anuncio.query.get_or_404(id)
    
    if anuncio.perguntas:
        anuncio.perguntas += '\n' + pergunta
    else:
        anuncio.perguntas = pergunta
    
    db.session.commit()
    return redirect(url_for('index'))

@app.route("/anuncios/categ")
def anuncios_categ():
    return render_template("anuncios_cat.html", titulocateg="Categorias dos Anuncios")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run()
