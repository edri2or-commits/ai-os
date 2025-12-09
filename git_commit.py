#!/usr/bin/env python3
"""Git commit helper"""
import subprocess
import sys

def run_git(*args):
    """Run git command"""
    result = subprocess.run(
        ['git', *args],
        cwd=r'C:\Users\edri2\Desktop\AI\ai-os',
        capture_output=True,
        text=True
    )
    print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)
    return result.returncode

if __name__ == "__main__":
    # Stage files
    print("Staging files...")
    run_git('add', 
            'memory-bank/01-active-context.md',
            'memory-bank/02-progress.md',
            'create_context_files.py')
    
    # Commit
    print("\nCommitting...")
    run_git('commit', '-m', 'docs(memory-bank): UTF-8 encoding fix for Hebrew context files')
    
    # Show last commit
    print("\nLast commit:")
    run_git('log', '--oneline', '-1')
