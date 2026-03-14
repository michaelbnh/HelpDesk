import sqlite3
import os

def criar_banco():
    if os.path.exists('database.db'):
        resposta = input("Banco de dados já existe. Deseja recriá-lo? (s/N): ")
        if resposta.lower() == 's':
            os.remove('database.db')
            print("Banco de dados antigo removido.")
        else:
            print("Operação cancelada.")
            return
    
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE chamados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            descricao TEXT NOT NULL,
            categoria TEXT NOT NULL,
            prioridade TEXT NOT NULL,
            status TEXT DEFAULT 'Aberto',
            aberto_por TEXT NOT NULL,
            email_contato TEXT,
            telefone_contato TEXT,
            data_abertura DATETIME DEFAULT CURRENT_TIMESTAMP,
            data_atualizacao DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Inserir alguns dados de exemplo
    cursor.execute('''
        INSERT INTO chamados (titulo, descricao, categoria, prioridade, aberto_por, email_contato, telefone_contato)
        VALUES 
            ('Computador não liga', 'O computador não liga após queda de energia', 'Hardware', 'Alta', 'João Silva', 'joao@empresa.com', '(11) 99999-8888'),
            ('Erro no Excel', 'Excel está fechando sozinho ao salvar', 'Software', 'Média', 'Maria Santos', 'maria@empresa.com', '(11) 97777-6666'),
            ('Internet lenta', 'Conexão está muito lenta hoje', 'Rede', 'Baixa', 'Pedro Oliveira', 'pedro@empresa.com', '(11) 95555-4444')
    ''')
    
    conn.commit()
    conn.close()
    
    print("✅ Banco de dados criado com sucesso!")
    print("📊 Tabela 'chamados' criada com as colunas:")
    print("   - id")
    print("   - titulo")
    print("   - descricao")
    print("   - categoria")
    print("   - prioridade")
    print("   - status")
    print("   - aberto_por")
    print("   - email_contato")
    print("   - telefone_contato")
    print("   - data_abertura")
    print("   - data_atualizacao")

if __name__ == "__main__":
    criar_banco()