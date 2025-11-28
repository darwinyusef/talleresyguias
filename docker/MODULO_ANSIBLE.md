# Módulo: Ansible - Automatización de Configuración

## Objetivo
Aprender a automatizar la configuración de servidores, despliegue de Docker y gestión de infraestructura usando Ansible.

---

## ¿Qué es Ansible?

**Ansible** es una herramienta de automatización de TI que permite:
- Configuración de servidores
- Despliegue de aplicaciones
- Orquestación de tareas
- Gestión de configuración

### Características
- ✅ **Agentless**: No requiere agentes en servidores remotos
- ✅ **SSH**: Usa SSH para conexión
- ✅ **YAML**: Sintaxis simple y legible
- ✅ **Idempotente**: Ejecutar múltiples veces = mismo resultado
- ✅ **Modular**: Gran ecosistema de módulos

---

## Parte 1: Instalación y Configuración

### Instalación

**macOS:**
```bash
brew install ansible
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install ansible -y
```

**Python (cualquier OS):**
```bash
pip install ansible
```

**Verificar:**
```bash
ansible --version
```

### Estructura de Proyecto Ansible

```
ansible-project/
├── ansible.cfg              # Configuración de Ansible
├── inventory/               # Inventarios
│   ├── production/
│   │   ├── hosts.yml
│   │   └── group_vars/
│   │       ├── all.yml
│   │       └── webservers.yml
│   └── staging/
│       └── hosts.yml
├── playbooks/               # Playbooks principales
│   ├── setup-docker.yml
│   ├── deploy-app.yml
│   └── site.yml
├── roles/                   # Roles reutilizables
│   ├── common/
│   ├── docker/
│   ├── nginx/
│   └── postgres/
├── group_vars/              # Variables por grupo
├── host_vars/               # Variables por host
└── files/                   # Archivos estáticos
```

---

## Parte 2: Inventario (Inventory)

### inventory/production/hosts.yml
```yaml
all:
  children:
    webservers:
      hosts:
        web1:
          ansible_host: 192.168.1.10
          ansible_user: ubuntu
        web2:
          ansible_host: 192.168.1.11
          ansible_user: ubuntu

    databases:
      hosts:
        db1:
          ansible_host: 192.168.1.20
          ansible_user: ubuntu

    loadbalancers:
      hosts:
        lb1:
          ansible_host: 192.168.1.30
          ansible_user: ubuntu

  vars:
    ansible_python_interpreter: /usr/bin/python3
    ansible_ssh_private_key_file: ~/.ssh/id_rsa
```

### Inventario dinámico (AWS)
```yaml
# aws_ec2.yml
plugin: aws_ec2
regions:
  - us-east-1
filters:
  tag:Environment: production
  instance-state-name: running
keyed_groups:
  - key: tags.Role
    prefix: role
```

---

## Parte 3: Configuración Ansible

### ansible.cfg
```ini
[defaults]
inventory = inventory/production/hosts.yml
remote_user = ubuntu
private_key_file = ~/.ssh/id_rsa
host_key_checking = False
roles_path = ./roles
retry_files_enabled = False
gathering = smart
fact_caching = jsonfile
fact_caching_connection = /tmp/ansible_facts
fact_caching_timeout = 86400

[privilege_escalation]
become = True
become_method = sudo
become_user = root
become_ask_pass = False

[ssh_connection]
pipelining = True
control_path = /tmp/ansible-ssh-%%h-%%p-%%r
```

---

## Parte 4: Playbooks Básicos

### playbooks/ping.yml
```yaml
---
- name: Test connectivity
  hosts: all
  tasks:
    - name: Ping hosts
      ansible.builtin.ping:

    - name: Print message
      ansible.builtin.debug:
        msg: "Hello from {{ inventory_hostname }}"
```

**Ejecutar:**
```bash
ansible-playbook playbooks/ping.yml
```

### playbooks/setup-docker.yml
```yaml
---
- name: Install and configure Docker
  hosts: webservers
  become: yes

  vars:
    docker_users:
      - ubuntu
      - deploy

  tasks:
    - name: Update apt cache
      ansible.builtin.apt:
        update_cache: yes
        cache_valid_time: 3600

    - name: Install prerequisites
      ansible.builtin.apt:
        name:
          - apt-transport-https
          - ca-certificates
          - curl
          - gnupg
          - lsb-release
        state: present

    - name: Add Docker GPG key
      ansible.builtin.apt_key:
        url: https://download.docker.com/linux/ubuntu/gpg
        state: present

    - name: Add Docker repository
      ansible.builtin.apt_repository:
        repo: "deb [arch=amd64] https://download.docker.com/linux/ubuntu {{ ansible_distribution_release }} stable"
        state: present

    - name: Install Docker
      ansible.builtin.apt:
        name:
          - docker-ce
          - docker-ce-cli
          - containerd.io
          - docker-compose-plugin
        state: present
        update_cache: yes

    - name: Start Docker service
      ansible.builtin.service:
        name: docker
        state: started
        enabled: yes

    - name: Add users to docker group
      ansible.builtin.user:
        name: "{{ item }}"
        groups: docker
        append: yes
      loop: "{{ docker_users }}"

    - name: Install Docker Python library
      ansible.builtin.pip:
        name:
          - docker
          - docker-compose
        state: present
```

