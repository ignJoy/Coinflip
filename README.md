### Coinflip Discord Bot

A simple Discord bot that allows users to play a **coinflip game** and manage their in-bot currency. Players can create coinflip challenges or join existing ones, betting their coins for a chance to win.

---

#### Features:
- **Create Coinflip Games:** Users can create a coinflip game with a specific bet amount.
- **Join Coinflip Games:** Other users can join available coinflip games to compete.
- **Automatic Winner Selection:** Randomly determines the winner and transfers the bet amount to the winner's account.
- **In-Bot Currency Management:**
  - Coins are tracked and stored in a `coins.json` file.
  - Users' balances are updated after each game.
- **Slash Command Support:** Easy-to-use commands to start and manage games.

---

#### Requirements:
- Python 3.8+
- Discord API token
- Dependencies:
  - `discord.py`
  - `json`
  - `os`

---

#### How to Use:
1. Clone this repository:
   ```bash
   git clone https://github.com/ignJoy/coinflip.git
   ```
2. Install dependencies:
   ```bash
   pip install discord.py
   ```
3. Add your Discord bot token to the script:
   ```python
   bot.run('YOUR_BOT_TOKEN')
   ```
4. Run the bot:
   ```bash
   python bot.py
   ```
5. Use the `/coinflip` command to start creating or joining games.

---

#### Commands:
- **`/coinflip <amount>`:** Create a coinflip game with the specified bet amount.
- **`/coinflip` (no arguments):** View and join available coinflip games.

---

#### File Structure:
- `bot.py` - Main bot script.
- `coins.json` - File to store users' coin balances.

---

#### Contributing:
Feel free to open issues or submit pull requests to improve this bot!

---

#### License:
This project is licensed under the MIT License.
