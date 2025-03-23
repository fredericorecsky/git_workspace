import os

from git import Repo
from pathlib import Path
from urllib.parse import urlparse

class GitRepository:
    def __init__(self, repository_url ):
        parsed_url = urlparse(repository_url)
        self.url = repository_url.rstrip("\n")
        self.url_domain = parsed_url.netloc
        self.url_path = parsed_url.path

        self.project = self.url_domain
        self.repository_name = os.path.basename(self.url_path)
        if self.repository_name.endswith(".git"):
            self.repository_name = self.repository_name[:-4]  

        self.repository_path = os.path.join(self.project, self.repository_name)

        self.cloned = False
        self.branch = None
        self.branch_clean = False
        self.branch_sync = False
        self.default_remote_branch = None

        self.local_commit = None
        self.remote_commit = None

        self.is_cloned()
        self.current_branch()

    def __str__(self):
         attributes = vars(self)
         return '\n'.join(
                 f"{key}={value}" for key, value in attributes.items()
         )

    def is_cloned(self):
        if Path( self.repository_path ).is_dir():
            self.cloned = True

    # rename to something useful
    def current_branch(self):
        if self.cloned:
            repo = Repo(self.repository_path)
            self.branch = repo.active_branch.name
            self.branch_clean = repo.is_dirty()

            self.local_commit = repo.head.commit.hexsha
            self.remote_commit = repo.refs[f'origin/{self.branch}'].commit.hexsha

            if self.local_commit == self.remote_commit:
                self.branch_sync = True
            #else:
            #    print( f"[{self.local_commit}][{self.remote_commit}]" )

    def clone(self):
        if not self.cloned:
            cloned = Repo.clone_from( self.url, self.repository_path )
            return cloned
        else:
            return None




