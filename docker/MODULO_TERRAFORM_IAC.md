# Módulo: Terraform - Infrastructure as Code (IaC)

## Objetivo
Aprender a gestionar infraestructura cloud como código usando Terraform, automatizando el despliegue de aplicaciones Docker en AWS, Azure y Google Cloud.

---

## ¿Qué es Infrastructure as Code (IaC)?

**Infrastructure as Code** es la práctica de gestionar infraestructura mediante código declarativo en lugar de configuración manual.

### Beneficios
- ✅ **Reproducibilidad**: Misma infraestructura en dev, staging y prod
- ✅ **Versionado**: Control de cambios con Git
- ✅ **Automatización**: Menos errores humanos
- ✅ **Documentación**: El código documenta la infraestructura
- ✅ **Velocidad**: Despliegue en minutos, no horas

### Herramientas de IaC
- **Terraform** (HashiCorp) - Multi-cloud
- **AWS CloudFormation** - Solo AWS
- **Azure Resource Manager (ARM)** - Solo Azure
- **Pulumi** - Multi-cloud con lenguajes de programación

---

## Parte 1: Introducción a Terraform

### Instalación

**macOS:**
```bash
brew install terraform
```

**Linux:**
```bash
wget -O- https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
sudo apt update && sudo apt install terraform
```

**Verificar:**
```bash
terraform --version
```

### Conceptos Básicos

#### Proveedores (Providers)
Plugins que permiten interactuar con APIs cloud (AWS, Azure, GCP, etc.)

#### Recursos (Resources)
Componentes de infraestructura (EC2, VPC, Load Balancers, etc.)

#### Variables
Parámetros configurables

#### Outputs
Valores que Terraform exporta después del despliegue

#### Estado (State)
Archivo que mantiene el estado actual de la infraestructura

---

## Parte 2: Terraform con AWS

### Proyecto 1: EC2 + Docker con Terraform

#### Estructura del proyecto
```
terraform-aws-docker/
├── main.tf
├── variables.tf
├── outputs.tf
├── terraform.tfvars
├── user_data.sh
└── .gitignore
```

#### main.tf
```hcl
# Configurar proveedor AWS
terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# VPC
resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name        = "${var.project_name}-vpc"
    Environment = var.environment
  }
}

# Internet Gateway
resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name = "${var.project_name}-igw"
  }
}

# Subnet pública
resource "aws_subnet" "public" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.1.0/24"
  availability_zone       = "${var.aws_region}a"
  map_public_ip_on_launch = true

  tags = {
    Name = "${var.project_name}-public-subnet"
  }
}

# Route Table
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main.id
  }

  tags = {
    Name = "${var.project_name}-public-rt"
  }
}

# Route Table Association
resource "aws_route_table_association" "public" {
  subnet_id      = aws_subnet.public.id
  route_table_id = aws_route_table.public.id
}

# Security Group
resource "aws_security_group" "docker_app" {
  name        = "${var.project_name}-sg"
  description = "Security group for Docker application"
  vpc_id      = aws_vpc.main.id

  # SSH
  ingress {
    description = "SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = var.allowed_ssh_ips
  }

  # HTTP
  ingress {
    description = "HTTP"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # HTTPS
  ingress {
    description = "HTTPS"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Custom App Port
  ingress {
    description = "App Port"
    from_port   = var.app_port
    to_port     = var.app_port
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Egress all
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${var.project_name}-sg"
  }
}

# Key Pair
resource "aws_key_pair" "deployer" {
  key_name   = "${var.project_name}-key"
  public_key = file(var.ssh_public_key_path)
}

# EC2 Instance
resource "aws_instance" "docker_host" {
  ami                    = var.ami_id
  instance_type          = var.instance_type
  key_name               = aws_key_pair.deployer.key_name
  subnet_id              = aws_subnet.public.id
  vpc_security_group_ids = [aws_security_group.docker_app.id]

  user_data = file("user_data.sh")

  root_block_device {
    volume_size = 30
    volume_type = "gp3"
  }

  tags = {
    Name        = "${var.project_name}-docker-host"
    Environment = var.environment
  }
}

# Elastic IP
resource "aws_eip" "docker_host" {
  instance = aws_instance.docker_host.id
  domain   = "vpc"

  tags = {
    Name = "${var.project_name}-eip"
  }
}
```

