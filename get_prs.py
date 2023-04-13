import traceback
from graphqlclient import GraphQLClient
from datetime import datetime
import pandas as pd
import json
import os
import time

qtd_iteracoes = 0

last_token = 0
url = "https://api.github.com/graphql"
token_rafael = os.getenv('TOKEN_GITHUB')
token_davi = os.getenv('TOKEN_GITHUB_DAVI')
variables = {
    'after': None,
    'name': None,
    'owner': None,
}


def swap_token():
    global last_token
    if last_token == 0:
        last_token += 1
        return token_rafael
    else:
        last_token -= 1
        return token_davi


query = """
query ($after: String, $owner: String!, $name: String!) {
  repository(name: $name, owner: $owner) {
    pullRequests(first: 100, after: $after, states: [CLOSED, MERGED]) {
      pageInfo {
        endCursor
        hasNextPage
      }
      nodes {
        id
        createdAt
        closedAt
        reviews { totalCount }
        state
        body
        files { totalCount }
        comments { totalCount }
      }
    }
  }
}
"""
client = GraphQLClient(url)

repo_list = pd.read_csv('lista-repo-1.csv')
print(repo_list)
data = []

for i, row in repo_list.iterrows():
    variables["name"] = row['name']
    variables["owner"] = row['owner']
    variables["after"] = None
    has_next = True
    while has_next:
        try:
            print('nº iteraçoes: ', qtd_iteracoes)
            qtd_iteracoes += 1
            token = "Bearer " + swap_token()
            client.inject_token(token=token)
            time.sleep(0.05)
            result = json.loads(
                client.execute(
                    query=query,
                    variables=variables))["data"]["repository"]["pullRequests"]
            end_cursor = result["pageInfo"]["endCursor"]
            has_next = result["pageInfo"]["hasNextPage"]
            variables["after"] = end_cursor
            pull_requests = result["nodes"]
            for pr in pull_requests:
                created_at = datetime.strptime(pr['createdAt'],
                                               '%Y-%m-%dT%H:%M:%SZ')
                closed_at = datetime.strptime(pr['closedAt'],
                                              '%Y-%m-%dT%H:%M:%SZ')
                data.append({
                    'repo': row['name'],
                    'owner': row['owner'],
                    'id': pr['id'],
                    'tamanho': pr['files']['totalCount'],
                    'created_at': created_at,
                    'closed_at': closed_at,
                    'descricao': len(pr['body']),
                    'interacoes': pr['comments']['totalCount'],
                    'reviews': pr['reviews']['totalCount'],
                    'state': pr['state']
                })
                df = pd.DataFrame(data=data)
                df.to_csv('dados_pr.csv', index=False)
        except Exception as e:
            print(e)
            swap_token()
            with open('log.txt', '+a') as f:
                f.write(row['name'] + ',' + row['owner'] + ',' +
                        variables["after"] + '\n')

print(df)