# Ansible Role: Server Workspace (arpanrec.utilities.server_workspace)

## Oracle Java

Install oracle jdk in user space

## Variables

```yaml
options:
  rv_jdk_tmp_dir:
    description: Temporary directory.
    required: false
    type: str
    default: "{{ ansible_facts.user_dir }}/.tmp/java"
  rv_jdk_install_path:
    description: Install path for java.
    required: false
    type: str
    default: "{{ pv_ua_user_share_dir }}/java"
  rv_jdk_version:
    description: Major Java Release version
    required: false
    type: int
    default: 17
  rv_jdk_mvn_install_path:
    description: Install Path.
    required: false
    type: str
    default: "{{ pv_ua_user_share_dir }}/maven"
  rv_jdk_mvn_version:
    description: Exact release version of maven.
    required: false
    type: str
    default: 3.8.6
  rv_jdk_gradle_version:
    description: Release version of Gradle from https://gradle.org/releases/.
    required: false
    type: str
    default: 7.5.1
```

## Example Playbook Oracle Java

```yaml
- name: Oracle JDK
  hosts: all
  gather_facts: false
  become: false
  any_errors_fatal: true
  roles:
    - name: arpanrec.utilities.java
```

## Testing Oracle Java

```bash
molecule test -s role.java.default
```
