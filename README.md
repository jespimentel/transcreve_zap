# transcreve_zap
Transcreve o chat do WhatsApp, lendo o arquivo texto. Quando encontra mensagens de áudio ("opus") e de vídeo ("mp4"), calcula o hash (sha256) dos respectivos arquivos e as transcreve com o Whisper, na sequência, para dar contexto.
