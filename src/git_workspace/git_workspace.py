"""
Wrapper for Git 
"""

import argparse
import pandas as pd
import os
import sys

from git_workspace import __version__
from git_workspace.gitrepo import GitRepository
from pathlib import Path

def load_repositories():
    """
    Load the repositories from the configuration file. Defaults to 
    current directory file named "repositories.txt"
    """
    default_repository_file = "repositories.txt"

    repositories = []
    if Path(default_repository_file).is_file():
        with open( default_repository_file, "r" ) as repo_file:
            for line in repo_file:
                repo = GitRepository( line ) 
                repositories.append( repo )
    else:
        print("Could not find the repositories file: repositories.txt")

    return repositories

def show_repositories_details(repositories):
    # use colorama
    for repo in repositories:
        print( repo )
        print()
        #print( repo.__dict__ )

def repositories_list(df):
    df_output = df[['project','repository_name', 'cloned', 'branch', 'branch_sync' ]]
    print( df_output)

def clone_repository(repository_url):
    print( f"Will clone {repository_url} " )
    repo = GitRepository( repository_url )
    if repo.clone():
        print( f"Cloned Repository {repo.repository_name} at {repo.repository_path}" )
    else:
        print( f"The {repo.repository_name} is already cloned at {repo.repository_path}" )
    return

def parse_args(args):
    parser = argparse.ArgumentParser(
            description="Git Workspace Manager" 
    )
    parser.add_argument(
            "--version",
            action="version",
            version=f"git_workspace{__version__}",
    )
    parser.add_argument(
            "--repos",
            action="store_true",
            help="Print the list of repositories"
    )
    parser.add_argument(
            "--filter",
            type=str,
            help="will filter the repositories by the string"
    )
    parser.add_argument(
            "--status",
            action="store_true",
            help="Print the current overview and repos status" 
    )
    parser.add_argument(
            '--clone', 
            type=int,
            help="Will clone locally the repository number n" 
    )
    if len( args ) == 0:
        parser.print_help()
        sys.exit(1)

    return parser.parse_args(args)

def run():
    args = parse_args(sys.argv[1:])

    repositories = load_repositories()
    df = pd.DataFrame([vars(item) for item in repositories])

    if args.status:
        repositories_list(df)
        sys.exit()

    if args.clone != None:
        print( f"clone {args.clone}" )
        clone_repository(df.iloc[args.clone]['url'])
        sys.exit()

    
    if args.repos:
        show_repositories_details(repositories)


if __name__ == "__main__":
    run()
