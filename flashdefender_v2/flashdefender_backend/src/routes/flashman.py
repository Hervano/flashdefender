from flask import Blueprint, jsonify, request
import requests
import base64
import time
from datetime import datetime

flashman_bp = Blueprint('flashman', __name__)

def create_auth_header(username, password):
    """Cria o header de autenticação Basic Auth em base64"""
    credentials = f"{username}:{password}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()
    return f"Basic {encoded_credentials}"

def get_all_devices(flashman_url, auth_header):
    """Coleta todos os equipamentos online da API Flashman"""
    devices = []
    page = 1
    page_limit = 50  # Máximo permitido pela API Flashman
    
    print(f"Iniciando coleta de dispositivos de {flashman_url}")
    
    while True:
        try:
            print(f"Buscando página {page} com limite {page_limit}")
            
            response = requests.get(
                f"{flashman_url}/api/v3/device/search/",
                headers={
                    'accept': 'application/json',
                    'Authorization': auth_header
                },
                params={
                    'online': 'true',
                    'fields': '_id',
                    'page': page,
                    'pageLimit': page_limit
                },
                timeout=30
            )
            
            print(f"Status da resposta: {response.status_code}")
            
            if response.status_code != 200:
                print(f"Erro HTTP: {response.status_code} - {response.text}")
                break
                
            data = response.json()
            print(f"Dados recebidos: {data}")
            
            if not data.get('success'):
                print(f"API retornou success=false: {data.get('message', 'Sem mensagem')}")
                break
                
            devices_in_page = data.get('devices', [])
            print(f"Dispositivos encontrados na página {page}: {len(devices_in_page)}")
            
            if not devices_in_page:
                print("Nenhum dispositivo encontrado nesta página, parando busca")
                break
                
            devices.extend(devices_in_page)
            print(f"Total de dispositivos coletados até agora: {len(devices)}")
            
            # Se retornou menos que o limite, chegamos ao fim
            if len(devices_in_page) < page_limit:
                print("Página retornou menos dispositivos que o limite, finalizando busca")
                break
                
            page += 1
            
        except Exception as e:
            print(f"Erro ao buscar dispositivos na página {page}: {e}")
            break
    
    print(f"Coleta finalizada. Total de dispositivos: {len(devices)}")
    return devices

def get_device_dns(flashman_url, auth_header, device_id):
    """Obtém os DNS atuais de um equipamento"""
    try:
        # URL encode do MAC address
        encoded_mac = device_id.replace(':', '%3A')
        
        print(f"Obtendo DNS do dispositivo: {device_id}")
        
        response = requests.get(
            f"{flashman_url}/api/v3/device/mac/{encoded_mac}/lan-dns-servers",
            headers={
                'accept': 'application/json',
                'Authorization': auth_header
            },
            timeout=30
        )
        
        print(f"Status DNS {device_id}: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Dados DNS {device_id}: {data}")
            if data.get('success'):
                return data.get('lan_dns_servers_list', [])
        
        print(f"Falha ao obter DNS de {device_id}: {response.text}")
        return None
        
    except Exception as e:
        print(f"Erro ao obter DNS do dispositivo {device_id}: {e}")
        return None

def update_device_dns(flashman_url, auth_header, device_id, new_dns_list):
    """Atualiza os DNS de um equipamento"""
    try:
        # URL encode do MAC address
        encoded_mac = device_id.replace(':', '%3A')
        
        print(f"Atualizando DNS do dispositivo {device_id} para: {new_dns_list}")
        
        response = requests.put(
            f"{flashman_url}/api/v3/device/mac/{encoded_mac}/lan-dns-servers",
            headers={
                'accept': 'application/json',
                'Authorization': auth_header,
                'Content-Type': 'application/json'
            },
            json={
                'lan_dns_servers_list': new_dns_list
            },
            timeout=30
        )
        
        print(f"Status atualização {device_id}: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Resultado atualização {device_id}: {data}")
            return data.get('success', False)
        
        print(f"Falha ao atualizar DNS de {device_id}: {response.text}")
        return False
        
    except Exception as e:
        print(f"Erro ao atualizar DNS do dispositivo {device_id}: {e}")
        return False