---

## Parte 5: Roles (Reutilización)

### Crear un role
```bash
ansible-galaxy init roles/docker
```

### roles/docker/tasks/main.yml
```yaml
---
- name: Include OS-specific variables
  ansible.builtin.include_vars: "{{ ansible_os_family }}.yml"

- name: Install Docker prerequisites
  ansible.builtin.apt:
    name: "{{ docker_prerequisites }}"
    state: present
    update_cache: yes
  when: ansible_os_family == "Debian"

- name: Add Docker GPG key
  ansible.builtin.apt_key:
    url: "{{ docker_gpg_key_url }}"
    state: present

- name: Add Docker repository
  ansible.builtin.apt_repository:
    repo: "{{ docker_repository }}"
    state: present

- name: Install Docker
  ansible.builtin.apt:
    name: "{{ docker_packages }}"
    state: present
    update_cache: yes

- name: Ensure Docker is started and enabled
  ansible.builtin.service:
    name: docker
    state: started
    enabled: yes

- name: Add users to docker group
  ansible.builtin.user:
    name: "{{ item }}"
    groups: docker
    append: yes
  loop: "{{ docker_users }}"
```

### roles/docker/defaults/main.yml
```yaml
---
docker_users:
  - ubuntu

docker_packages:
  - docker-ce
  - docker-ce-cli
  - containerd.io
  - docker-compose-plugin

docker_prerequisites:
  - apt-transport-https
  - ca-certificates
  - curl
  - gnupg
  - lsb-release

docker_gpg_key_url: https://download.docker.com/linux/ubuntu/gpg
docker_repository: "deb [arch=amd64] https://download.docker.com/linux/ubuntu {{ ansible_distribution_release }} stable"
```

### Usar el role

```yaml
---
- name: Setup Docker hosts
  hosts: webservers
  become: yes

  roles:
    - docker
```

---

## Parte 6: Desplegar Aplicación Docker

### playbooks/deploy-app.yml
```yaml
---
- name: Deploy Docker application
  hosts: webservers
  become: yes

  vars:
    app_name: myapp
    app_image: "{{ docker_registry }}/{{ app_name }}:{{ app_version }}"
    app_port: 3000
    docker_registry: docker.io/myuser
    app_version: latest

  tasks:
    - name: Pull Docker image
      community.docker.docker_image:
        name: "{{ app_image }}"
        source: pull

    - name: Stop old container
      community.docker.docker_container:
        name: "{{ app_name }}"
        state: stopped
      ignore_errors: yes

    - name: Remove old container
      community.docker.docker_container:
        name: "{{ app_name }}"
        state: absent
      ignore_errors: yes

    - name: Run new container
      community.docker.docker_container:
        name: "{{ app_name }}"
        image: "{{ app_image }}"
        state: started
        restart_policy: unless-stopped
        ports:
          - "{{ app_port }}:3000"
        env:
          NODE_ENV: production
          DATABASE_URL: "{{ database_url }}"
        networks:
          - name: app-network

    - name: Wait for application to be ready
      ansible.builtin.uri:
        url: "http://localhost:{{ app_port }}/health"
        status_code: 200
      register: result
      until: result.status == 200
      retries: 12
      delay: 5
```

---

## Parte 7: Docker Compose con Ansible

### playbooks/deploy-compose.yml
```yaml
---
- name: Deploy with Docker Compose
  hosts: webservers
  become: yes

  vars:
    project_dir: /opt/myapp
    compose_file: docker-compose.yml

  tasks:
    - name: Create project directory
      ansible.builtin.file:
        path: "{{ project_dir }}"
        state: directory
        owner: ubuntu
        group: ubuntu
        mode: '0755'

    - name: Copy docker-compose.yml
      ansible.builtin.template:
        src: templates/docker-compose.yml.j2
        dest: "{{ project_dir }}/{{ compose_file }}"
        owner: ubuntu
        group: ubuntu
        mode: '0644'

    - name: Copy .env file
      ansible.builtin.template:
        src: templates/.env.j2
        dest: "{{ project_dir }}/.env"
        owner: ubuntu
        group: ubuntu
        mode: '0600'

    - name: Pull images
      community.docker.docker_compose:
        project_src: "{{ project_dir }}"
        files:
          - "{{ compose_file }}"
        pull: yes
      register: output

    - name: Start services
      community.docker.docker_compose:
        project_src: "{{ project_dir }}"
        files:
          - "{{ compose_file }}"
        state: present
        restarted: yes

    - name: Check running containers
      ansible.builtin.command: docker compose ps
      args:
        chdir: "{{ project_dir }}"
      register: compose_ps

    - name: Display running containers
      ansible.builtin.debug:
        var: compose_ps.stdout_lines
```

