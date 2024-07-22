# transcreve_zap
Transcreve o chat do WhatsApp, lendo o arquivo texto da conversa exportada. Quando encontra mensagens de áudio ("opus") e de vídeo ("mp4"), calcula o hash (sha256) dos respectivos arquivos e as transcreve com o Whisper, na sequência, para dar contexto.

## Requisitos
FFmpeg: (configure o path nas variáveis de ambiente; privilégio de administrador)
Whisper: pip install git+https://github.com/openai/whisper.git
