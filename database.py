import json
import os
from datetime import datetime

class Database:
    def __init__(self, arquivo='dados.json'):
        self.arquivo = arquivo
        self.carregar_dados()

    def carregar_dados(self):
        if os.path.exists(self.arquivo):
            with open(self.arquivo, 'r', encoding='utf-8') as f:
                self.dados = json.load(f)
        else:
            self.dados = {
                'fotos': [],
                'musicas': [],
                'cartas': [],
                'mensagens': [],
                'datas': [],
                'configuracoes': {
                    'titulo_site': 'Meu Amor',
                    'cor_primaria': '#6c5ce7',
                    'cor_secundaria': '#a8a5e8',
                    'fundo_particles': True,
                    'surpresa_titulo': '✨ Surpresa de Dia dos Namorados ✨',
                    'surpresa_frase_jogo': 'AMOR ETERNO',
                    'surpresa_mensagem_capsula': '🎁 Mensagem secreta aqui!',
                    'surpresa_data_capsula': '2026-06-12',
                    'surpresa_data_contagem': '2026-06-12',
                    'surpresa_ativo_contagem': True,
                    'surpresa_ativo_capsula': True,
                    'surpresa_ativo_jogo': True,
                    'surpresa_ativo_album': True,
                    'surpresa_ativo_mural': True,
                    'surpresa_ativo_playlist': True
                }
            }
            self.salvar_dados()

    def salvar_dados(self):
        with open(self.arquivo, 'w', encoding='utf-8') as f:
            json.dump(self.dados, f, ensure_ascii=False, indent=2)

    def adicionar_foto(self, caminho, legenda=''):
        self.dados['fotos'].append({
            'id': len(self.dados['fotos']) + 1,
            'caminho': caminho,
            'legenda': legenda,
            'data': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
        self.salvar_dados()

    def remover_foto(self, id_foto):
        self.dados['fotos'] = [f for f in self.dados['fotos'] if f['id'] != id_foto]
        self.salvar_dados()

    def adicionar_musica(self, caminho, titulo=''):
        self.dados['musicas'].append({
            'id': len(self.dados['musicas']) + 1,
            'caminho': caminho,
            'titulo': titulo,
            'data': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
        self.salvar_dados()

    def remover_musica(self, id_musica):
        self.dados['musicas'] = [m for m in self.dados['musicas'] if m['id'] != id_musica]
        self.salvar_dados()

    def adicionar_carta(self, titulo, conteudo):
        self.dados['cartas'].append({
            'id': len(self.dados['cartas']) + 1,
            'titulo': titulo,
            'conteudo': conteudo,
            'data': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
        self.salvar_dados()

    def editar_carta(self, id_carta, titulo, conteudo):
        for carta in self.dados['cartas']:
            if carta['id'] == id_carta:
                carta['titulo'] = titulo
                carta['conteudo'] = conteudo
                break
        self.salvar_dados()

    def remover_carta(self, id_carta):
        self.dados['cartas'] = [c for c in self.dados['cartas'] if c['id'] != id_carta]
        self.salvar_dados()

    def adicionar_mensagem(self, texto):
        self.dados['mensagens'].append({
            'id': len(self.dados['mensagens']) + 1,
            'texto': texto,
            'data': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
        self.salvar_dados()

    def remover_mensagem(self, id_mensagem):
        self.dados['mensagens'] = [m for m in self.dados['mensagens'] if m['id'] != id_mensagem]
        self.salvar_dados()

    def adicionar_data(self, titulo, data_evento):
        self.dados['datas'].append({
            'id': len(self.dados['datas']) + 1,
            'titulo': titulo,
            'data': data_evento,
            'criado_em': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
        self.salvar_dados()

    def remover_data(self, id_data):
        self.dados['datas'] = [d for d in self.dados['datas'] if d['id'] != id_data]
        self.salvar_dados()

    def atualizar_configuracoes(self, novas_configs):
        self.dados['configuracoes'].update(novas_configs)
        self.salvar_dados()

    def obter_dados_relacionamento(self):
        if self.dados['datas']:
            data_inicio = min(self.dados['datas'], key=lambda x: x['data'])
            return {
                'data_inicio': data_inicio['data'],
                'total_datas': len(self.dados['datas'])
            }
        return None

db = Database()