### templates/docker-compose.yml.j2
```yaml
version: '3.8'

services:
  app:
    image: {{ app_image }}
    container_name: {{ app_name }}
    restart: unless-stopped
    ports:
      - "{{ app_port }}:3000"
    environment:
      NODE_ENV: {{ node_env }}
      DATABASE_URL: {{ database_url }}
    networks:
      - app-network

  nginx:
    image: nginx:alpine
    container_name: nginx
    restart: unless-stopped
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - app
    networks:
      - app-network

networks:
  app-network:
    driver: bridge
```

---

## Parte 8: Configurar Nginx

### playbooks/setup-nginx.yml
```yaml
---
- name: Configure Nginx
  hosts: loadbalancers
  become: yes

  tasks:
    - name: Install Nginx
      ansible.builtin.apt:
        name: nginx
        state: present
        update_cache: yes

    - name: Copy Nginx configuration
      ansible.builtin.template:
        src: templates/nginx.conf.j2
        dest: /etc/nginx/sites-available/{{ app_name }}
        mode: '0644'
      notify: Reload Nginx

    - name: Enable site
      ansible.builtin.file:
        src: /etc/nginx/sites-available/{{ app_name }}
        dest: /etc/nginx/sites-enabled/{{ app_name }}
        state: link
      notify: Reload Nginx

    - name: Remove default site
      ansible.builtin.file:
        path: /etc/nginx/sites-enabled/default
        state: absent
      notify: Reload Nginx

    - name: Test Nginx configuration
      ansible.builtin.command: nginx -t
      register: nginx_test
      changed_when: false

    - name: Display test result
      ansible.builtin.debug:
        var: nginx_test.stderr_lines

  handlers:
    - name: Reload Nginx
      ansible.builtin.service:
        name: nginx
        state: reloaded
```

---

## Parte 9: Gestión de Secretos con Ansible Vault

### Encriptar archivo
```bash
# Crear archivo encriptado
ansible-vault create secrets.yml

# Editar archivo encriptado
ansible-vault edit secrets.yml

# Encriptar archivo existente
ansible-vault encrypt vars.yml

# Desencriptar
ansible-vault decrypt vars.yml

# Ver contenido
ansible-vault view secrets.yml
```

### secrets.yml
```yaml
---
database_password: super_secret_password
api_key: abc123xyz456
```

### Usar en playbook
```yaml
---
- name: Deploy with secrets
  hosts: webservers
  become: yes

  vars_files:
    - secrets.yml

  tasks:
    - name: Deploy app with secret
      community.docker.docker_container:
        name: myapp
        image: myapp:latest
        env:
          DB_PASSWORD: "{{ database_password }}"
          API_KEY: "{{ api_key }}"
```

**Ejecutar con vault:**
```bash
ansible-playbook playbooks/deploy-app.yml --ask-vault-pass

# O con archivo de password
echo "mi-password" > .vault_pass
ansible-playbook playbooks/deploy-app.yml --vault-password-file .vault_pass
```

---

## Parte 10: Handlers y Notificaciones

```yaml
---
- name: Example with handlers
  hosts: webservers
  become: yes

  tasks:
    - name: Copy nginx config
      ansible.builtin.template:
        src: nginx.conf.j2
        dest: /etc/nginx/nginx.conf
      notify:
        - Reload Nginx
        - Send notification

    - name: Copy app config
      ansible.builtin.copy:
        src: app.conf
        dest: /etc/myapp/config.conf
      notify: Restart App

  handlers:
    - name: Reload Nginx
      ansible.builtin.service:
        name: nginx
        state: reloaded

    - name: Restart App
      community.docker.docker_container:
        name: myapp
        state: started
        restart: yes

    - name: Send notification
      ansible.builtin.debug:
        msg: "Nginx configuration updated on {{ inventory_hostname }}"
```

---

## Parte 11: Loops y Condiciones

```yaml
---
- name: Advanced tasks
  hosts: all
  become: yes

  tasks:
    - name: Install multiple packages
      ansible.builtin.apt:
        name: "{{ item }}"
        state: present
      loop:
        - git
        - curl
        - vim
        - htop

    - name: Create multiple users
      ansible.builtin.user:
        name: "{{ item.name }}"
        groups: "{{ item.groups }}"
        state: present
      loop:
        - { name: 'alice', groups: 'sudo,docker' }
        - { name: 'bob', groups: 'docker' }

    - name: Install Docker only on Ubuntu
      ansible.builtin.apt:
        name: docker.io
        state: present
      when: ansible_distribution == "Ubuntu"

    - name: Configure firewall on production
      ansible.builtin.ufw:
        rule: allow
        port: '80'
        proto: tcp
      when: environment == "production"
```

