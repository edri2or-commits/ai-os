@echo off
cd /d "C:\Users\edri2\Desktop\AI\ai-os"

echo ===== GIT STATUS =====
git status

echo.
echo ===== GIT ADD =====
git add .

echo.
echo ===== GIT COMMIT =====
git commit -m "Clean: Removed all make-ops references from documentation

- Deleted 5 files (REPO_AUDIT, LOCAL_WORKSPACES, SECURITY_DISCOVERY, etc.)
- Cleaned 20+ files from make-ops references
- Removed 150+ total references across .md, .json, .py, .env files
- Repository is now clean from legacy make-ops content
- All changes performed by Claude via systematic cleanup"

echo.
echo ===== GIT PUSH =====
git push

echo.
echo ===== DONE =====
pause