#### variables.tf
```hcl
variable "aws_region" {
  description = "AWS Region"
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Project name for resource naming"
  type        = string
  default     = "docker-app"
}

variable "environment" {
  description = "Environment (dev, staging, prod)"
  type        = string
  default     = "dev"
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t3.micro"
}

variable "ami_id" {
  description = "AMI ID (Ubuntu 22.04 LTS)"
  type        = string
  default     = "ami-0c7217cdde317cfec" # Ubuntu 22.04 us-east-1
}

variable "ssh_public_key_path" {
  description = "Path to SSH public key"
  type        = string
  default     = "~/.ssh/id_rsa.pub"
}

variable "allowed_ssh_ips" {
  description = "IPs allowed to SSH"
  type        = list(string)
  default     = ["0.0.0.0/0"] # ⚠️ Cambiar en producción
}

variable "app_port" {
  description = "Application port"
  type        = number
  default     = 3000
}
```

#### outputs.tf
```hcl
output "instance_id" {
  description = "EC2 Instance ID"
  value       = aws_instance.docker_host.id
}

output "public_ip" {
  description = "Elastic IP"
  value       = aws_eip.docker_host.public_ip
}

output "public_dns" {
  description = "Public DNS"
  value       = aws_instance.docker_host.public_dns
}

output "ssh_command" {
  description = "SSH command to connect"
  value       = "ssh -i ~/.ssh/id_rsa ubuntu@${aws_eip.docker_host.public_ip}"
}

output "application_url" {
  description = "Application URL"
  value       = "http://${aws_eip.docker_host.public_ip}"
}
```

#### user_data.sh
```bash
#!/bin/bash
set -e

# Update system
apt-get update
apt-get upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Add ubuntu user to docker group
usermod -aG docker ubuntu

# Install Docker Compose
apt-get install -y docker-compose-plugin

# Enable Docker service
systemctl enable docker
systemctl start docker

# Create app directory
mkdir -p /home/ubuntu/app
chown ubuntu:ubuntu /home/ubuntu/app

# Install other tools
apt-get install -y git curl wget htop

# Pull and run your Docker image (ejemplo)
# docker run -d --name app -p 80:3000 tu-usuario/tu-app:latest

echo "Docker installation completed!" > /home/ubuntu/docker-ready.txt
```

#### terraform.tfvars
```hcl
aws_region      = "us-east-1"
project_name    = "mi-app"
environment     = "production"
instance_type   = "t3.small"
app_port        = 3000
allowed_ssh_ips = ["YOUR_IP/32"] # Cambia a tu IP
```

#### .gitignore
```
# Terraform
.terraform/
*.tfstate
*.tfstate.backup
*.tfvars
.terraform.lock.hcl

# SSH keys
*.pem
*.key
```

### Comandos Terraform

```bash
# Inicializar proyecto (descarga providers)
terraform init

# Validar sintaxis
terraform validate

# Ver plan de ejecución
terraform plan

# Aplicar cambios
terraform apply

# Aplicar sin confirmación
terraform apply -auto-approve

# Ver estado actual
terraform show

# Ver outputs
terraform output

# Destruir infraestructura
terraform destroy

# Formatear código
terraform fmt

# Importar recurso existente
terraform import aws_instance.docker_host i-1234567890abcdef0
```

---

## Parte 3: Terraform con Azure

### Proyecto 2: Azure Container Instances + ACR

#### main.tf (Azure)
```hcl
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}

provider "azurerm" {
  features {}
}

# Resource Group
resource "azurerm_resource_group" "main" {
  name     = "${var.project_name}-rg"
  location = var.location

  tags = {
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}

# Azure Container Registry
resource "azurerm_container_registry" "acr" {
  name                = "${var.project_name}acr${random_string.suffix.result}"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  sku                 = "Basic"
  admin_enabled       = true

  tags = {
    Environment = var.environment
  }
}

# Random suffix for unique names
resource "random_string" "suffix" {
  length  = 6
  special = false
  upper   = false
}

# Container Instance
resource "azurerm_container_group" "app" {
  name                = "${var.project_name}-container"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  os_type             = "Linux"
  dns_name_label      = "${var.project_name}-${random_string.suffix.result}"

  image_registry_credential {
    server   = azurerm_container_registry.acr.login_server
    username = azurerm_container_registry.acr.admin_username
    password = azurerm_container_registry.acr.admin_password
  }

  container {
    name   = "app"
    image  = "${azurerm_container_registry.acr.login_server}/app:latest"
    cpu    = "1"
    memory = "1.5"

    ports {
      port     = 80
      protocol = "TCP"
    }

    environment_variables = {
      NODE_ENV = var.environment
    }
  }

  tags = {
    Environment = var.environment
  }
}

# PostgreSQL Server
resource "azurerm_postgresql_flexible_server" "db" {
  name                   = "${var.project_name}-psql"
  resource_group_name    = azurerm_resource_group.main.name
  location               = azurerm_resource_group.main.location
  version                = "14"
  administrator_login    = var.db_admin_username
  administrator_password = var.db_admin_password
  storage_mb             = 32768
  sku_name               = "B_Standard_B1ms"

  tags = {
    Environment = var.environment
  }
}

# Database
resource "azurerm_postgresql_flexible_server_database" "appdb" {
  name      = var.database_name
  server_id = azurerm_postgresql_flexible_server.db.id
  charset   = "UTF8"
  collation = "en_US.utf8"
}
```

