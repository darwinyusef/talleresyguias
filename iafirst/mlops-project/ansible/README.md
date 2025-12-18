# Ansible Deployment para MLOps Platform

Automatización completa del deployment de la plataforma MLOps usando Ansible.

## 📁 Estructura

```
ansible/
├── ansible.cfg                    # Configuración de Ansible
├── inventories/
│   ├── production/
│   │   └── hosts.ini             # Servidores de producción
│   └── staging/
│       └── hosts.ini             # Servidores de staging
├── playbooks/
│   ├── deploy_mlops.yml          # Deploy principal
│   └── setup_gpu.yml             # Setup de GPU servers
└── roles/
    ├── common/                    # Tareas comunes
    ├── docker/                    # Instalación Docker
    └── mlops/                     # Deploy MLOps platform
```

## 🚀 Quick Start

### 1. Instalar Ansible

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install ansible -y

# macOS
brew install ansible

# Python pip
pip install ansible
```

### 2. Configurar Inventario

Edita el archivo de hosts según tu entorno:

```bash
# Production
vim inventories/production/hosts.ini

# Staging
vim inventories/staging/hosts.ini
```

**Ejemplo de configuración:**

```ini
[mlops_servers]
mlops-prod-01 ansible_host=10.0.1.10 ansible_user=ubuntu

[gpu_servers]
mlops-gpu-01 ansible_host=10.0.2.10 ansible_user=ubuntu

[mlops:vars]
ansible_python_interpreter=/usr/bin/python3
```

### 3. Verificar Conectividad

```bash
# Ping a todos los hosts
ansible all -m ping

# Verificar conectividad a producción
ansible -i inventories/production/hosts.ini all -m ping

# Verificar staging
ansible -i inventories/staging/hosts.ini all -m ping
```

## 📖 Playbooks Disponibles

### Deploy MLOps Platform

```bash
# Deploy a producción
ansible-playbook -i inventories/production/hosts.ini playbooks/deploy_mlops.yml

# Deploy a staging
ansible-playbook -i inventories/staging/hosts.ini playbooks/deploy_mlops.yml

# Dry run (check mode)
ansible-playbook playbooks/deploy_mlops.yml --check

# Verbose output
ansible-playbook playbooks/deploy_mlops.yml -vvv
```

### Setup GPU Servers

```bash
# Setup GPU drivers y NVIDIA Docker
ansible-playbook -i inventories/production/hosts.ini playbooks/setup_gpu.yml

# Solo para hosts específicos
ansible-playbook playbooks/setup_gpu.yml --limit mlops-gpu-01
```

## 🎯 Roles

### Role: common

Instala paquetes básicos y configura el sistema.

**Tareas:**
- Actualizar paquetes del sistema
- Instalar herramientas comunes (curl, git, vim, etc.)
- Crear directorios del proyecto
- Configurar firewall (UFW)

### Role: docker

Instala y configura Docker + Docker Compose.

**Tareas:**
- Remover instalaciones antiguas de Docker
- Añadir repositorio oficial de Docker
- Instalar Docker CE y plugins
- Configurar daemon de Docker
- Añadir usuario al grupo docker

### Role: mlops

Despliega la plataforma MLOps.

**Tareas:**
- Clonar/actualizar repositorio
- Configurar archivos .env
- Crear directorios necesarios
- Pull de imágenes Docker
- Build de imágenes custom
- Iniciar servicios con docker-compose

## 🔧 Variables

### Variables Globales

Definidas en `inventories/<env>/hosts.ini`:

```ini
[mlops:vars]
ansible_python_interpreter=/usr/bin/python3
docker_compose_version=2.23.0
nvidia_driver_version=535
project_dir=/opt/mlops
environment=production
```

### Variables de Playbook

Puedes pasar variables al ejecutar:

```bash
ansible-playbook playbooks/deploy_mlops.yml \
  -e "git_branch=develop" \
  -e "project_dir=/opt/mlops-staging"
```

## 📝 Comandos Útiles

### Ad-hoc Commands

```bash
# Ejecutar comando en todos los hosts
ansible all -a "uptime"

# Verificar espacio en disco
ansible mlops_servers -m shell -a "df -h"

# Verificar servicios Docker
ansible all -a "docker ps"

# Reiniciar servicio Docker
ansible all -m systemd -a "name=docker state=restarted" --become

# Obtener facts del sistema
ansible mlops_servers -m setup

# Copiar archivo a todos los hosts
ansible all -m copy -a "src=/local/file dest=/remote/file"
```

### Gestión de Servicios

```bash
# Detener servicios MLOps
ansible mlops_servers -m shell -a "cd /opt/mlops && docker compose down" --become

