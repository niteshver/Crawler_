import asyncio
import httpx

# Configuration
GITHUB_TOKEN = "your_github_personal_access_token"  # Increases rate limit to 5000 req/hour
REPO_OWNER = "microsoft"                            # e.g., facebook, microsoft, openai
REPO_NAME = "vscode"                                # The repository name

HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}" if GITHUB_TOKEN else None,
    "Accept": "application/vnd.github.v3+json",
    "User-Agent": "EnterpriseURLExtractor/1.0"
}

async def fetch_urls_paginated(client: httpx.AsyncClient, endpoint: str, url_key: str = "html_url") -> list[str]:
    """Handles GitHub's page-by-page link pagination to extract all resource URLs safely."""
    urls = []
    url = f"https://github.com{REPO_OWNER}/{REPO_NAME}/{endpoint}"
    params = {"per_page": 100, "page": 1}
    
    while url:
        try:
            response = await client.get(url, params=params, headers=HEADERS, timeout=15.0)
            if response.status_code == 403:
                print("❌ Rate Limit Exceeded or Bad Token. Check response headers.")
                break
            response.raise_for_status()
            
            data = response.json()
            if not data:
                break
                
            # Extract URLs based on the resource type
            for item in data:
                if url_key in item:
                    urls.append(item[url_key])
            
            # Check GitHub's 'Link' header to see if a next page exists
            if "next" in response.links:
                url = response.links["next"]["url"]
                params = {} # Clear query parameters since URL contains them now
            else:
                url = None
                
        except Exception as e:
            print(f"⚠️ Error fetching {endpoint}: {e}")
            break
            
    return urls

async def get_project_docs_urls(client: httpx.AsyncClient) -> list[str]:
    """Extracts internal documentation markdown URLs (README & /docs directory)."""
    doc_urls = []
    # 1. Base Readme URL
    doc_urls.append(f"https://github.com/{REPO_OWNER}/{REPO_NAME}/blob/main/README.md")
    
    # 2. Search directory contents for a standard /docs folder structure
    api_url = f"https://github.com{REPO_OWNER}/{REPO_NAME}/contents/docs"
    try:
        res = await client.get(api_url, headers=HEADERS)
        if res.status_code == 200:
            doc_urls.extend([item["html_url"] for item in res.json() if item["type"] == "file"])
    except Exception:
        pass # Directory might not exist
        
    return doc_urls

async def run_github_pipeline():
    async with httpx.AsyncClient() as client:
        print(f"🚀 Starting URL discovery for {REPO_OWNER}/{REPO_NAME}...\n")
        
        # Concurrently gather Issues, PRs, and Docs 
        # Note: GitHub API treats PRs as a subset of issues, but separating gives cleaner control
        issues_task = fetch_urls_paginated(client, "issues?state=all")
        prs_task = fetch_urls_paginated(client, "pulls?state=all")
        docs_task = get_project_docs_urls(client)
        
        issues, prs, docs = await asyncio.gather(issues_task, prs_task, docs_task)
        
        # Process and filter out PR elements mixed inside standard issue endpoints
        clean_issue_urls = [url for url in issues if "/pull/" not in url]
        
        print("====== EXTRACTED TOPOLOGY ======")
        print(f"📑 Project Documentation URLs ({len(docs)} found):")
        for u in docs[:5]: print(f"  -> {u}")
        
        print(f"\n🐛 Open & Closed Issue URLs ({len(clean_issue_urls)} found):")
        for u in clean_issue_urls[:5]: print(f"  -> {u}")
            
        print(f"\n🔄 Pull Request URLs ({len(prs)} found):")
        for u in prs[:5]: print(f"  -> {u}")
        print("================================")

if __name__ == "__main__":
    asyncio.run(run_github_pipeline())