#### variables.tf (Azure)
```hcl
variable "project_name" {
  description = "Project name"
  type        = string
  default     = "myapp"
}

variable "location" {
  description = "Azure region"
  type        = string
  default     = "East US"
}

variable "environment" {
  description = "Environment"
  type        = string
  default     = "dev"
}

variable "db_admin_username" {
  description = "Database admin username"
  type        = string
  sensitive   = true
}

variable "db_admin_password" {
  description = "Database admin password"
  type        = string
  sensitive   = true
}

variable "database_name" {
  description = "Database name"
  type        = string
  default     = "appdb"
}
```

---

## Parte 4: Terraform Modules (Reutilización)

### Estructura de módulos
```
terraform-project/
├── modules/
│   ├── vpc/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   ├── ec2/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   └── rds/
│       ├── main.tf
│       ├── variables.tf
│       └── outputs.tf
├── environments/
│   ├── dev/
│   │   ├── main.tf
│   │   └── terraform.tfvars
│   ├── staging/
│   │   ├── main.tf
│   │   └── terraform.tfvars
│   └── prod/
│       ├── main.tf
│       └── terraform.tfvars
└── README.md
```

### Módulo VPC

#### modules/vpc/main.tf
```hcl
resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = merge(
    var.tags,
    {
      Name = "${var.name}-vpc"
    }
  )
}

resource "aws_subnet" "public" {
  count = length(var.public_subnet_cidrs)

  vpc_id                  = aws_vpc.main.id
  cidr_block              = var.public_subnet_cidrs[count.index]
  availability_zone       = var.availability_zones[count.index]
  map_public_ip_on_launch = true

  tags = merge(
    var.tags,
    {
      Name = "${var.name}-public-${count.index + 1}"
      Type = "public"
    }
  )
}

resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id

  tags = merge(
    var.tags,
    {
      Name = "${var.name}-igw"
    }
  )
}
```

#### modules/vpc/variables.tf
```hcl
variable "name" {
  description = "Name prefix for resources"
  type        = string
}

variable "vpc_cidr" {
  description = "VPC CIDR block"
  type        = string
}

variable "public_subnet_cidrs" {
  description = "Public subnet CIDRs"
  type        = list(string)
}

variable "availability_zones" {
  description = "Availability zones"
  type        = list(string)
}

variable "tags" {
  description = "Tags to apply to resources"
  type        = map(string)
  default     = {}
}
```

#### modules/vpc/outputs.tf
```hcl
output "vpc_id" {
  description = "VPC ID"
  value       = aws_vpc.main.id
}

output "public_subnet_ids" {
  description = "Public subnet IDs"
  value       = aws_subnet.public[*].id
}
```

### Usar el módulo

#### environments/prod/main.tf
```hcl
module "vpc" {
  source = "../../modules/vpc"

  name                 = "production"
  vpc_cidr             = "10.0.0.0/16"
  public_subnet_cidrs  = ["10.0.1.0/24", "10.0.2.0/24"]
  availability_zones   = ["us-east-1a", "us-east-1b"]

  tags = {
    Environment = "production"
    ManagedBy   = "Terraform"
  }
}

module "ec2" {
  source = "../../modules/ec2"

  name              = "production"
  vpc_id            = module.vpc.vpc_id
  subnet_id         = module.vpc.public_subnet_ids[0]
  instance_type     = "t3.medium"
  ami_id            = var.ami_id
  key_name          = var.key_name
}
```

---

## Parte 5: Remote State (S3 Backend)

### Configurar backend S3
```hcl
terraform {
  backend "s3" {
    bucket         = "mi-terraform-state-bucket"
    key            = "prod/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-locks"
  }
}
```

### Crear bucket y DynamoDB para locks

```hcl
# backend-setup.tf (ejecutar primero)
resource "aws_s3_bucket" "terraform_state" {
  bucket = "mi-terraform-state-bucket"

  lifecycle {
    prevent_destroy = true
  }
}

resource "aws_s3_bucket_versioning" "terraform_state" {
  bucket = aws_s3_bucket.terraform_state.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "terraform_state" {
  bucket = aws_s3_bucket.terraform_state.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_dynamodb_table" "terraform_locks" {
  name         = "terraform-locks"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "LockID"

  attribute {
    name = "LockID"
    type = "S"
  }
}
```

---

## Parte 6: Terraform con Kubernetes (EKS)

