import os
import fnmatch

def is_text_file(filepath):
    try:
        with open(filepath, 'rb') as f:
            chunk = f.read(1024)
            if b'\0' in chunk:
                return False
            return True
    except:
        return False

exclude_dirs = {'sampledata', '__pycache__', 'build', 'dist', '.eggs', '.git', 'venv', '.venv', '.vscode', '.idea', '.pytest_cache', '.mypy_cache', 'htmlcov', 'node_modules', 'frontend/build', 'frontend/dist', 'backend/__pycache__', 'backend/staticfiles', 'backend/media', 'txts', 'instance', 'coverage'}

def should_exclude_file(filepath):
    file = os.path.basename(filepath)
    # Specific files
    if file in {'codebase_bundle.md', 'bundle.py'}:
        return True
    # Pattern matches
    if fnmatch.fnmatch(file, '*.py[co]') or fnmatch.fnmatch(file, '*.log') or fnmatch.fnmatch(file, '*.swp') or fnmatch.fnmatch(file, '*.swo') or fnmatch.fnmatch(file, '.DS_Store') or fnmatch.fnmatch(file, '*.bak') or fnmatch.fnmatch(file, '*.tmp') or fnmatch.fnmatch(file, '*.out') or fnmatch.fnmatch(file, '*.spec') or fnmatch.fnmatch(file, '*.db') or fnmatch.fnmatch(file, '*.sqlite3') or fnmatch.fnmatch(file, '*.pid') or fnmatch.fnmatch(file, '*.seed') or fnmatch.fnmatch(file, '*.sock') or fnmatch.fnmatch(file, '*.tar') or fnmatch.fnmatch(file, 'Thumbs.db') or fnmatch.fnmatch(file, 'ehthumbs.db') or fnmatch.fnmatch(file, 'Desktop.ini') or fnmatch.fnmatch(file, '*.csv'):
        return True
    if file.startswith('.env') or file.startswith('npm-debug.log') or file.startswith('yarn-debug.log') or file.startswith('yarn-error.log') or file.startswith('.pnpm-debug.log'):
        return True
    # Specific files
    if file in {'package-lock.json', 'yarn.lock', 'docker-compose.override.yml'}:
        return True
    return False

with open('codebase_bundle.md', 'w') as out:
    for root, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        for file in files:
            filepath = os.path.join(root, file)
            if should_exclude_file(filepath):
                continue
            if is_text_file(filepath):
                out.write(f'# File: {filepath}\n\n')
                try:
                    with open(filepath, 'r') as f:
                        content = f.read()
                        if filepath.endswith('.py'):
                            out.write('```python\n')
                        elif filepath.endswith('.tsx') or filepath.endswith('.ts'):
                            out.write('```typescript\n')
                        elif filepath.endswith('.js'):
                            out.write('```javascript\n')
                        elif filepath.endswith('.json'):
                            out.write('```json\n')
                        elif filepath.endswith('.css'):
                            out.write('```css\n')
                        elif filepath.endswith('.html'):
                            out.write('```html\n')
                        elif filepath.endswith('.yml') or filepath.endswith('.yaml'):
                            out.write('```yaml\n')
                        elif filepath.endswith('.sh'):
                            out.write('```bash\n')
                        elif filepath.endswith('.md'):
                            out.write('```markdown\n')
                        else:
                            out.write('```\n')
                        out.write(content)
                        out.write('\n```\n\n')
                except UnicodeDecodeError:
                    pass  # skip if decode error
