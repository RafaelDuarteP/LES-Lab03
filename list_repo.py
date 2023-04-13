from graphqlclient import GraphQLClient
from datetime import datetime as date
import pandas as pd
import json
import os

url = "https://api.github.com/graphql"
token = "Bearer " + os.getenv('TOKEN_GITHUB')
today = date.utcnow()
variables = {"after": None}

query = """
query ($after: String) {
  search(query: "stars:>100", type: REPOSITORY, first: 50, after: $after) {
    pageInfo {
      endCursor
    }
    nodes {
      ... on Repository {
        nameWithOwner
        closed: pullRequests(states: CLOSED) {
          totalCount
        }
        merged: pullRequests(states: MERGED) {
          totalCount
        }
      }
    }
  }
}
"""
client = GraphQLClient(url)
client.inject_token(token=token)

data = []

while len(data) < 200:
    result = json.loads(client.execute(query=query, variables=variables))
    result = result["data"]["search"]
    end_cursor = result["pageInfo"]["endCursor"]

    variables["after"] = end_cursor
    repositories = result["nodes"]

    for repo in repositories:
        total_pr = repo['closed']['totalCount'] + repo['merged']['totalCount']
        if total_pr >= 100:
            data.append({
                'owner': repo['nameWithOwner'].split('/')[0],
                'name': repo['nameWithOwner'].split('/')[1],
                'total_prs': total_pr,
            })

df = pd.DataFrame(data=data[:200])

df.to_csv('lista-repo.csv', index=False)

print(df)