### main.tf (EKS simplificado)
```hcl
module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "~> 19.0"

  cluster_name    = "${var.project_name}-eks"
  cluster_version = "1.27"

  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnet_ids

  eks_managed_node_groups = {
    main = {
      min_size     = 1
      max_size     = 3
      desired_size = 2

      instance_types = ["t3.medium"]
      capacity_type  = "ON_DEMAND"
    }
  }

  tags = {
    Environment = var.environment
  }
}

# Helm provider para desplegar aplicaciones
provider "helm" {
  kubernetes {
    host                   = module.eks.cluster_endpoint
    cluster_ca_certificate = base64decode(module.eks.cluster_certificate_authority_data)

    exec {
      api_version = "client.authentication.k8s.io/v1beta1"
      command     = "aws"
      args = [
        "eks",
        "get-token",
        "--cluster-name",
        module.eks.cluster_name
      ]
    }
  }
}

# Desplegar aplicación con Helm
resource "helm_release" "app" {
  name       = "myapp"
  repository = "https://charts.myapp.com"
  chart      = "myapp"
  namespace  = "production"

  set {
    name  = "image.tag"
    value = var.app_version
  }

  set {
    name  = "replicaCount"
    value = "3"
  }

  depends_on = [module.eks]
}
```

---

## Parte 7: Mejores Prácticas

### 1. Organización de archivos
```
project/
├── main.tf           # Recursos principales
├── variables.tf      # Variables de entrada
├── outputs.tf        # Valores de salida
├── providers.tf      # Configuración de providers
├── backend.tf        # Configuración de backend
├── versions.tf       # Versiones requeridas
└── terraform.tfvars  # Valores de variables (no commitear)
```

### 2. Naming conventions
```hcl
# Usar naming consistente
resource "aws_instance" "web_server" {  # snake_case
  tags = {
    Name = "web-server-prod"  # kebab-case para nombres visuales
  }
}
```

### 3. Variables sensibles
```hcl
variable "db_password" {
  description = "Database password"
  type        = string
  sensitive   = true  # No se muestra en outputs
}
```

### 4. Data sources (recursos existentes)
```hcl
# Referenciar recursos existentes
data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"] # Canonical

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }
}

resource "aws_instance" "web" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = "t3.micro"
}
```

### 5. Locals para valores calculados
```hcl
locals {
  common_tags = {
    Environment = var.environment
    Project     = var.project_name
    ManagedBy   = "Terraform"
  }

  instance_name = "${var.project_name}-${var.environment}-instance"
}

resource "aws_instance" "web" {
  tags = merge(
    local.common_tags,
    {
      Name = local.instance_name
    }
  )
}
```

---

## Parte 8: Terraform Cloud / Terraform Enterprise

### Workspace remoto
```hcl
terraform {
  cloud {
    organization = "mi-organizacion"

    workspaces {
      name = "produccion"
    }
  }
}
```

---

## Comandos Útiles

```bash
# Inicializar
terraform init

# Upgrade providers
terraform init -upgrade

# Workspace management
terraform workspace list
terraform workspace new dev
terraform workspace select prod

# Plan con archivo de salida
terraform plan -out=tfplan
terraform apply tfplan

# Targeting recursos específicos
terraform apply -target=aws_instance.web

# Ver recursos en estado
terraform state list

# Mostrar recurso específico
terraform state show aws_instance.web

# Remover recurso del estado (sin destruir)
terraform state rm aws_instance.web

# Importar recurso existente
terraform import aws_instance.web i-1234567890

# Taint (marcar para recrear)
terraform taint aws_instance.web
terraform untaint aws_instance.web

# Graph (visualizar dependencias)
terraform graph | dot -Tpng > graph.png

# Validate
terraform validate

# Format
terraform fmt -recursive

# Console (REPL)
terraform console
```

---

## Resumen Comandos de Workflow

```bash
# 1. Inicializar proyecto
terraform init

# 2. Validar sintaxis
terraform validate

# 3. Formatear código
terraform fmt -recursive

# 4. Plan (dry-run)
terraform plan -out=plan.tfplan

# 5. Aplicar
terraform apply plan.tfplan

# 6. Ver outputs
terraform output

# 7. Destruir todo
terraform destroy
```

---

## Checklist de Terraform

- [ ] Instalar Terraform
- [ ] Configurar AWS/Azure CLI
- [ ] Crear proyecto con estructura correcta
- [ ] Definir providers
- [ ] Crear recursos
- [ ] Definir variables y outputs
- [ ] Usar módulos para reutilización
- [ ] Configurar remote backend
- [ ] Versionar código en Git (sin .tfvars)
- [ ] Implementar CI/CD para Terraform
- [ ] Usar workspaces para ambientes
- [ ] Documentar infraestructura

---

¡Infraestructura como código con Terraform! 🚀