def has_suspicious_dns(current_dns, dns_to_delete):
    """Verifica se o equipamento possui DNS suspeito"""
    if not current_dns or not dns_to_delete:
        return False
    
    suspicious_dns_list = [dns.strip() for dns in dns_to_delete.split(',')]
    print(f"DNS suspeitos configurados: {suspicious_dns_list}")
    print(f"DNS atuais do equipamento: {current_dns}")
    
    for dns in current_dns:
        if dns.strip() in suspicious_dns_list:
            print(f"DNS suspeito encontrado: {dns}")
            return True
    
    print("Nenhum DNS suspeito encontrado")
    return False

@flashman_bp.route('/test-connection', methods=['POST'])
def test_connection():
    """Testa a conexão com a API Flashman"""
    try:
        data = request.get_json()
        flashman_url = data.get('flashman_url')
        username = data.get('username')
        password = data.get('password')
        
        if not all([flashman_url, username, password]):
            return jsonify({
                'success': False,
                'message': 'URL do Flashman, usuário e senha são obrigatórios'
            }), 400
        
        # Remove barra final se existir
        flashman_url = flashman_url.rstrip('/')
        
        # Cria header de autenticação
        auth_header = create_auth_header(username, password)
        
        print(f"Testando conexão com: {flashman_url}")
        
        # Testa a conexão buscando a primeira página de dispositivos
        response = requests.get(
            f"{flashman_url}/api/v3/device/search/",
            headers={
                'accept': 'application/json',
                'Authorization': auth_header
            },
            params={
                'online': 'true',
                'fields': '_id',
                'page': 1,
                'pageLimit': 1
            },
            timeout=30
        )
        
        print(f"Status teste conexão: {response.status_code}")
        print(f"Resposta teste: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                # Busca o total de dispositivos
                devices = get_all_devices(flashman_url, auth_header)
                return jsonify({
                    'success': True,
                    'message': f'Conexão estabelecida com sucesso!',
                    'total_devices': len(devices)
                })
        
        return jsonify({
            'success': False,
            'message': 'Falha na autenticação ou conexão com a API'
        }), 401
        
    except requests.exceptions.Timeout:
        return jsonify({
            'success': False,
            'message': 'Timeout na conexão com a API'
        }), 408
        
    except requests.exceptions.ConnectionError:
        return jsonify({
            'success': False,
            'message': 'Erro de conexão com a API'
        }), 503
        
    except Exception as e:
        print(f"Erro no teste de conexão: {e}")
        return jsonify({
            'success': False,
            'message': f'Erro interno: {str(e)}'
        }), 500

@flashman_bp.route('/process-dns', methods=['POST'])
def process_dns():
    """Processa a alteração de DNS nos equipamentos com nova lógica de categorização"""
    try:
        data = request.get_json()
        flashman_url = data.get('flashman_url')
        username = data.get('username')
        password = data.get('password')
        default_dns = data.get('default_dns')
        dns_to_delete = data.get('dns_to_delete')
        
        print(f"Iniciando processamento DNS")
        print(f"URL: {flashman_url}")
        print(f"DNS padrão: {default_dns}")
        print(f"DNS para deletar: {dns_to_delete}")
        
        if not all([flashman_url, username, password, default_dns, dns_to_delete]):
            return jsonify({
                'success': False,
                'error': 'Todos os campos são obrigatórios'
            }), 400
        
        # Remove barra final se existir
        flashman_url = flashman_url.rstrip('/')
        
        # Cria header de autenticação
        auth_header = create_auth_header(username, password)
        
        # Prepara lista de DNS padrão
        default_dns_list = [dns.strip() for dns in default_dns.split(',')]
        print(f"Lista DNS padrão: {default_dns_list}")
        
        # Coleta todos os equipamentos
        devices = get_all_devices(flashman_url, auth_header)
        
        if not devices:
            print("Nenhum dispositivo encontrado!")
            return jsonify({
                'success': False,
                'error': 'Nenhum equipamento encontrado'
            }), 404
        
        print(f"Processando {len(devices)} dispositivos")
        
        # Inicializa contadores e listas de resultados
        safe_devices = []        # Rede Segura
        success_devices = []     # OK (DNS alterados com sucesso)
        failed_devices = []      # Falhas
        
        start_time = datetime.now()
        
        # Processa cada equipamento
        for i, device in enumerate(devices):
            device_id = device.get('_id')
            if not device_id:
                print(f"Dispositivo {i+1} sem ID, pulando")
                continue
            
            print(f"Processando dispositivo {i+1}/{len(devices)}: {device_id}")
            
            try:
                # Obtém DNS atual do equipamento
                current_dns = get_device_dns(flashman_url, auth_header, device_id)
                
                if current_dns is None:
                    # Erro ao obter DNS
                    print(f"Erro ao obter DNS de {device_id}")
                    failed_devices.append({
                        'device_id': device_id,
                        'old_dns': [],
                        'new_dns': [],
                        'error': 'Erro ao obter DNS atual'
                    })
                    continue
                
                # Verifica se possui DNS suspeito
                if not has_suspicious_dns(current_dns, dns_to_delete):
                    # Rede Segura - não possui DNS suspeito
                    print(f"Dispositivo {device_id} já é seguro")
                    safe_devices.append({
                        'device_id': device_id,
                        'old_dns': current_dns,
                        'new_dns': current_dns,
                        'message': 'Equipamento já possui DNS seguro'
                    })
                else:
                    # Possui DNS suspeito, tenta alterar
                    print(f"Dispositivo {device_id} possui DNS suspeito, tentando alterar")
                    success = update_device_dns(flashman_url, auth_header, device_id, default_dns_list)
                    
                    if success:
                        # OK - DNS alterado com sucesso
                        print(f"DNS de {device_id} alterado com sucesso")
                        success_devices.append({
                            'device_id': device_id,
                            'old_dns': current_dns,
                            'new_dns': default_dns_list,
                            'message': 'DNS alterado com sucesso'
                        })
                    else:
                        # Falha - não conseguiu alterar DNS
                        print(f"Falha ao alterar DNS de {device_id}")
                        failed_devices.append({
                            'device_id': device_id,
                            'old_dns': current_dns,
                            'new_dns': [],
                            'error': 'Falha ao alterar DNS'
                        })
                
                # Pequena pausa para não sobrecarregar a API
                time.sleep(0.1)
                
            except Exception as e:
                print(f"Erro no processamento de {device_id}: {e}")
                failed_devices.append({
                    'device_id': device_id,
                    'old_dns': [],
                    'new_dns': [],
                    'error': f'Erro no processamento: {str(e)}'
                })
        
        end_time = datetime.now()
        
        print(f"Processamento concluído:")
        print(f"- Rede Segura: {len(safe_devices)}")
        print(f"- Sucessos: {len(success_devices)}")
        print(f"- Falhas: {len(failed_devices)}")
        
        return jsonify({
            'success': True,
            'message': 'Processamento concluído',
            'start_time': start_time.strftime('%d/%m/%Y %H:%M:%S'),
            'end_time': end_time.strftime('%d/%m/%Y %H:%M:%S'),
            'total_devices': len(devices),
            'safe': safe_devices,
            'success': success_devices,
            'failures': failed_devices,
            'summary': {
                'safe_count': len(safe_devices),
                'success_count': len(success_devices),
                'failures_count': len(failed_devices)
            }
        })
        
    except Exception as e:
        print(f"Erro geral no processamento: {e}")
        return jsonify({
            'success': False,
            'error': f'Erro interno: {str(e)}'
        }), 500

