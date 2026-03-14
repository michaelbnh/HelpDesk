import sqlite3

def adicionar_coluna_usuario():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # Verificar se a coluna já existe
    cursor.execute("PRAGMA table_info(chamados)")
    colunas = [coluna[1] for coluna in cursor.fetchall()]
    
    if 'aberto_por' not in colunas:
        try:
            cursor.execute("ALTER TABLE chamados ADD COLUMN aberto_por TEXT NOT NULL DEFAULT 'Usuário Anônimo'")
            print("✅ Coluna 'aberto_por' adicionada com sucesso!")
        except sqlite3.OperationalError as e:
            print(f"Erro ao adicionar coluna: {e}")
    else:
        print("ℹ️ Coluna 'aberto_por' já existe.")
    
    if 'email_contato' not in colunas:
        try:
            cursor.execute("ALTER TABLE chamados ADD COLUMN email_contato TEXT")
            print("✅ Coluna 'email_contato' adicionada com sucesso!")
        except sqlite3.OperationalError as e:
            print(f"Erro ao adicionar coluna: {e}")
    else:
        print("ℹ️ Coluna 'email_contato' já existe.")
    
    if 'telefone_contato' not in colunas:
        try:
            cursor.execute("ALTER TABLE chamados ADD COLUMN telefone_contato TEXT")
            print("✅ Coluna 'telefone_contato' adicionada com sucesso!")
        except sqlite3.OperationalError as e:
            print(f"Erro ao adicionar coluna: {e}")
    else:
        print("ℹ️ Coluna 'telefone_contato' já existe.")
    
    conn.commit()
    conn.close()
    print("\n✅ Migração concluída!")

if __name__ == "__main__":
    adicionar_coluna_usuario()