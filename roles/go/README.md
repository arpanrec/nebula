# Ansible Role: GoLang (arpanrec.utilities.go)

## Go Language

Install Go Language in user space

## Variables Go Language

```yaml
options:
  rv_golang_install_path:
    description: Install path for Go.
    required: false
    type: str
    default: "{{ ansible_facts.user_dir }}/.local/share/go"
  rv_golang_version:
    description: Exact release version of go language.
    required: false
    type: str
    default: 1.20.4
  rv_golang_tmp_dir:
    description: Temporary cache directory for install.
    required: false
    type: str
    default: "{{ ansible_facts.user_dir }}/.tmp/go"
```

## Example Playbook Go Language

```yaml
---
- name: Golang
  hosts: all
  gather_facts: false
  become: false
  any_errors_fatal: true
  roles:
    - name: arpanrec.utilities.go
```

## Testing Go Language

```bash
molecule test -s role.go.default
```