---

## Parte 12: Tags

```yaml
---
- name: Full deployment
  hosts: webservers
  become: yes

  tasks:
    - name: Install Docker
      ansible.builtin.apt:
        name: docker.io
        state: present
      tags:
        - docker
        - install

    - name: Deploy application
      community.docker.docker_container:
        name: myapp
        image: myapp:latest
        state: started
      tags:
        - deploy
        - app

    - name: Configure Nginx
      ansible.builtin.template:
        src: nginx.conf.j2
        dest: /etc/nginx/nginx.conf
      tags:
        - nginx
        - config
```

**Ejecutar con tags:**
```bash
# Solo tareas con tag 'deploy'
ansible-playbook deploy.yml --tags deploy

# Omitir tags específicos
ansible-playbook deploy.yml --skip-tags install

# Múltiples tags
ansible-playbook deploy.yml --tags "docker,app"
```

---

## Parte 13: Comandos Ad-Hoc

```bash
# Ping todos los hosts
ansible all -m ping

# Ejecutar comando
ansible webservers -m command -a "uptime"

# Shell command
ansible all -m shell -a "df -h | grep /dev"

# Copiar archivo
ansible webservers -m copy -a "src=/local/file dest=/remote/file"

# Instalar paquete
ansible all -m apt -a "name=vim state=present" --become

# Reiniciar servicio
ansible webservers -m service -a "name=nginx state=restarted" --become

# Gather facts
ansible all -m setup

# Filtrar facts
ansible all -m setup -a "filter=ansible_distribution*"
```

---

## Parte 14: Integración con CI/CD

### GitLab CI
```yaml
# .gitlab-ci.yml
stages:
  - deploy

deploy_production:
  stage: deploy
  image: willhallonline/ansible:latest
  before_script:
    - ansible --version
    - mkdir -p ~/.ssh
    - echo "$SSH_PRIVATE_KEY" > ~/.ssh/id_rsa
    - chmod 600 ~/.ssh/id_rsa
  script:
    - ansible-playbook -i inventory/production playbooks/deploy-app.yml --vault-password-file <(echo $VAULT_PASSWORD)
  only:
    - main
  environment:
    name: production
```

### GitHub Actions
```yaml
# .github/workflows/deploy.yml
name: Deploy with Ansible

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Setup SSH
        run: |
          mkdir -p ~/.ssh
          echo "${{ secrets.SSH_PRIVATE_KEY }}" > ~/.ssh/id_rsa
          chmod 600 ~/.ssh/id_rsa

      - name: Install Ansible
        run: |
          sudo apt update
          sudo apt install ansible -y

      - name: Run playbook
        env:
          VAULT_PASSWORD: ${{ secrets.VAULT_PASSWORD }}
        run: |
          echo "$VAULT_PASSWORD" > .vault_pass
          ansible-playbook -i inventory/production playbooks/deploy-app.yml --vault-password-file .vault_pass
```

---

## Comandos Útiles

```bash
# Verificar sintaxis
ansible-playbook playbooks/deploy.yml --syntax-check

# Dry run (check mode)
ansible-playbook playbooks/deploy.yml --check

# Modo diff (mostrar cambios)
ansible-playbook playbooks/deploy.yml --check --diff

# Limitar a hosts específicos
ansible-playbook playbooks/deploy.yml --limit web1,web2

# Verbosidad
ansible-playbook playbooks/deploy.yml -v   # verbose
ansible-playbook playbooks/deploy.yml -vvv # más detalle

# Listar hosts
ansible all --list-hosts
ansible webservers --list-hosts

# Listar tareas
ansible-playbook playbooks/deploy.yml --list-tasks

# Listar tags
ansible-playbook playbooks/deploy.yml --list-tags

# Iniciar desde tarea específica
ansible-playbook playbooks/deploy.yml --start-at-task="Deploy application"
```

---

## Checklist de Ansible

- [ ] Instalar Ansible
- [ ] Crear inventario
- [ ] Configurar ansible.cfg
- [ ] Crear playbooks básicos
- [ ] Organizar en roles
- [ ] Usar variables y templates
- [ ] Implementar handlers
- [ ] Encriptar secretos con Vault
- [ ] Usar tags para organización
- [ ] Integrar con CI/CD
- [ ] Documentar playbooks
- [ ] Versionar en Git

---

¡Automatización completa con Ansible! 🤖
