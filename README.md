# Sistema de Inventário de Racks

Sistema desenvolvido em Django para controle de racks, switches e portas de rede.

## Requisitos

* Python 3.10 ou superior
* pip

## Passo a passo para executar o projeto

### 1. Baixar o projeto

Clone o repositório ou extraia o arquivo .zip enviado.

### 2. Criar ambiente virtual

No terminal, dentro da pasta do projeto:

Windows:

```
python -m venv venv
```

Linux / Mac:

```
python3 -m venv venv
```

### 3. Ativar o ambiente virtual

Windows:

```
venv\Scripts\activate
```

Linux / Mac:

```
source venv/bin/activate
```

### 4. Instalar dependências

```
pip install -r requirements.txt
```

### 5. Aplicar migrações do banco

```
python manage.py migrate
```

### 6. (Opcional) Criar usuário administrador

```
python manage.py createsuperuser
```

### 7. Executar o servidor

```
python manage.py runserver
```

### 8. Acessar o sistema

Abra no navegador:

```
http://127.0.0.1:8000/
```

O sistema redirecionará automaticamente para:

```
/inventario
```

### Acesso ao painel administrativo

```
http://127.0.0.1:8000/admin
```
