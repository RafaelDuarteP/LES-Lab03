from graphqlclient import GraphQLClient
from datetime import datetime
import pandas as pd
import json
import os
import time

url = "https://api.github.com/graphql"
token = "Bearer " + os.getenv('TOKEN_GITHUB')
variables = {
    'after': None,
    'name': None,
    'owner': None,
}

query = """
query ($after: String, $owner: String!, $name: String!) {
  repository(name: $name, owner: $owner) {
    pullRequests(first: 100, after: $after,states: [CLOSED, MERGED]) {
      pageInfo {
        endCursor
        hasNextPage
      }
      nodes {
        createdAt
        closedAt
        reviews {
          totalCount
        }
        state
        body
        files {
          totalCount
        }
      }
    }
  }
}
"""
client = GraphQLClient(url)
client.inject_token(token=token)

repo_list = pd.read_csv('lista-repo.csv')
data = []

for i, row in repo_list.iterrows():
    variables["name"] = row['name']
    variables["owner"] = row['owner']
    has_next = True
    try:
        while has_next:
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
                reviews = pr['reviews']['totalCount']
                created_at = datetime.strptime(pr['createdAt'],
                                               '%Y-%m-%dT%H:%M:%SZ')
                closed_at = datetime.strptime(pr['closedAt'],
                                              '%Y-%m-%dT%H:%M:%SZ')
                tempo = (closed_at - created_at).total_seconds()
                if reviews >= 1 and tempo >= 3600:
                    data.append({
                        'tamanho': pr['files']['totalCount'],
                        'tempo': tempo,
                        'descricao': len(pr['body']),
                        'interacoes': reviews,
                    })
    except Exception as e:
        print(e)

df = pd.DataFrame(data=data)
df.to_csv('dados_pr.csv')
