from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import re

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_aqui_mude_em_producao'

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def validar_email(email):
    if not email:
        return True  # Email é opcional
    padrao = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(padrao, email) is not None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chamados')
def listar_chamados():
    conn = get_db_connection()
    
    # Filtros opcionais
    filtro_status = request.args.get('status', '')
    filtro_prioridade = request.args.get('prioridade', '')
    filtro_usuario = request.args.get('usuario', '')
    
    query = 'SELECT * FROM chamados WHERE 1=1'
    params = []
    
    if filtro_status:
        query += ' AND status = ?'
        params.append(filtro_status)
    
    if filtro_prioridade:
        query += ' AND prioridade = ?'
        params.append(filtro_prioridade)
    
    if filtro_usuario:
        query += ' AND aberto_por LIKE ?'
        params.append(f'%{filtro_usuario}%')
    
    query += ' ORDER BY data_abertura DESC'
    
    chamados = conn.execute(query, params).fetchall()
    conn.close()
    
    return render_template('chamados.html', chamados=chamados, 
                         filtro_status=filtro_status,
                         filtro_prioridade=filtro_prioridade,
                         filtro_usuario=filtro_usuario)

@app.route('/abrir_chamado', methods=['GET', 'POST'])
def abrir_chamado():
    if request.method == 'POST':
        titulo = request.form['titulo']
        descricao = request.form['descricao']
        categoria = request.form['categoria']
        prioridade = request.form['prioridade']
        aberto_por = request.form['aberto_por']
        email_contato = request.form.get('email_contato', '')
        telefone_contato = request.form.get('telefone_contato', '')
        
        # Validações
        if not titulo or not descricao or not aberto_por:
            flash('Título, descrição e nome são obrigatórios!', 'error')
            return redirect(url_for('abrir_chamado'))
        
        if email_contato and not validar_email(email_contato):
            flash('E-mail inválido!', 'error')
            return redirect(url_for('abrir_chamado'))
        
        conn = get_db_connection()
        conn.execute('''
            INSERT INTO chamados (titulo, descricao, categoria, prioridade, 
                                 aberto_por, email_contato, telefone_contato)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (titulo, descricao, categoria, prioridade, aberto_por, email_contato, telefone_contato))
        conn.commit()
        conn.close()
        
        flash(f'Chamado aberto com sucesso por {aberto_por}!', 'success')
        return redirect(url_for('listar_chamados'))
    
    return render_template('abrir_chamado.html')

@app.route('/atualizar/<int:id>', methods=['GET', 'POST'])
def atualizar_chamado(id):
    conn = get_db_connection()
    chamado = conn.execute('SELECT * FROM chamados WHERE id = ?', (id,)).fetchone()
    
    if request.method == 'POST':
        titulo = request.form['titulo']
        descricao = request.form['descricao']
        categoria = request.form['categoria']
        prioridade = request.form['prioridade']
        status = request.form['status']
        aberto_por = request.form['aberto_por']
        email_contato = request.form.get('email_contato', '')
        telefone_contato = request.form.get('telefone_contato', '')
        
        if email_contato and not validar_email(email_contato):
            flash('E-mail inválido!', 'error')
            return redirect(url_for('atualizar_chamado', id=id))
        
        conn.execute('''
            UPDATE chamados 
            SET titulo = ?, descricao = ?, categoria = ?, 
                prioridade = ?, status = ?, aberto_por = ?,
                email_contato = ?, telefone_contato = ?,
                data_atualizacao = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (titulo, descricao, categoria, prioridade, status, 
              aberto_por, email_contato, telefone_contato, id))
        conn.commit()
        conn.close()
        
        flash('Chamado atualizado com sucesso!', 'success')
        return redirect(url_for('listar_chamados'))
    
    conn.close()
    return render_template('atualizar.html', chamado=chamado)

@app.route('/excluir/<int:id>')
def excluir_chamado(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM chamados WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    
    flash('Chamado excluído com sucesso!', 'success')
    return redirect(url_for('listar_chamados'))

@app.route('/detalhes/<int:id>')
def detalhes_chamado(id):
    conn = get_db_connection()
    chamado = conn.execute('SELECT * FROM chamados WHERE id = ?', (id,)).fetchone()
    conn.close()
    
    if chamado is None:
        flash('Chamado não encontrado!', 'error')
        return redirect(url_for('listar_chamados'))
    
    return render_template('detalhes.html', chamado=chamado)

@app.route('/meus_chamados/<nome>')
def meus_chamados(nome):
    conn = get_db_connection()
    # CORREÇÃO: F-string corrigida - separando corretamente a string SQL do parâmetro
    sql = "SELECT * FROM chamados WHERE aberto_por LIKE ? ORDER BY data_abertura DESC"
    chamados = conn.execute(sql, ('%' + nome + '%',)).fetchall()
    conn.close()
    
    return render_template('chamados.html', chamados=chamados, 
                         titulo=f"Chamados de {nome}")

@app.route('/estatisticas')
def estatisticas():
    conn = get_db_connection()
    
    # Estatísticas gerais
    total = conn.execute('SELECT COUNT(*) as total FROM chamados').fetchone()['total']
    
    # Chamados por status
    por_status = conn.execute('''
        SELECT status, COUNT(*) as quantidade 
        FROM chamados 
        GROUP BY status
    ''').fetchall()
    
    # Chamados por prioridade
    por_prioridade = conn.execute('''
        SELECT prioridade, COUNT(*) as quantidade 
        FROM chamados 
        GROUP BY prioridade
    ''').fetchall()
    
    # Chamados por usuário (top 5)
    por_usuario = conn.execute('''
        SELECT aberto_por, COUNT(*) as quantidade 
        FROM chamados 
        GROUP BY aberto_por 
        ORDER BY quantidade DESC 
        LIMIT 5
    ''').fetchall()
    
    conn.close()
    
    return render_template('estatisticas.html', 
                         total=total,
                         por_status=por_status,
                         por_prioridade=por_prioridade,
                         por_usuario=por_usuario)

if __name__ == '__main__':
    app.run(debug=True)