# Iniciar servicios
ansible mlops_servers -m shell -a "cd /opt/mlops && docker compose up -d" --become

# Ver logs
ansible mlops_servers -m shell -a "cd /opt/mlops && docker compose logs --tail=50"

# Reiniciar servicio específico
ansible mlops_servers -m shell -a "cd /opt/mlops && docker compose restart pytorch-service"
```

### Debugging

```bash
# Verificar qué tareas se ejecutarían
ansible-playbook playbooks/deploy_mlops.yml --list-tasks

# Ver variables disponibles para un host
ansible mlops-prod-01 -m debug -a "var=hostvars[inventory_hostname]"

# Ejecutar solo tags específicos
ansible-playbook playbooks/deploy_mlops.yml --tags docker

# Skip tags
ansible-playbook playbooks/deploy_mlops.yml --skip-tags gpu
```

## 🎨 Customización

### Añadir Nuevo Rol

```bash
# Crear estructura de rol
ansible-galaxy init roles/monitoring

# Estructura generada:
roles/monitoring/
├── tasks/
│   └── main.yml
├── handlers/
│   └── main.yml
├── templates/
├── files/
├── vars/
│   └── main.yml
└── defaults/
    └── main.yml
```

### Crear Playbook Custom

```yaml
# playbooks/custom_deploy.yml
---
- name: Custom Deployment
  hosts: mlops_servers
  become: yes

  vars:
    custom_var: "value"

  tasks:
    - name: Custom task
      debug:
        msg: "Executing custom task"

    - import_role:
        name: common

    - import_role:
        name: mlops
```

## 🔐 Seguridad

### Usar Ansible Vault

```bash
# Crear archivo encriptado
ansible-vault create secrets.yml

# Editar archivo encriptado
ansible-vault edit secrets.yml

# Encriptar archivo existente
ansible-vault encrypt vars.yml

# Ejecutar playbook con vault
ansible-playbook playbooks/deploy_mlops.yml --ask-vault-pass

# Usar archivo de password
echo "mypassword" > .vault_pass
ansible-playbook playbooks/deploy_mlops.yml --vault-password-file .vault_pass
```

### SSH Keys

```bash
# Generar par de llaves
ssh-keygen -t ed25519 -C "ansible@mlops"

# Copiar llave pública a hosts
ssh-copy-id -i ~/.ssh/id_ed25519.pub ubuntu@10.0.1.10

# Probar conexión
ssh -i ~/.ssh/id_ed25519 ubuntu@10.0.1.10
```

## 📊 Monitoring del Deployment

### Verificar Estado Post-Deployment

```bash
# Verificar todos los contenedores
ansible mlops_servers -m shell -a "docker ps --format 'table {{.Names}}\t{{.Status}}'"

# Verificar salud de servicios
ansible mlops_servers -m shell -a "curl -f http://localhost:8000/health"

# Verificar logs de errores
ansible mlops_servers -m shell -a "docker compose logs --tail=100 | grep ERROR"
```

## 🐛 Troubleshooting

### Problemas Comunes

**1. Error de conexión SSH:**
```bash
# Verificar conectividad
ansible all -m ping -vvv

# Verificar llaves SSH
ssh-add -l

# Agregar llave si es necesario
ssh-add ~/.ssh/id_ed25519
```

**2. Error de permisos:**
```bash
# Ejecutar con sudo
ansible-playbook playbooks/deploy_mlops.yml --become --ask-become-pass
```

**3. Python no encontrado:**
```ini
# Agregar a hosts.ini
[mlops:vars]
ansible_python_interpreter=/usr/bin/python3
```

**4. Docker compose no funciona:**
```bash
# Verificar instalación
ansible all -m shell -a "docker compose version"

# Reinstalar si es necesario
ansible-playbook playbooks/deploy_mlops.yml --tags docker
```

## 📚 Recursos Adicionales

- [Ansible Documentation](https://docs.ansible.com/)
- [Ansible Galaxy](https://galaxy.ansible.com/)
- [Best Practices](https://docs.ansible.com/ansible/latest/user_guide/playbooks_best_practices.html)

## 🎯 Próximos Pasos

1. **Configurar inventarios** para tus servidores
2. **Ejecutar playbook** de deployment
3. **Verificar servicios** estén corriendo
4. **Configurar monitoring** con Prometheus/Grafana
5. **Setup CI/CD** para deployments automáticos

---

**¡Deployment automatizado exitoso! 🚀**
