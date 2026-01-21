import sys
import os
import traceback
import tkinter as tk
from tkinter import messagebox
import tkinter.font as tkfont
import importlib

# ensure parent folder (project root) is on sys.path so we can import systemBlackJackGame
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# try to import game functions; show an error and exit if import fails
try:
    sbg = importlib.import_module("systemBlackJackGame")
    deal_cards = sbg.deal_cards
    calculate_score = sbg.calculate_score
    compare_scores = sbg.compare_scores
    determine_level = getattr(sbg, "determine_level", lambda *_: None)
except Exception as ex:
    # create a temporary Tk root to show a dialog then exit
    root = tk.Tk()
    root.withdraw()
    tb = traceback.format_exc()
    messagebox.showerror(
        "Import Error",
        "Failed to import systemBlackJackGame module.\n\n"
        f"{ex}\n\nSee console for full traceback."
    )
    print("Failed to import systemBlackJackGame:\n", tb)
    root.destroy()
    sys.exit(1)

DEFAULT_BALANCE = 100
COINS = [1, 2, 5, 10, 20, 50, 100, 200, 500, 1000, 5000]


class BlackjackGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Blackjack")
        # allow resizing and maximize
        self.resizable(True, True)

        # larger default font for readability
        default_font = ("Segoe UI", 12)
        self.option_add("*Font", default_font)
        self.large_font = tkfont.Font(family="Segoe UI", size=18, weight="bold")
        self.medium_font = tkfont.Font(family="Segoe UI", size=14)
        self.italic_font = tkfont.Font(family="Segoe UI", size=12, slant="italic")

        # fullscreen toggle via F11, exit via Escape
        self.fullscreen = False
        self.bind("<F11>", self._toggle_fullscreen)
        self.bind("<Escape>", lambda e: self._exit_fullscreen())

        # Game / bank state
        self.balance = DEFAULT_BALANCE
        self.bet = 0
        self.total_bet = 0
        self.rounds_played = 0
        self.rounds_completed = 0

        # Round state
        self.user_cards = []
        self.computer_cards = []
        self.is_over = True  # True == no round in progress

        # Build UI
        self._build_top()
        self._build_bet_frame()
        self._build_cards_frame()
        self._build_controls()
        self._update_ui()

    def _build_top(self):
        top = tk.Frame(self)
        top.pack(padx=12, pady=10, fill="x")

        self.lbl_balance = tk.Label(top, text=f"Balance: ${self.balance}", font=self.large_font)
        self.lbl_balance.pack(side="left")

        self.lbl_total = tk.Label(
            top,
            text=f"Total Bet: ${self.total_bet}  Rounds: {self.rounds_played}  Completed: {self.rounds_completed}",
            font=self.medium_font,
        )
        self.lbl_total.pack(side="left", padx=16)

        btn_frame = tk.Frame(top)
        btn_frame.pack(side="right")
        self.btn_reset = tk.Button(btn_frame, text="Reset Bank", command=self._reset_bank)
        self.btn_reset.pack(side="right", padx=(6, 0))
        self.btn_maximize = tk.Button(btn_frame, text="Maximize", command=self._toggle_maximize)
        self.btn_maximize.pack(side="right", padx=(0, 6))

    def _build_bet_frame(self):
        frame = tk.LabelFrame(self, text="Place Bet", padx=10, pady=8)
        frame.pack(padx=12, pady=(0, 10), fill="x")

        tk.Label(frame, text="Coin:").grid(row=0, column=0, sticky="w")
        self.coin_var = tk.IntVar(value=COINS[0])
        coin_menu = tk.OptionMenu(frame, self.coin_var, *COINS)
        coin_menu.config(width=8)
        coin_menu.grid(row=0, column=1, sticky="w", padx=(6, 12))

        tk.Label(frame, text="Count:").grid(row=0, column=2, sticky="w")
        self.count_var = tk.IntVar(value=1)
        count_spin = tk.Spinbox(frame, from_=1, to=1000, textvariable=self.count_var, width=8)
        count_spin.grid(row=0, column=3, sticky="w", padx=(6, 12))

        self.btn_add_coin = tk.Button(frame, text="Add", command=self._add_coin, width=10)
        self.btn_add_coin.grid(row=0, column=4, padx=6)

        self.btn_done_bet = tk.Button(frame, text="Done", command=self._finalize_bet, width=10)
        self.btn_done_bet.grid(row=0, column=5, padx=6)

        tk.Label(frame, text="Current Bet:").grid(row=1, column=0, sticky="w", pady=(8, 0))
        self.lbl_bet = tk.Label(frame, text=f"${self.bet}", font=self.medium_font)
        self.lbl_bet.grid(row=1, column=1, sticky="w", pady=(8, 0))

        tk.Label(frame, text="Available Coins:").grid(row=1, column=2, sticky="w", pady=(8, 0))
        tk.Label(frame, text=", ".join(map(str, COINS))).grid(row=1, column=3, columnspan=3, sticky="w", pady=(8, 0))

    def _build_cards_frame(self):
        frame = tk.Frame(self)
        frame.pack(padx=12, pady=(0, 10), fill="x")

        self.lbl_user = tk.Label(frame, text="Your cards: []  Score: 0", font=self.medium_font)
        self.lbl_user.pack(anchor="w", padx=6, pady=(6, 4))

        self.lbl_computer = tk.Label(frame, text="Computer's first card: ?  Score: ?", font=self.medium_font)
        self.lbl_computer.pack(anchor="w", padx=6, pady=(0, 6))

        self.lbl_status = tk.Label(self, text="Place a bet to start.", font=self.italic_font)
        self.lbl_status.pack(padx=12, pady=(0, 10))

    def _build_controls(self):
        frame = tk.Frame(self)
        frame.pack(padx=12, pady=(0, 12))

        self.btn_deal = tk.Button(frame, text="Deal", width=12, state="disabled", command=self._deal)
        self.btn_deal.grid(row=0, column=0, padx=8)

        self.btn_hit = tk.Button(frame, text="Hit", width=12, state="disabled", command=self._hit)
        self.btn_hit.grid(row=0, column=1, padx=8)

        self.btn_stand = tk.Button(frame, text="Stand", width=12, state="disabled", command=self._stand)
        self.btn_stand.grid(row=0, column=2, padx=8)

        self.btn_quit = tk.Button(frame, text="Quit", width=12, command=self.destroy)
        self.btn_quit.grid(row=0, column=3, padx=8)

    def _update_ui(self, reveal_computer=False):
        try:
            user_score = calculate_score(self.user_cards) if self.user_cards else 0
        except Exception:
            user_score = "?"
        try:
            comp_score = calculate_score(self.computer_cards) if (self.computer_cards and reveal_computer) else "?"
        except Exception:
            comp_score = "?"

        self.lbl_user.config(text=f"Your cards: {self.user_cards}  Score: {user_score}")
        if reveal_computer:
            self.lbl_computer.config(text=f"Computer's cards: {self.computer_cards}  Score: {comp_score}")
        else:
            first = self.computer_cards[0] if self.computer_cards else "?"
            self.lbl_computer.config(text=f"Computer's first card: {first}  Score: {comp_score}")

        self.lbl_balance.config(text=f"Balance: ${self.balance}")
        self.lbl_bet.config(text=f"${self.bet}")
        self.lbl_total.config(text=f"Total Bet: ${self.total_bet}  Rounds: {self.rounds_played}  Completed: {self.rounds_completed}")

        if self.is_over and self.bet > 0:
            self.btn_deal.config(state="normal")
        else:
            self.btn_deal.config(state="disabled")

        if self.is_over:
            self.btn_add_coin.config(state="normal")
            self.btn_done_bet.config(state="normal")
            self.btn_hit.config(state="disabled")
            self.btn_stand.config(state="disabled")
        else:
            self.btn_add_coin.config(state="disabled")
            self.btn_done_bet.config(state="disabled")
            self.btn_hit.config(state="normal")
            self.btn_stand.config(state="normal")

    def _reset_bank(self):
        if messagebox.askyesno("Reset Bank", f"Reset balance to ${DEFAULT_BALANCE}?"):
            self.balance = DEFAULT_BALANCE
            self.total_bet = 0
            self.rounds_played = 0
            self.rounds_completed = 0
            self.bet = 0
            self.user_cards = []
            self.computer_cards = []
            self.is_over = True
            self.lbl_status.config(text="Place a bet to start.")
            self._update_ui()

    def _add_coin(self):
        if not self.is_over:
            self.lbl_status.config(text="Cannot change bet during a round.", fg="red")
            return
        coin = int(self.coin_var.get())
        try:
            count = int(self.count_var.get())
        except Exception:
            count = 1
            self.count_var.set(1)
        addition = coin * count
        if addition <= 0:
            self.lbl_status.config(text="Invalid addition.", fg="red")
            return
        if addition + self.bet > self.balance:
            self.lbl_status.config(text="Bet exceeds current balance!", fg="red")
            return
        self.bet += addition
        self.lbl_status.config(text=f"Building bet: ${self.bet}", fg="black")
        self.lbl_bet.config(text=f"${self.bet}")
        self._update_ui()

    def _finalize_bet(self):
        if not self.is_over:
            return
        if self.bet <= 0:
            messagebox.showwarning("No Bet", "Add coins to your bet before finalizing.")
            return
        self.lbl_status.config(text=f"Bet of ${self.bet} placed. Click DEAL to start the round.", fg="black")
        self._update_ui()

    def _deal(self):
        if not self.is_over:
            return
        if self.bet <= 0:
            messagebox.showwarning("No Bet", "Place a bet before dealing.")
            return
        if self.bet > self.balance:
            messagebox.showerror("Invalid Bet", "Your bet exceeds your balance.")
            return

        # take stake up-front
        self.balance -= self.bet

        # start round
        try:
            self.user_cards = [deal_cards(), deal_cards()]
            self.computer_cards = [deal_cards(), deal_cards()]
        except Exception as ex:
            messagebox.showerror("Deal Error", f"Error dealing cards: {ex}")
            return

        self.is_over = False
        self.lbl_status.config(text="Round started. Hit to draw or Stand to finish.", fg="black")
        self._update_ui(reveal_computer=False)

        try:
            u = calculate_score(self.user_cards)
            c = calculate_score(self.computer_cards)
        except Exception:
            u = c = None

        if u == 0 or c == 0:
            self._end_round()

    def _hit(self):
        if self.is_over:
            return
        try:
            self.user_cards.append(deal_cards())
        except Exception as ex:
            messagebox.showerror("Hit Error", f"Error drawing card: {ex}")
            return
        if calculate_score(self.user_cards) > 21:
            self._end_round()
        self._update_ui(reveal_computer=False)

    def _stand(self):
        if self.is_over:
            return
        # dealer plays
        try:
            while calculate_score(self.computer_cards) != 0 and calculate_score(self.computer_cards) < 17 and calculate_score(self.user_cards) <= 21:
                self.computer_cards.append(deal_cards())
        except Exception as ex:
            messagebox.showerror("Dealer Error", f"Error during dealer play: {ex}")
        self._end_round()

    def _end_round(self):
        if self.is_over:
            return
        self.is_over = True

        try:
            user_score = calculate_score(self.user_cards)
            computer_score = calculate_score(self.computer_cards)
        except Exception as ex:
            messagebox.showerror("Scoring Error", f"Error calculating scores: {ex}")
            return

        self._update_ui(reveal_computer=True)
        message, winner = compare_scores(user_score, computer_score)

        if winner == "user":
            self.balance += self.bet * 2
            self.lbl_status.config(text=f"You win! {message}", fg="green")
        elif winner == "computer":
            self.lbl_status.config(text=f"You lose! {message}", fg="red")
        else:
            self.balance += self.bet
            self.lbl_status.config(text=f"Push! {message}", fg="blue")

        self.total_bet += self.bet
        self.rounds_played += 1
        self.rounds_completed += 1

        messagebox.showinfo("Round Result", f"{message}\n\nBet: ${self.bet}\nNew Balance: ${self.balance}")

        self.bet = 0
        self.lbl_bet.config(text=f"${self.bet}")
        self._update_ui()

        if self.balance <= 0:
            try:
                determine_level(self.total_bet, self.rounds_played, DEFAULT_BALANCE)
            except Exception:
                # ignore determine_level errors (console summary helper)
                pass
            restart = messagebox.askyesno("Bankrupt", "Your balance is 0. Restart with default balance?")
            if restart:
                self.balance = DEFAULT_BALANCE
                self.total_bet = 0
                self.rounds_played = 0
                self.rounds_completed = 0
                self.lbl_status.config(text="Balance reset. Place a bet to continue.")
                self._update_ui()
            else:
                self.lbl_status.config(text="Game over. Reset balance to play again.")
                self.btn_add_coin.config(state="disabled")
                self.btn_done_bet.config(state="disabled")
                self.btn_deal.config(state="disabled")
        else:
            self.lbl_status.config(text="Place a bet to start the next round.")
            self._update_ui()

    # fullscreen / maximize helpers
    def _toggle_fullscreen(self, _event=None):
        self.fullscreen = not self.fullscreen
        self.attributes("-fullscreen", self.fullscreen)

    def _exit_fullscreen(self):
        if self.fullscreen:
            self.fullscreen = False
            self.attributes("-fullscreen", False)

    def _toggle_maximize(self):
        try:
            if self.state() == "zoomed":
                self.state("normal")
            else:
                self.state("zoomed")
        except Exception:
            self._toggle_fullscreen()


if __name__ == "__main__":
    app = BlackjackGUI()
    app.mainloop()