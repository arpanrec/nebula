# Ansible Role: Server Workspace (arpanrec.utilities.server_workspace)

## Oracle Java

Install oracle jdk in user space

## Variables

```yaml
options:
  java_rv_jdk_tmp_dir:
    description: Temporary directory.
    required: false
    type: str
    default: "{{ ansible_facts.user_dir }}/.tmp/java"
  java_rv_jdk_install_path:
    description: Install path for java.
    required: false
    type: str
    default: "{{ pv_ua_user_share_dir }}/java"
  java_rv_jdk_version:
    description: Major Java Release version
    required: false
    type: int
    default: 17
  java_rv_jdk_mvn_install_path:
    description: Install Path.
    required: false
    type: str
    default: "{{ pv_ua_user_share_dir }}/maven"
  java_rv_jdk_mvn_version:
    description:
      - Exact release version of maven.
      - By default it will be latest release version from [Github](https://api.github.com/repos/apache/maven/releases/latest)
      - Example format `3.9.4`
    required: false
    type: str
  java_rv_jdk_gradle_version:
    description:
      - Release version of Gradle from https://gradle.org/releases/.
      - Default Get latest release name from [github](https://api.github.com/repos/gradle/gradle/releases/latest)
      - Example format `7.3.3`
    required: false
    type: str
  java_rv_jdk_groovy_version:
    description: Release version of Groovy from https://groovy.apache.org/download.html.
    required: false
    type: str
    default: 4.0.2
  java_rv_jdk_kotlinc_version:
    description:
      - Release version of Kotlin from github
      - Default Get latest release name from [github](https://api.github.com/repos/JetBrains/kotlin/releases/latest)
      - Example format `1.5.31`
    required: false
    type: str
  java_rv_jdk_graalvm_install_path:
    description: Install Path for [GraalVM](https://www.graalvm.org/).
    required: false
    type: str
    default: "{{ ansible_facts.user_dir }}/.local/share/graalvm"
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
