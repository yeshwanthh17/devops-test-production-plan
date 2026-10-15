"""Local dummy monitoring endpoint; no production business functionality."""
import subprocess
from pathlib import Path
from urllib.parse import urlsplit
import frappe

@frappe.whitelist()
def get_deployed_app_versions():
    from frappe.utils.change_log import get_versions
    versions = get_versions()
    for app, details in versions.items():
        path = Path(frappe.get_app_path(app))
        def git(*args):
            result = subprocess.run(['git', '-C', str(path), *args], capture_output=True, text=True, timeout=5)
            return result.stdout.strip() if result.returncode == 0 else ''
        branch = git('symbolic-ref', '--quiet', '--short', 'HEAD') or 'HEAD'
        commit = git('rev-parse', 'HEAD')
        tags = git('tag', '--points-at', 'HEAD').splitlines()
        remote = git('remote', 'get-url', 'origin') or git('remote', 'get-url', 'upstream')
        if remote.startswith('git@github.com:'):
            remote = 'https://github.com/' + remote.split(':', 1)[1]
        parsed = urlsplit(remote)
        url = 'https://github.com/' + parsed.path.strip('/') if parsed.hostname == 'github.com' else ''
        details.update(branch=branch, git_commit=commit, git_tag=tags[0] if tags else '', repo_url=url)
    return versions
