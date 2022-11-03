from urllib.request import urlopen
import json
from pathlib import Path

def get_closed_prs(username):
    with urlopen(f"https://api.github.com/search/issues?q=state%3Aclosed+type%3Apr+author%3A{username}") as response:
        user_body = json.loads(response.read())
    return user_body.get("items")

if __name__ == "__main__":
    your_organization = "godatadriven"

    fpath = Path("pullrequests.jsonl")
    ids = [json.loads(line)['id'] for line in fpath.read_text().splitlines()]
    
    with urlopen("https://api.github.com/orgs/{your_organization}/members") as response:
        org_members = json.loads(response.read())

    for member in org_members:
        closed_prs = get_closed_prs(member['login'])
        for pr in closed_prs:
            if (pr['pull_request']['merged_at'] is not None) and pr['id'] not in ids:
                with fpath.open('a') as fp:
                    json.dump(pr,fp)
                    fp.write("\n")