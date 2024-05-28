# Teste de Performance 4

# Importar bibliotecas SQL e Pandas
import sqlite3
import pandas as pd

# Criar conexão com a memória
conn = sqlite3.connect(':memory:')

# Lista de arquivos CSV e o nome correspondente da tabela
files = [
    ('Cargo.csv', 'Cargo'),
    ('Departamento.csv', 'Departamento'),
    ('Dependente.csv', 'Dependente'),
    ('Funcionario.csv', 'Funcionario'),
    ('Salarios.csv', 'Salarios'),
    ('Projeto.csv', 'Projeto'),
    ('Recurso.csv', 'Recurso')
]

# Loop para criar as tabelas 
for file, table in files:
    pd.read_csv(file).to_sql(table, conn, index=False)


# Trazer a média dos salários (atual) dos funcionários responsáveis por projetos concluídos, agrupados por departamento.
consulta_SQL_1 = """
SELECT d.NOME AS Departamento, AVG(s.Salario) AS MediaSalario
FROM Projeto p
JOIN Funcionario f ON p.Responsavel = f.Nome
JOIN Salarios s ON f.ID_FUNCIONARIO = s.ID_FUNCIONARIO
JOIN Departamento d ON f.ID_DEPARTAMENTO = d.ID_DEPARTAMENTO
WHERE p.Status = 'Concluído'
GROUP BY d.NOME;
"""

consulta_SQL_1 = pd.read_sql_query(consulta_SQL_1, conn)
print(consulta_SQL_1)


# Identificar os três recursos materiais mais usados nos projetos, listando a descrição do recursoe a quantidade total usada.
consulta_SQL_2 = """
SELECT r.Descricao, SUM(r.Quantidade) AS TotalUsado
FROM Projeto p
JOIN Recurso r ON p.Nome = r.Nome
GROUP BY r.Descricao
ORDER BY TotalUsado DESC
LIMIT 3;
"""

consulta_SQL_2 = pd.read_sql_query(consulta_SQL_2, conn)
print(consulta_SQL_2)


# Calcular o custo total dos projetos por departamento, considerando apenas os projetos 'Concluídos'.
consulta_SQL_3 = """
SELECT d.NOME AS Departamento, ROUND(SUM(p.Custo), 2) AS CustoTotal
FROM Projeto p
JOIN Funcionario f ON p.Responsavel = f.Nome
JOIN Departamento d ON f.ID_DEPARTAMENTO = d.ID_DEPARTAMENTO
WHERE p.Status = 'Concluído'
GROUP BY d.NOME;
"""

consulta_SQL_3 = pd.read_sql_query(consulta_SQL_3, conn)
print(consulta_SQL_3)


# Listar todos os projetos com seus respectivos nomes, custo, data de início, data de conclusão e o nome do funcionário responsável, que estejam 'Em Execução'.
consulta_SQL_4 = """
SELECT Nome AS Projeto, Custo, Data_inicial, Data_final, Responsavel
FROM Projeto
WHERE Status = 'Em Execução';
"""

consulta_SQL_4 = pd.read_sql_query(consulta_SQL_4, conn)
print(consulta_SQL_4)


# Identificar o projeto com o maior número de dependentes envolvidos, considerando que os dependentes são associados aos funcionários que estão gerenciando os projetos.
consulta_SQL_5 = """
SELECT p.Nome AS Projeto, COUNT(*) AS NumDependentes
FROM Projeto p
JOIN Dependente d ON p.Responsavel = d.Nome
GROUP BY p.Nome
ORDER BY NumDependentes DESC
LIMIT 1;
"""

consulta_SQL_5 = pd.read_sql_query(consulta_SQL_5, conn)
print(consulta_SQL_5)
