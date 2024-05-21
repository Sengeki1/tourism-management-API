from database.session import engine
from app.api.models.model import Base, Quarto

# Cria todas as tabelas
Base.metadata.create_all(bind=engine)

# Inicializa os dados de quartos
def init_quartos():
    from sqlalchemy.orm import Session
    from app.database.session import conectar_bd

    db: Session = conectar_bd()
    try:
        # Verifica se os quartos já estão inicializados
        if not db.query(Quarto).first():
            db.add_all([
                Quarto(classe="A", quantidade=5),
                Quarto(classe="B", quantidade=15),
                Quarto(classe="C", quantidade=30)
            ])
            db.commit()
    finally:
        db.close()

# Executa a inicialização
init_quartos()
