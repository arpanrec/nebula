# Ansible Role: KDE (arpanrec.utilities.kde)

Install [konsave](https://github.com/Prayag2/konsave) and upload [sweet-kde](https://github.com/EliverLara/Sweet-kde), [KDE Nordic](https://github.com/EliverLara/Nordic-kde)

## Variables

- Not Applicable

## Example Playbook KDE Konsave Profiles

```yaml
- name: Include KDE
  ansible.builtin.import_role:
    name: arpanrec.utilities.kde
```

## Testing KDE Konsave Profiles

```bash
molecule test -s role.kde.default
```
