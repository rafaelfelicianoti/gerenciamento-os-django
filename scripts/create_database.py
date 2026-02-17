#!/usr/bin/env python
"""Tenta criar o database Postgres definido nas variáveis de ambiente.

Lê: DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT
Conecta ao database 'postgres' e cria o database desejado se não existir.
"""
import os
import sys
try:
    import psycopg
except Exception as e:
    print('psycopg não está instalado:', e)
    sys.exit(1)


def main():
    db_name = os.environ.get('DB_NAME')
    db_user = os.environ.get('DB_USER')
    db_password = os.environ.get('DB_PASSWORD')
    db_host = os.environ.get('DB_HOST') or 'localhost'
    db_port = os.environ.get('DB_PORT') or '5432'

    if not db_name:
        print('ERRO: variável DB_NAME não definida.')
        sys.exit(1)

    print('Tentando criar database:', db_name)

    connect_params = {
        'host': db_host,
        'port': int(db_port),
        'user': db_user,
        'password': db_password,
        'dbname': 'postgres',
    }

    # Remove None values so psycopg uses defaults when appropriate
    connect_params = {k: v for k, v in connect_params.items() if v is not None}

    try:
        with psycopg.connect(**connect_params) as conn:
            conn.autocommit = True
            with conn.cursor() as cur:
                cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (db_name,))
                exists = cur.fetchone() is not None
                if exists:
                    print('Database já existe:', db_name)
                    return 0
                try:
                    sql = f'CREATE DATABASE "{db_name}"'
                    if db_user:
                        sql += f' OWNER "{db_user}"'
                    cur.execute(sql)
                    print('Database criada com sucesso:', db_name)
                    return 0
                except Exception as ce:
                    print('Falha ao criar database:', ce)
                    return 2
    except Exception as e:
        print('Erro conectando ao servidor Postgres:', e)
        return 3


if __name__ == '__main__':
    sys.exit(main())
