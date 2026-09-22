import sqlite3
from datetime import datetime

DB_PATH = "/home/th/Downloads/Bitnet_TTS/memoria.db"


def _conectar():
    return sqlite3.connect(DB_PATH)


def criar_banco():
    conn = _conectar()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pergunta TEXT,
            resposta TEXT,
            horario TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS nao_respondidas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pergunta_bruta TEXT,
            pergunta_corrigida TEXT,
            horario TEXT
        )
    """)

    conn.commit()
    conn.close()


def salvar_conversa(pergunta: str, resposta: str) -> None:
    conn = _conectar()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO conversa (pergunta, resposta, horario) VALUES (?, ?, ?)",
        (pergunta, resposta, datetime.now().isoformat()),
    )
    conn.commit()
    conn.close()


def registrar_nao_respondida(pergunta_bruta: str, pergunta_corrigida: str) -> None:
    """Chame isso sempre que o brain.py cair no fallback 'não entendi'.
    Depois, rode listar_nao_respondidas() para ver o que vale a pena
    adicionar na lista FRASES do brain.py."""
    conn = _conectar()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO nao_respondidas (pergunta_bruta, pergunta_corrigida, horario) "
        "VALUES (?, ?, ?)",
        (pergunta_bruta, pergunta_corrigida, datetime.now().isoformat()),
    )
    conn.commit()
    conn.close()


def listar_nao_respondidas(limite: int = 50):
    """Útil para rodar manualmente depois de uma sessão de testes:
        python -c "import memoria; memoria.listar_nao_respondidas()"
    """
    conn = _conectar()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT pergunta_bruta, horario FROM nao_respondidas "
        "ORDER BY id DESC LIMIT ?",
        (limite,),
    )
    linhas = cursor.fetchall()
    conn.close()

    for pergunta, horario in linhas:
        print(f"[{horario}] {pergunta}")
    return linhas


def obter_memoria(limite: int = 10):
    conn = _conectar()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT pergunta, resposta FROM conversa ORDER BY id DESC LIMIT ?",
        (limite,),
    )
    resultado = cursor.fetchall()
    conn.close()
    return list(reversed(resultado))