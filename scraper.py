from urllib.request import urlopen
import json
from pathlib import Path

your_organization = "godatadriven"  # github.com/<your_organization>

fpath = Path("pullrequests.jsonl")
ids = [json.loads(line)['id'] for line in fpath.read_text().splitlines()]

with urlopen(f"https://api.github.com/orgs/{your_organization}/members") as response:
    org_members = json.loads(response.read())

for member in org_members:
    with urlopen(f"https://api.github.com/search/issues?q=state%3Aclosed+type%3Apr+author%3A{member['login']}") as response:
        user_body = json.loads(response.read())
    closed_prs =  user_body.get("items")

    for pr in closed_prs:
        if (pr['pull_request']['merged_at'] is not None) and pr['id'] not in ids:
            with fpath.open('a') as fp:
                json.dump(pr,fp)
                fp.write("\n")