# Ansible Role: Microsoft Visual Studio Code (arpanrec.utilities.code)

Install vscode, and extensions Also creates a soft link to the `code` executable in `{{ rv_code_bin_dir }}`

## Variables

```yaml
options:
  rv_code_tmp_dir:
    description: Tarball download location.
    required: false
    type: str
    default: "{{ ansible_facts.user_dir }}/.tmp/code"
  rv_code_bin_dir:
    description:
      - Code executable directory,.
      - This path expected to be in ${PATH}.
    required: false
    type: str
    default: "{{ ansible_facts.user_dir }}/.local/bin"
  rv_code_install_path:
    description: Install Path.
    required: false
    type: str
    default: "{{ ansible_facts.user_dir }}/.local/share/vscode"
  rv_code_xdg_icon_dir:
    description: XDG icon directory.
    required: false
    type: str
    default: "{{ ansible_facts.user_dir }}/.local/share/applications"
  rv_code_version:
    description: Version of [Microsoft Visual Studio Code](https://code.visualstudio.com/updates).
    required: false
    type: str
    default: Dynamically find the [latest tag_name](https://api.github.com/repos/microsoft/vscode/releases/latest), like `1.64.2`.
  rv_code_ext_to_be_installed:
    description: List of VSCode extension to be installed.
    required: false
    type: list[str]
    default:
      - "akamud.vscode-theme-onedark"
      - "Angular.ng-template"
      - "bbenoist.shell"
      - "ceciljacob.code-plus-theme"
      - "DavidAnson.vscode-markdownlint"
      - "dracula-theme.theme-dracula"
      - "foxundermoon.shell-format"
      # - "GabrielBB.vscode-lombok"
      - "GitHub.github-vscode-theme"
      - "golang.go"
      - "hashicorp.terraform"
      - "johnpapa.Angular2"
      - "johnpapa.winteriscoming"
      # - "ms-azuretools.vscode-docker"
      # - "ms-kubernetes-tools.vscode-kubernetes-tools"
      - "ms-python.python"
      - "ms-python.vscode-pylance"
      - "ms-toolsai.jupyter"
      - "ms-toolsai.jupyter-keymap"
      - "ms-toolsai.jupyter-renderers"
      - "ms-vscode-remote.vscode-remote-extensionpack"
      - "ms-vscode-remote.remote-containers"
      - "ms-vscode-remote.remote-ssh"
      - "ms-vscode-remote.remote-ssh-edit"
      - "ms-vscode-remote.remote-wsl"
      - "vscjava.vscode-java-pack"
      - "Pivotal.vscode-boot-dev-pack"
      - "Pivotal.vscode-spring-boot"
      - "PKief.material-icon-theme"
      - "redhat.ansible"
      - "redhat.fabric8-analytics"
      - "redhat.java"
      - "redhat.vscode-xml"
      - "redhat.vscode-yaml"
      - "shengchen.vscode-checkstyle"
      - "timonwong.shellcheck"
      - "Tyriar.shell-launcher"
      - "VisualStudioExptTeam.vscodeintellicode"
      - "VisualStudioExptTeam.vscodeintellicode-completions"
      - "vscjava.vscode-gradle"
      - "vscjava.vscode-java-debug"
      - "vscjava.vscode-java-dependency"
      - "vscjava.vscode-java-test"
      - "vscjava.vscode-maven"
      - "vscjava.vscode-spring-boot-dashboard"
      - "vscjava.vscode-spring-initializr"
      - "streetsidesoftware.code-spell-checker"
      - "dhruv.maven-dependency-explorer"
      - "yzhang.markdown-all-in-one"
      - "zhuangtongfa.material-theme"
      - "Trunk.io"
      - "wholroyd.jinja"
      - "esbenp.prettier-vscode"
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
