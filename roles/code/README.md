# Ansible Role: Microsoft Visual Studio Code (arpanrec.utilities.code)

Install vscode, and extensions Also creates a soft link to the `code` executable in `{{ code_rv_bin_dir }}`

## Variables

```yaml
options:
  code_rv_tmp_dir:
    description: Tarball download location.
    required: false
    type: str
    default: "{{ ansible_facts.user_dir }}/.tmp/code"
  code_rv_bin_dir:
    description:
      - Code executable directory,.
      - This path expected to be in ${PATH}.
    required: false
    type: str
    default: "{{ ansible_facts.user_dir }}/.local/bin"
  code_rv_install_path:
    description: Install Path.
    required: false
    type: str
    default: "{{ ansible_facts.user_dir }}/.local/share/vscode"
  code_rv_xdg_icon_dir:
    description: XDG icon directory.
    required: false
    type: str
    default: "{{ ansible_facts.user_dir }}/.local/share/applications"
  code_rv_version:
    description: Version of [Microsoft Visual Studio Code](https://code.visualstudio.com/updates).
    required: false
    type: str
    default: Dynamically find the [latest tag_name](https://api.github.com/repos/microsoft/vscode/releases/latest), like `1.64.2`.
  code_rv_ext_to_be_installed:
    description: List of VSCode extension to be installed.
    required: false
    type: list[str]
    default:
      - "Angular.ng-template"
      - "DavidAnson.vscode-markdownlint"
      - "dhruv.maven-dependency-explorer"
      - "esbenp.prettier-vscode"
      - "foxundermoon.shell-format"
      - "GitHub.github-vscode-theme"
      - "GitHub.vscode-pull-request-github"
      - "golang.go"
      - "hashicorp.terraform"
      - "johnpapa.Angular2"
      - "ms-azuretools.vscode-docker"
      - "ms-python.isort"
      - "ms-python.python"
      - "ms-python.vscode-pylance"
      - "ms-toolsai.jupyter"
      - "ms-toolsai.jupyter-keymap"
      - "ms-toolsai.jupyter-renderers"
      - "ms-toolsai.vscode-jupyter-cell-tags"
      - "ms-toolsai.vscode-jupyter-slideshow"
      - "ms-vscode-remote.remote-containers"
      - "ms-vscode-remote.remote-ssh"
      - "ms-vscode-remote.remote-ssh-edit"
      - "ms-vscode-remote.remote-wsl"
      - "ms-vscode-remote.vscode-remote-extensionpack"
      - "ms-vscode.remote-explorer"
      - "PKief.material-icon-theme"
      - "redhat.ansible"
      - "redhat.fabric8-analytics"
      - "redhat.java"
      - "redhat.vscode-xml"
      - "redhat.vscode-yaml"
      - "shengchen.vscode-checkstyle"
      - "streetsidesoftware.code-spell-checker"
      - "timonwong.shellcheck"
      - "VisualStudioExptTeam.intellicode-api-usage-examples"
      - "VisualStudioExptTeam.vscodeintellicode"
      - "VisualStudioExptTeam.vscodeintellicode-completions"
      - "vmware.vscode-boot-dev-pack"
      - "vmware.vscode-spring-boot"
      - "vscjava.vscode-gradle"
      - "vscjava.vscode-java-debug"
      - "vscjava.vscode-java-dependency"
      - "vscjava.vscode-java-pack"
      - "vscjava.vscode-java-test"
      - "vscjava.vscode-maven"
      - "vscjava.vscode-spring-boot-dashboard"
      - "vscjava.vscode-spring-initializr"
      - "wholroyd.jinja"
      - "yzhang.markdown-all-in-one"

```

## Example Playbook Visual Studio Code

```yaml
---
- name: Visual Studio Code
  hosts: all
  gather_facts: false
  become: false
  any_errors_fatal: true
  roles:
    - name: arpanrec.utilities.code
```

## Testing Visual Studio Code

```bash
molecule test -s role.code.default
```
