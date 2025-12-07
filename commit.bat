@echo off
cd /d C:\Users\edri2\Desktop\AI\ai-os
"C:\Program Files\Git\cmd\git.exe" add memory-bank/01-active-context.md memory-bank/02-progress.md create_context_files.py
"C:\Program Files\Git\cmd\git.exe" commit -m "docs(memory-bank): UTF-8 encoding fix for Hebrew context files"
"C:\Program Files\Git\cmd\git.exe" log --oneline -1
pause
