**OwoBot: FFLogs Discord Bot**

*OwoBot* é um bot para Discord desenvolvido em Python, que integra com a API v2 do FFLogs:

* 📊 Exibir estatísticas de desempenho de personagens de Final Fantasy XIV (Best Avg, Median Avg, All‑Star Rank).
* ⏱ Listar as 3 últimas lutas do personagem (boss, dificuldade, resultado e duração) com link direto para o log.
* 🏰 Capturar o gráfico de progresso da guilda via Selenium e enviar como imagem.

---

## 🚀 Funcionalidades

1. **Vincular personagem**

   ```bash
   !vincular <servidor> [região] <Nome_Sobrenome>
   ```

   * Exemplo: `!vincular lamia NA Jiro Strahlender`
   * Armazena servidor, região (padrão `NA`) e nome no arquivo `user_characters.json`.

2. **Exibir perfil**

   ```bash
   !perfil [@membro]
   ```

   * Exibe: Best Avg, Median Avg, All‑Star Rank, destaque (melhor parse % em boss) e link para o perfil FFLogs.
   * Se mencionar outro usuário, traz o perfil vinculado dele.

3. **Lutas recentes**

   ```bash
   !recente [servidor] [região] <Nome>
   ```

   * Lista as 3 últimas lutas: boss, dificuldade (Normal/Savage/Ultimate), ✅/❌, duração e link.
   * Usa dados vinculados se não passar argumentos.

4. **Progresso de guilda**

   ```bash
   !progresso
   ```

   * Captura via Selenium o widget de progresso da guilda (embed FFLogs) e envia um screenshot.

5. **Ajuda**

   ```bash
   !help
   ```

   * Lista e descreve todos os comandos.

---

## ⚙️ Instalação e Configuração

1. Clone o repositório:

   ```bash
   git clone https://github.com/SEU_USUARIO/owobot.git
   cd owobot
   ```

2. Crie e ative um virtualenv:

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # macOS/Linux
   venv\Scripts\activate   # Windows
   ```

3. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

4. Crie um arquivo `.env` na raiz com as credenciais:

   ```text
   DISCORD_TOKEN=seu_token_discord
   FFLOGS_CLIENT_ID=seu_client_id_fflogs
   FFLOGS_CLIENT_SECRET=seu_client_secret_fflogs
   ```

5. Inicie o bot:

   ```bash
   python bot.py
   ```

---

## 🤝 Contribuições

1. Faça um Fork deste repositório.
2. Crie uma branch para sua feature: `git checkout -b feature/nova-funcionalidade`
3. Commit suas mudanças: `git commit -m "Adiciona X feature"`
4. Push na branch: `git push origin feature/nova-funcionalidade`
5. Abra um Pull Request.

---

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para detalhes.
