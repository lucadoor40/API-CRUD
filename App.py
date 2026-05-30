from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from enum import Enum

app = Flask(__name__)

# BANCO
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

#  HASH MAP
ativos_cache = {}

# ENUMS

class TipoAtivo(Enum):
    NOTEBOOK = "NOTEBOOK"
    SERVIDOR = "SERVIDOR"
    ROTEADOR = "ROTEADOR"
    SISTEMA_INTERNO = "SISTEMA_INTERNO"
    SOFTWARE_LICENCIADO = "SOFTWARE_LICENCIADO"


class Severidades(Enum):
    BAIXA = "baixa"
    MEDIA = "media"
    ALTA = "alta"
    MUITO_ALTA = "muito alta"


class Status(Enum):
    ABERTO = "aberto"
    EM_TRATAMENTO = "em tratamento"
    TRATADO = "tratado"
    ACEITO = "aceito"

# MODELOS

class Ativo(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    hostname = db.Column(db.String(100), nullable=False)
    responsavel = db.Column(db.String(100), nullable=False)
    setor = db.Column(db.String(100), nullable=False)

    tipo_ativo = db.Column(db.String(50), nullable=False)

    notebook = db.Column(db.String(100))
    servidor = db.Column(db.String(100))
    roteador = db.Column(db.String(100))
    sistema_interno = db.Column(db.String(100))
    software_licenciado = db.Column(db.String(100))

    vulnerabilidades = db.relationship(
        'Vulnerabilidade',
        backref='ativo',
        cascade="all, delete-orphan",
        lazy=True
    )

    def to_dict(self):
        return {
            "id": self.id,
            "hostname": self.hostname,
            "responsavel": self.responsavel,
            "setor": self.setor,
            "tipo_ativo": self.tipo_ativo,
            "vulnerabilidades": [
                {
                    "descricao": v.descricao,
                    "severidade": v.severidade,
                    "status": v.status,
                    "categoria": v.categoria
                }
                for v in self.vulnerabilidades
            ]
        }


class Vulnerabilidade(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    descricao = db.Column(db.String(100), nullable=False)
    categoria = db.Column(db.String(100), nullable=False)
    severidade = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), nullable=False)

    ativo_id = db.Column(db.Integer, db.ForeignKey('ativo.id'))


# CRIA BANCO
with app.app_context():
    db.create_all()

# FUNÇÃO ARQUIVO TXT

def salvar_em_arquivo(ativo):
    with open("ativos.txt", "a", encoding="utf-8") as f:
        f.write(f"""
ID: {ativo.id}
Hostname: {ativo.hostname}
Responsável: {ativo.responsavel}
Setor: {ativo.setor}
Tipo: {ativo.tipo_ativo}
-----------------------------
""")

# ROTAS ATIVOS

@app.route('/ativos', methods=['POST'])
def criar_ativo():
    dados = request.json

    # validações obrigatórias
    if not dados.get("hostname"):
        return jsonify({"erro": "hostname obrigatório"}), 400

    if not dados.get("responsavel"):
        return jsonify({"erro": "responsável obrigatório"}), 400

    if not dados.get("setor"):
        return jsonify({"erro": "setor obrigatório"}), 400

    # cria ativo
    novo = Ativo(
        hostname=dados.get("hostname"),
        responsavel=dados.get("responsavel"),
        setor=dados.get("setor"),
        tipo_ativo=dados.get("tipo_ativo")
    )

    db.session.add(novo)
    db.session.commit()

    #  SALVA NO DICT
    ativos_cache[novo.id] = novo.to_dict()

    #  SALVA EM ARQUIVO
    salvar_em_arquivo(novo)

    return jsonify({
        "msg": "Ativo criado com sucesso",
        "id": novo.id
    })


@app.route('/ativos', methods=['GET'])
def listar_ativos():
    return jsonify(list(ativos_cache.values()))


@app.route('/ativos/<int:id>', methods=['PUT'])
def atualizar_ativo(id):
    ativo = Ativo.query.get(id)

    if not ativo:
        return jsonify({"erro": "não encontrado"}), 404

    dados = request.json

    ativo.hostname = dados.get("hostname", ativo.hostname)
    ativo.responsavel = dados.get("responsavel", ativo.responsavel)
    ativo.setor = dados.get("setor", ativo.setor)

    db.session.commit()

    ativos_cache[id] = ativo.to_dict()

    return jsonify({"msg": "atualizado"})


@app.route('/ativos/<int:id>', methods=['DELETE'])
def deletar_ativo(id):
    ativo = Ativo.query.get(id)

    if not ativo:
        return jsonify({"erro": "não encontrado"}), 404

    db.session.delete(ativo)
    db.session.commit()

    ativos_cache.pop(id, None)

    return jsonify({"msg": "removido"})

# VULNERABILIDADES

@app.route('/vulnerabilidades', methods=['POST'])
def criar_vuln():
    dados = request.json

    vuln = Vulnerabilidade(
        descricao=dados.get("descricao"),
        categoria=dados.get("categoria"),
        severidade=dados.get("severidade"),
        status=dados.get("status"),
        ativo_id=dados.get("ativo_id")
    )

    db.session.add(vuln)
    db.session.commit()

    # atualiza cache do ativo
    ativo = Ativo.query.get(dados.get("ativo_id"))
    if ativo:
        ativos_cache[ativo.id] = ativo.to_dict()

    return jsonify({"msg": "vulnerabilidade criada"})


@app.route('/vulnerabilidades/<int:id>', methods=['GET'])
def listar_vuln(id):
    ativo = Ativo.query.get(id)

    if not ativo:
        return jsonify({"erro": "não encontrado"}), 404

    if not ativo.vulnerabilidades:
        return jsonify({"msg": "sem vulnerabilidades"}), 404

    return jsonify([
        {
            "descricao": v.descricao,
            "categoria": v.categoria,
            "severidade": v.severidade,
            "status": v.status
        }
        for v in ativo.vulnerabilidades
    ])


# RUN

if __name__ == "__main__":
    app.run(debug=True)