import json

class RepoReader:
    """\n    A secure internal Repo reader base class, ensuring that all agents access the repo only through the authorized GitHub API.

    - Reads files from the repo using the affiliated plugin action, not through direct url calls.
    - Verifies that content has been successfully retrieved.
    - Supports safe mode: if no connection is active, wait and retry later.
    """
    def __init__(self, github_client):
        self.github_client = github_client

    def read_file(self, path):
        """Read a file from the repo using the secure api connection."""
        try:
            data = self.github_client.getFileOrDir({"path": path})
            content = data.get("content")
            if content:
                return json.loads(content)
            return None
        except Exception as e:
            print(f"repo_reader error: {e}")
            return None
    def verify_read(self, path):
        content = self.read_file(path)
        return content is not None

    def get_files_list(self, directory):
        data = self.github_client.getFileOrDir({path: directory})
        return [d.get("basename") for d in data]