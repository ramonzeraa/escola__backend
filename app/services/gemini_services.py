import google.generativeai as genai
from app.config import settings
import json
import time
class GeminiService:
    def __init__(self):
        genai.configure(api_key=settings.GOOGLE_API_KEY)
        self.model = genai.GenerativeModel('gemini-pro')
        # Contador de requests, para evitar abuso e possíveis bloqueios
        self.requests_count = 0
        self.last_request_time = None

    def criar_prompt(self, materia: str, pergunta: str) -> str:
        return f"""
        Você é um professor de ensino fundamental explicando sobre {materia}.
        Responda à seguinte pergunta: {pergunta}
        Você precisa criar uma explicação clara e objetiva para o aluno entender o assunto {materia} em relação a pergunta {pergunta}.
        
        
        IMPORTANTE: Sua resposta DEVE seguir EXATAMENTE este formato JSON:
        {{
            "materia": "{materia}",
            "resposta": "SUA_EXPLICACAO_AQUI",
            "links": [
                "3 links reais e relevantes sobre o assunto"
            ],
            "informacoes_uteis": [
                "3 a 5 informações úteis e específicas sobre o tema"
            ]
        }}
        
        Diretrizes para uma resposta inclusiva:
        1. Use linguagem simples e clara
        2. Divida explicações complexas em passos menores
        3. Forneça exemplos do cotidiano
        4. Inclua diferentes formas de aprender o mesmo conceito
        5. Considere diferentes ritmos de aprendizagem
        
         Para os links:
        - Inclua sites com recursos de acessibilidade
        - Os links PRECISAM ser de fácil acesso em português brasileiro
        - Priorize conteúdo com suporte a leitores de tela
        - Sugira sites com opções de alto contraste
        - Inclua recursos multimídia (vídeos legendados, áudios, etc)
        Exemplos de sites: Google, Brasil Escola, Educamais Brasil, Khan Academy
        
        Para as informações úteis, inclua:
        - Dicas práticas de estudo adaptadas
        - Sugestões de ferramentas assistivas quando relevante
        - Diferentes abordagens para o mesmo conteúdo
        - Dicas para diferentes estilos de aprendizagem
        - Sugestões de como adaptar o estudo às necessidades individuais
          GEMINI, NÃO DÊ RESPOSTAS GENERALIZADAS, APROFUNDE E ENTRE EM CONTATO COM O ALUNO PARA QUE ELE POSSA APRENDER DE FORMA MAIS EFICIENTE
        
        Mantenha a explicação:
        - Clara e objetiva
        - Simples e direta de forma informal para mais facil entendimento
        - Bem estruturada
        - Com exemplos concretos
        - Adequada para diferentes níveis de compreensão
        NÃO inclua nada além do JSON na sua resposta.
        """

    async def generate_response(self, materia: str, pergunta: str) -> dict:
        try:
            # Adicionar verificação básica de rate limit
            current_time = time.time()
            if self.last_request_time and current_time - self.last_request_time < 1:  # 1 segundo entre requisições
                raise Exception("Taxa de requisições excedida. Aguarde um momento.")
            self.last_request_time = current_time
            
            prompt = self.criar_prompt(materia, pergunta)
            response = self.model.generate_content(prompt)
            texto_resposta = response.text.strip()
            
            # Procura pelo JSON na resposta
            inicio = texto_resposta.find('{')
            fim = texto_resposta.rfind('}') + 1
            json_str = texto_resposta[inicio:fim]
            
            return json.loads(json_str)
                
        except Exception as e:
            raise Exception(f"Erro ao gerar resposta: {str(e)}")