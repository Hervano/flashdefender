# Instruções de Instalação - FlashDefender

## Pré-requisitos

- Python 3.11 ou superior
- pip (gerenciador de pacotes Python)
- Acesso à internet
- Credenciais válidas da API Flashman

## Instalação

### 1. Preparação do Ambiente

```bash
# Clone ou baixe o projeto FlashDefender
cd flashdefender_backend

# Crie um ambiente virtual Python
python3 -m venv venv

# Ative o ambiente virtual
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows
```

### 2. Instalação de Dependências

```bash
# Instale as dependências do projeto
pip install -r requirements.txt
```

### 3. Execução da Aplicação

```bash
# Execute a aplicação
python src/main.py
```

A aplicação estará disponível em: `http://localhost:5000`

## Estrutura do Projeto

```
flashdefender_backend/
├── src/
│   ├── routes/
│   │   ├── flashman.py      # Rotas da API Flashman
│   │   └── user.py          # Rotas de usuário (exemplo)
│   ├── models/              # Modelos de dados
│   ├── static/              # Arquivos estáticos (frontend)
│   ├── database/            # Banco de dados SQLite
│   └── main.py              # Arquivo principal
├── venv/                    # Ambiente virtual Python
├── requirements.txt         # Dependências Python
├── README.md               # Documentação
└── INSTALACAO.md           # Este arquivo
```

## Configuração

### Variáveis de Ambiente (Opcional)

Você pode configurar as seguintes variáveis de ambiente:

```bash
export FLASK_ENV=development    # Modo de desenvolvimento
export FLASK_DEBUG=1           # Debug habilitado
```

### Configuração de Rede

A aplicação roda por padrão em:
- **Host**: 0.0.0.0 (todas as interfaces)
- **Porta**: 5000

Para alterar, modifique o arquivo `src/main.py`:

```python
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
```

## Solução de Problemas

### Erro de Dependências

Se houver erro na instalação de dependências:

```bash
# Atualize o pip
pip install --upgrade pip

# Reinstale as dependências
pip install -r requirements.txt --force-reinstall
```

### Erro de Porta em Uso

Se a porta 5000 estiver em uso:

1. Pare outros serviços na porta 5000
2. Ou altere a porta no arquivo `main.py`

### Erro de CORS

Se houver problemas de CORS:

1. Verifique se `flask-cors` está instalado
2. Confirme que CORS está configurado no `main.py`

### Problemas de Conectividade

1. Verifique a conectividade com a API Flashman
2. Confirme as credenciais de acesso
3. Teste a URL da API manualmente

## Desenvolvimento

### Modo de Desenvolvimento

Para desenvolvimento, execute:

```bash
# Ative o ambiente virtual
source venv/bin/activate

# Execute em modo debug
python src/main.py
```

### Estrutura de Desenvolvimento

- **Frontend**: Localizado em `src/static/`
- **Backend**: Rotas em `src/routes/`
- **Modelos**: Definidos em `src/models/`

## Produção

Para ambiente de produção, considere:

1. **Servidor WSGI**: Use Gunicorn ou uWSGI
2. **Proxy Reverso**: Configure Nginx ou Apache
3. **HTTPS**: Configure certificados SSL
4. **Firewall**: Restrinja acesso às portas necessárias

### Exemplo com Gunicorn

```bash
# Instale o Gunicorn
pip install gunicorn

# Execute a aplicação
gunicorn -w 4 -b 0.0.0.0:5000 src.main:app
```

## Backup

Faça backup regular dos seguintes arquivos:
- `src/database/app.db` (banco de dados)
- `requirements.txt` (dependências)
- Arquivos de configuração personalizados

## Atualizações

Para atualizar a aplicação:

1. Faça backup dos dados
2. Atualize os arquivos do projeto
3. Reinstale as dependências
4. Reinicie a aplicação

## Suporte

Para suporte técnico:
1. Verifique os logs da aplicação
2. Consulte a documentação da API Flashman
3. Entre em contato com o administrador do sistema

