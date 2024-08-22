from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import (current_user, LoginManager, login_user, logout_user, login_required)
from flask import flash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://leonardocirino:leo12341848@leonardocirino.mysql.pythonanywhere-services.com:3306/leonardocirino$frameleo'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

app.secret_key = '1234'
Login_Manager = LoginManager()
Login_Manager.init_app(app)
Login_Manager.login_view = 'login'

class User(db.Model):
    __tablename__ = 'usuario'
    CPF = db.Column('usu_CPF', db.String(256), primary_key=True)
    nome = db.Column('usu_nome', db.String(256))
    email = db.Column('usu_email', db.String(256))
    passwd = db.Column('usu_pass', db.String(256))

    def __init__(self, nome, email, CPF, passwd):
        self.nome = nome
        self.email = email
        self.CPF = CPF
        self.passwd = passwd

    def is_authenticated(self):
        return True
    
    def is_active(self):
        return True

    def is_anonymous(self):
        return False
    
    def get_id(self):
        return str(self.CPF)

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

@Login_Manager.user_loader
def load_user(CPF):
    return User.query.get(CPF)

@app.route("/")
def index():
    anuncios = Anuncio.query.all()
    return render_template('index.html', anuncios=anuncios)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        cpf = request.form.get('cpf')
        passwd = request.form.get('passwd')

        user = User.query.filter_by(CPF=cpf, passwd=passwd).first()

        if user:
            login_user(user)
            return redirect(url_for('listar_usuarios'))  # Redireciona para a lista de usuários
        else:
            flash('Login inválido. Verifique seu CPF e senha e tente novamente.')
            return redirect(url_for('login'))
    return render_template('login.html')



@app.route("/cadastros/user")
def cad_usuarios():
    usuarios = User.query.all()
    return render_template("cadastro_user.html", titulocaduser="Cadastrar Usuários", usuarios=usuarios)

@app.route("/cadastros/cad_user", methods=['POST'])
def cad_user():
    nome = request.form['user']
    email = request.form['email']
    CPF = request.form['CPF']
    passwd = request.form['passwd']

    novo_usuario = User(nome=nome, email=email, CPF=CPF, passwd=passwd)
    db.session.add(novo_usuario)
    db.session.commit()

    return redirect(url_for('cad_usuarios'))

@app.route("/cadastros/anuncio", methods=['GET', 'POST'])
@login_required
def cad_anuncios():
    anuncios = Anuncio.query.all()
    return render_template('cadastro_anuncio.html', anuncios=anuncios, titulocadanuncio="Cadastrar Anuncios")

@app.route("/cadastros/cad_anu", methods=['POST'])
@login_required
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

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route("/Relat")
@login_required
def relat_compra():
    return render_template("relatorios.html")

@app.route("/usuarios")
@login_required
def listar_usuarios():
    usuarios = User.query.all()
    return render_template('listar_usuarios.html', usuarios=usuarios)


@app.route("/editar_usuario/<string:cpf>", methods=['GET', 'POST'])
@login_required
def editar_usuario(cpf):
    usuario = User.query.get_or_404(cpf)
    
    if request.method == 'POST':
        usuario.nome = request.form['user']
        usuario.email = request.form['email']
        db.session.commit()
        return redirect(url_for('listar_usuarios'))
    
    return render_template('editar_usuario.html', usuario=usuario)


@app.route("/deletar_usuario/<string:cpf>", methods=['GET'])
def deletar_usuario(cpf):
    usuario = User.query.get_or_404(cpf)
    db.session.delete(usuario)
    db.session.commit()
    return redirect(url_for('listar_usuarios'))


@app.route("/editar_anu/<string:id>", methods=['GET', 'POST'])
@login_required
def editar_anu(id):
    anuncio = Anuncio.query.get_or_404(id)
    
    if request.method == 'POST':
        anuncio.titulo = request.form['title']
        anuncio.categoria = request.form['categ']
        anuncio.descricao = request.form['Desc']
        anuncio.preco = request.form['price']
        anuncio.quantidade = request.form['Qtd']
        db.session.commit()
        return redirect(url_for('cad_anuncios'))
    return render_template('editar_anuncio.html', anuncio=anuncio)

@app.route("/deletar_anuncio/<string:id>", methods=['GET'])
@login_required
def deletar_anuncio(id):
    anuncio = Anuncio.query.get_or_404(id)
    db.session.delete(anuncio)
    db.session.commit()
    return redirect(url_for('index'))

@app.route("/anuncios/favoritos")
@login_required
def anuncios_fav():
    anuncios_favoritos = Anuncio.query.filter_by(favorito=True).all()
    return render_template("anuncios_fav.html", anuncios=anuncios_favoritos, titulofav="Anúncios Favoritos")

@app.route("/favoritar_anuncio", methods=['POST'])
@login_required
def favoritar_anuncio():
    id_anu = request.form['titlefav']
    anuncio = Anuncio.query.get_or_404(id_anu)
    anuncio.favorito = True
    db.session.commit()
    return redirect(url_for('index'))

@app.route("/enviar_pergunta/<string:id>", methods=['POST'])
@login_required
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
        
        if User.query.filter_by(CPF='admin').first() is None:
            admin_user = User(nome='Admin', email='admin@example.com', CPF='admin', passwd='admin123')
            db.session.add(admin_user)
            db.session.commit()

        app.run()
