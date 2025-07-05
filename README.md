**OwoBot: FFLogs Discord Bot**

*OwoBot* is a Discord bot written in Python that integrates with the FFLogs v2 API to:

* 📊 Display character performance stats for Final Fantasy XIV (Best Avg, Median Avg, All‑Star Rank).
* ⏱ List the last 3 fights of a character (boss, difficulty, result, duration) with direct log links.
* 🏰 Capture the guild progress widget via Selenium and send it as an image.

---

## 🚀 Features

1. **Link your character to your Discord account**

   ```bash
   !vincular <server> [region] <First_Last>
   ```
   ![image](https://github.com/user-attachments/assets/32915f4c-c621-444a-b69c-2829ff1f9f82)


   * Example: `!vincular behemoth NA John Doe`
   * Stores server, region, and character name.

2. **Show profile**

   ```bash
   !perfil
   ```
   ![image](https://github.com/user-attachments/assets/571e85d1-d008-4701-9e7a-df9a246b7d4b)

   * Shows: Best Avg, Median Avg, All‑Star Rank, Highlight (highest parse % and boss), and a link to the FFLogs profile.
   * Mention another user to display their linked character.

3. **Recent fights**

   ```bash
   !recente [server] [region] <Name>
   ```
![image](https://github.com/user-attachments/assets/fc4ee1f2-be32-4fd8-9ede-0e2c15ad421e)

   * Lists the last 3 fights: boss, difficulty (Normal/Savage/Ultimate), ✅/❌, duration, and log link.
   * Uses linked character if no arguments provided.

4. **Static/Guild progress**

   ```bash
   !progresso
   ```
   ![image](https://github.com/user-attachments/assets/fd93aeba-a593-45e6-b8cc-fe352a89317e)

   * Captures the guild progress widget via Selenium (FFLogs embed) and sends a screenshot.

4. **Help**

   ```bash
   !help
   ```

   * Lists and explains all commands.

---

## ⚙️ Installation & Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/YOUR_USERNAME/owobot.git
   cd owobot
   ```

2. **Create & activate a virtual environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate    # macOS/Linux
   venv\Scripts\activate     # Windows
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure credentials**
   Create a `.env` file in the project root:

   ```env
   DISCORD_TOKEN=<your-discord-bot-token>
   FFLOGS_CLIENT_ID=<your-fflogs-client-id>
   FFLOGS_CLIENT_SECRET=<your-fflogs-client-secret>
   ```

5. **Run the bot**

   ```bash
   python bot.py
   ```

---

## 🤝 Contributing

1. Fork this repository.
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m "Add feature X"`
4. Push to the branch: `git push origin feature/your-feature`
5. Open a Pull Request.

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
