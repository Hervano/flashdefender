# FlashDefender

FlashDefender é uma aplicação web para gerenciar DNS em equipamentos Flashman de forma automatizada. A aplicação permite configurar DNS padrão, remover DNS específicos e monitorar o status das operações em tempo real com categorização inteligente dos equipamentos.

## Funcionalidades

### 🔧 **Configuração de DNS**
- **Lista de DNS Confiáveis**: Seleção de provedores DNS públicos e confiáveis pré-configurados
- **DNS Personalizados**: Possibilidade de adicionar DNS personalizados à lista
- **DNS para Remoção**: Especificação de DNS suspeitos que devem ser removidos dos equipamentos

### 📊 **Categorização Inteligente**
- **Rede Segura**: Equipamentos que não possuem DNS suspeitos (já seguros)
- **OK**: Equipamentos que tiveram DNS alterados com sucesso
- **Falhas**: Equipamentos que apresentaram falha na alteração de DNS

### 📈 **Visualização e Relatórios**
- **Gráfico de Pizza**: Visualização em tempo real da distribuição dos equipamentos por categoria
- **Porcentagens**: Cálculo automático das proporções de cada categoria
- **Exportação CSV**: Download de relatórios detalhados para cada categoria

### 🔍 **Monitoramento**
- **Teste de Conectividade**: Validação de credenciais e conectividade com a API Flashman
- **Processamento em Tempo Real**: Acompanhamento do progresso das operações
- **Timestamps**: Registro de horários de início e fim das operações

### 🎨 **Interface Moderna**
- **Design Responsivo**: Funciona perfeitamente em desktop e dispositivos móveis
- **Componentes Interativos**: Interface intuitiva com feedback visual
- **Tema Profissional**: Design limpo e moderno com cores organizadas

## Provedores DNS Pré-configurados

A aplicação inclui os seguintes provedores DNS confiáveis:

| Provedor | DNS Primário | DNS Secundário |
|----------|--------------|----------------|
| Google | 8.8.8.8 | 8.8.4.4 |
| Cloudflare | 1.1.1.1 | 1.0.0.1 |
| Quad9 | 9.9.9.9 | 149.112.112.112 |
| OpenDNS | 208.67.222.222 | 208.67.220.220 |
| Controle D | 76.76.2.0 | 76.76.10.0 |
| DNS do AdGuard | 94.140.14.14 | 94.140.15.15 |
| Navegação limpa | 185.228.168.9 | 185.228.169.9 |
| DNS alternativo | 76.76.19.19 | 76.223.122.150 |

## Como Usar

### 1. Configuração de DNS Confiáveis

1. **Selecionar DNS**: Clique nos provedores DNS que deseja usar como padrão
2. **Adicionar Personalizados**: Use o botão "Adicionar DNS Personalizado" para incluir seus próprios DNS
3. **Visualizar Seleção**: Os DNS selecionados aparecerão na área "DNS Selecionados"

### 2. Configuração de Parâmetros

1. **DNS para Deletar**: Insira os DNS suspeitos que devem ser removidos (ex: `1.1.1.1,1.0.0.1`)
2. **URL Flashman**: Insira a URL da sua instância Flashman (ex: `https://suporte.flashman.anlix.io`)
3. **Credenciais**: Insira usuário e senha para autenticação na API

### 3. Teste e Execução

1. **Testar Conexão**: Clique em "Testar Conexão" para validar as configurações
2. **Iniciar Processamento**: Clique em "Iniciar" para começar a análise dos equipamentos
3. **Acompanhar Progresso**: Monitore o gráfico e estatísticas em tempo real

### 4. Análise de Resultados

- **Gráfico de Pizza**: Visualize a distribuição dos equipamentos por categoria
- **Estatísticas**: Veja contadores e porcentagens de cada categoria
- **Exportar Dados**: Baixe relatórios CSV para análise detalhada

## Fluxo de Operação Atualizado

1. **Coleta de Equipamentos**: Busca todos os equipamentos online na API Flashman (paginação automática)
2. **Análise de DNS**: Para cada equipamento, verifica os DNS atuais
3. **Categorização Inteligente**:
   - Se não possui DNS suspeito → **Rede Segura**
   - Se possui DNS suspeito e alteração foi bem-sucedida → **OK**
   - Se possui DNS suspeito mas falhou na alteração → **Falhas**
4. **Atualização em Tempo Real**: Gráfico e estatísticas são atualizados durante o processamento
5. **Relatório Final**: Exibição de resultados com opções de exportação

## Exportação de Dados

### Formatos de CSV

Cada categoria gera um arquivo CSV com as seguintes informações:

- **ID do Equipamento**: MAC address do equipamento
- **DNS Antigos**: DNS que estavam configurados antes
- **DNS Novos**: DNS que foram aplicados (quando aplicável)
- **Observações**: Mensagens de erro ou sucesso

### Nomenclatura dos Arquivos

- `flashdefender_rede_segura_AAAA-MM-DD_HHMMSS.csv`
- `flashdefender_ok_AAAA-MM-DD_HHMMSS.csv`
- `flashdefender_falhas_AAAA-MM-DD_HHMMSS.csv`

## Requisitos da API Flashman

A aplicação utiliza as seguintes rotas da API Flashman:

- `GET /api/v3/device/search/` - Busca equipamentos online (com paginação)
- `GET /api/v3/device/mac/{mac}/lan-dns-servers` - Obtém DNS do equipamento
- `PUT /api/v3/device/mac/{mac}/lan-dns-servers` - Atualiza DNS do equipamento

## Tecnologias Utilizadas

### Frontend
- **React 19.1.0** - Framework JavaScript
- **Tailwind CSS** - Framework CSS
- **Shadcn/UI** - Biblioteca de componentes
- **Recharts** - Biblioteca para gráficos
- **Lucide React** - Ícones
- **Axios** - Cliente HTTP

### Backend
- **Flask 3.1.1** - Framework web Python
- **Flask-CORS** - Middleware para CORS
- **Requests** - Biblioteca para requisições HTTP

## Segurança e Performance

- **Autenticação Base64**: Credenciais codificadas para API Flashman
- **CORS Configurado**: Comunicação segura frontend/backend
- **Paginação Automática**: Processamento eficiente de grandes volumes
- **Timeout Configurável**: Prevenção de travamentos (5 minutos)
- **Validação de Entrada**: Verificação de todos os campos obrigatórios

## Limitações

- Processa apenas equipamentos online
- Requer credenciais válidas da API Flashman
- Timeout de 5 minutos para operações longas
- Processamento sequencial para evitar sobrecarga da API

## Novidades da Versão Atual

### ✨ **Novas Funcionalidades**
- Lista de DNS confiáveis e públicos pré-configurada
- Possibilidade de adicionar DNS personalizados
- Categorização inteligente em três grupos (Rede Segura, OK, Falhas)
- Gráfico de pizza com porcentagens em tempo real
- Exportação de CSV para cada categoria
- Interface redesenhada com melhor usabilidade

### 🔧 **Melhorias Técnicas**
- Lógica de processamento otimizada
- Melhor tratamento de erros
- Interface mais responsiva
- Componentes modulares e reutilizáveis

## Suporte

Para suporte técnico ou dúvidas sobre a aplicação:
1. Consulte a documentação da API Flashman
2. Verifique os logs da aplicação
3. Entre em contato com o administrador do sistema

---

**FlashDefender** - Gerenciador de DNS para equipamentos Flashman com categorização inteligente e relatórios detalhados.

