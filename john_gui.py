import tkinter as tk
from tkinter import filedialog, scrolledtext
from tkinterdnd2 import TkinterDnD, DND_FILES
import subprocess
import threading
import os

# ── hidden config ─────────────────────────────────────────────────────────────
JOHN_EXE = r"C:\Users\SAMRIDHI\Downloads\john-1.9.0-jumbo-1-win64\john-1.9.0-jumbo-1-win64\run\john.exe"

# ── colour palette ────────────────────────────────────────────────────────────
BG          = "#0d0b1a"
BG_CARD     = "#130f28"
BG_CONSOLE  = "#080612"
VIOLET      = "#b86cff"
VIOLET_DIM  = "#4a3270"
VIOLET_GLOW = "#6a3fa0"
AMBER       = "#ffb347"
CORAL       = "#ff5f6d"
TEXT_MAIN   = "#d4c8f0"
TEXT_DIM    = "#5a4d7a"
BORDER      = "#231945"
WHITE       = "#f0ecff"

# ── button factory ────────────────────────────────────────────────────────────
def styled_btn(parent, text, cmd, color=VIOLET, width=18, pady_val=9):
    b = tk.Button(
        parent, text=text, command=cmd,
        font=("Segoe UI", 9, "bold"),
        fg=color, bg=BG_CARD,
        activeforeground=BG, activebackground=color,
        relief="flat", bd=0, cursor="hand2",
        width=width, pady=pady_val,
        highlightthickness=1, highlightbackground=color
    )
    b.bind("<Enter>", lambda e: b.config(bg=color, fg=BG))
    b.bind("<Leave>", lambda e: b.config(bg=BG_CARD, fg=color))
    return b

# ── console helpers ───────────────────────────────────────────────────────────
def log(text, tag="default"):
    console.config(state="normal")
    console.insert(tk.END, text + "\n", tag)
    console.see(tk.END)
    console.config(state="disabled")

def clear_console():
    console.config(state="normal")
    console.delete("1.0", tk.END)
    console.config(state="disabled")

def copy_logs():
    content = console.get("1.0", tk.END).strip()
    if content:
        root.clipboard_clear()
        root.clipboard_append(content)
        set_status("  Logs copied to clipboard.", VIOLET)

def set_status(msg, color=TEXT_DIM):
    status_var.set(msg)
    status_lbl.config(fg=color)

# ── result box animation ──────────────────────────────────────────────────────
_blink_job   = None
_blink_state = False

def _blink_border():
    global _blink_job, _blink_state
    _blink_state = not _blink_state
    col = CORAL if _blink_state else "#7a1020"
    result_box.config(highlightbackground=col)
    result_pw_lbl.config(fg=col if _blink_state else AMBER)
    _blink_job = root.after(420, _blink_border)

def _stop_blink():
    global _blink_job
    if _blink_job:
        root.after_cancel(_blink_job)
        _blink_job = None
    result_box.config(highlightbackground=CORAL)
    result_pw_lbl.config(fg=AMBER)

def show_result(password):
    _stop_blink()
    result_pw_lbl.config(text=password)
    result_found_lbl.config(text="⚠  PASSWORD CRACKED", fg=CORAL)
    result_box.config(highlightbackground=CORAL)
    _blink_border()

def show_result_failed():
    _stop_blink()
    result_pw_lbl.config(text="Not found", fg=TEXT_DIM)
    result_found_lbl.config(text="Password not recovered", fg=TEXT_DIM)
    result_box.config(highlightbackground=BORDER)

def reset_result():
    _stop_blink()
    result_pw_lbl.config(text="—", fg=TEXT_DIM)
    result_found_lbl.config(text="Waiting for result...", fg=TEXT_DIM)
    result_box.config(highlightbackground=BORDER)

# ── file handling ─────────────────────────────────────────────────────────────
def set_file(path):
    path = path.strip().strip("{}")
    if not path or not os.path.isfile(path):
        return
    file_var.set(path)
    name = os.path.basename(path)
    drop_lbl.config(text=f"✦  {name}", fg=AMBER)
    clear_btn.pack(pady=(0, 6))
    set_status(f"  File ready: {name}", VIOLET)

def browse_file():
    path = filedialog.askopenfilename(
        title="Select Hash File",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
    )
    if path:
        set_file(path)

def clear_file():
    file_var.set("")
    drop_lbl.config(text="Drag & drop a file here\nor click  Browse", fg=TEXT_DIM)
    clear_btn.pack_forget()
    set_status("  File cleared.", TEXT_DIM)

def on_drop(event):
    set_file(event.data)

# ── cracking logic ────────────────────────────────────────────────────────────
def start_crack():
    filepath = file_var.get().strip()
    if not filepath:
        set_status("  Please select or drop a hash file first.", CORAL)
        return

    clear_console()
    reset_result()
    crack_btn.config(state="disabled")
    set_status("  Decrypting...  please wait.", AMBER)

    log("  ◈  Starting crack session", "violet")
    log(f"  ◈  Target  →  {os.path.basename(filepath)}", "violet")
    log("  " + "─" * 52, "dim")

    def worker():
        try:
            subprocess.run(
                [JOHN_EXE, "--format=Raw-MD5", filepath],
                capture_output=True, text=True, timeout=60
            )
            show = subprocess.run(
                [JOHN_EXE, "--show", "--format=Raw-MD5", filepath],
                capture_output=True, text=True
            )
            result = show.stdout.strip()

            if result:
                lines     = result.splitlines()
                passwords = [l for l in lines if ":" in l and "password hash" not in l.lower()]
                summary   = [l for l in lines if "password hash" in l.lower()]

                if passwords:
                    log("", "dim")
                    log("  ◈  PASSWORD RECOVERED", "amber")
                    log("  " + "─" * 52, "dim")
                    cracked_vals = []
                    for p in passwords:
                        parts = p.split(":", 1)
                        val = parts[1] if len(parts) == 2 else p
                        cracked_vals.append(val)
                        log(f"  ➤  {val}", "amber")
                    log("", "dim")
                    root.after(0, lambda v="\n".join(cracked_vals): show_result(v))
                else:
                    root.after(0, show_result_failed)
                for s in summary:
                    log(f"  {s}", "dim")
            else:
                log("  ✖  No matching password found in dictionary.", "coral")
                log("  Consider trying a different file or hash type.", "dim")
                root.after(0, show_result_failed)

        except subprocess.TimeoutExpired:
            log("  ✖  Operation timed out.", "coral")
        except Exception as ex:
            log(f"  ✖  Error: {ex}", "coral")
        finally:
            root.after(0, lambda: crack_btn.config(state="normal"))
            root.after(0, lambda: set_status("  Session complete.", VIOLET))

    threading.Thread(target=worker, daemon=True).start()

# ══════════════════════════════════════════════════════════════════════════════
#  ROOT WINDOW
# ══════════════════════════════════════════════════════════════════════════════
root = TkinterDnD.Tk()
root.title("Password Cracking Application — Cyber Security Mini Project")
root.geometry("720x760")
root.minsize(640, 680)
root.configure(bg=BG)
root.resizable(True, True)

# ── header ────────────────────────────────────────────────────────────────────
tk.Label(root, text="🔐",
         font=("Segoe UI", 44), fg=VIOLET, bg=BG).pack(pady=(24, 0))

tk.Label(root, text="Password Cracking Application",
         font=("Segoe UI", 22, "bold"), fg=WHITE, bg=BG).pack(pady=(6, 2))

tk.Label(root, text="Powered by John the Ripper",
         font=("Segoe UI", 10), fg=VIOLET, bg=BG).pack()

tk.Label(root, text="Cyber Security Mini Project",
         font=("Segoe UI", 9), fg=TEXT_DIM, bg=BG).pack(pady=(2, 0))

tk.Label(root, text="Made by Samridhi",
         font=("Segoe UI", 8, "italic"), fg=VIOLET_DIM, bg=BG).pack(pady=(2, 0))

# decorative divider
div = tk.Frame(root, bg=BG)
div.pack(pady=12)
tk.Label(div, text="◆", font=("Segoe UI", 7), fg=VIOLET_DIM, bg=BG).pack(side="left", padx=4)
tk.Frame(div, bg=BORDER, width=190, height=1).pack(side="left")
tk.Label(div, text="◆", font=("Segoe UI", 7), fg=VIOLET,    bg=BG).pack(side="left", padx=4)
tk.Frame(div, bg=BORDER, width=190, height=1).pack(side="left")
tk.Label(div, text="◆", font=("Segoe UI", 7), fg=VIOLET_DIM, bg=BG).pack(side="left", padx=4)

# ── step 1 card ───────────────────────────────────────────────────────────────
card1 = tk.Frame(root, bg=BG_CARD, highlightthickness=1, highlightbackground=BORDER)
card1.pack(padx=50, pady=(0, 6), fill="x")

tk.Label(card1, text="STEP 1  —  SELECT A HASH FILE",
         font=("Segoe UI", 8, "bold"), fg=TEXT_DIM, bg=BG_CARD, anchor="w"
         ).pack(fill="x", padx=20, pady=(14, 8))

drop_zone = tk.Frame(card1, bg=BG_CONSOLE,
                     highlightthickness=1, highlightbackground=VIOLET_GLOW)
drop_zone.pack(padx=20, fill="x")

file_var  = tk.StringVar()
drop_lbl  = tk.Label(drop_zone, text="Drag & drop a file here\nor click  Browse",
                     font=("Segoe UI", 9), fg=TEXT_DIM, bg=BG_CONSOLE,
                     pady=18, justify="center")
drop_lbl.pack(fill="x")

drop_zone.drop_target_register(DND_FILES)
drop_zone.dnd_bind("<<Drop>>", on_drop)
drop_lbl.drop_target_register(DND_FILES)
drop_lbl.dnd_bind("<<Drop>>", on_drop)

btn_row = tk.Frame(card1, bg=BG_CARD)
btn_row.pack(pady=(8, 14))
styled_btn(btn_row, "  Browse File  ▸", browse_file, VIOLET, 16).pack(side="left", padx=6)
clear_btn = styled_btn(btn_row, "  ✕  Clear File", clear_file, CORAL, 14)

# ── step 2 card ───────────────────────────────────────────────────────────────
card2 = tk.Frame(root, bg=BG_CARD, highlightthickness=1, highlightbackground=BORDER)
card2.pack(padx=50, pady=(4, 6), fill="x")

tk.Label(card2, text="STEP 2  —  CRACK THE PASSWORD",
         font=("Segoe UI", 8, "bold"), fg=TEXT_DIM, bg=BG_CARD, anchor="w"
         ).pack(fill="x", padx=20, pady=(14, 8))

crack_btn = styled_btn(card2, "  Crack Password  ▸", start_crack, AMBER, 22, pady_val=10)
crack_btn.pack(pady=(0, 14))

# ── result spotlight box ──────────────────────────────────────────────────────
result_box = tk.Frame(root, bg=BG_CARD, highlightthickness=2, highlightbackground=BORDER)
result_box.pack(padx=50, pady=(4, 6), fill="x")

result_found_lbl = tk.Label(result_box, text="Waiting for result...",
                            font=("Segoe UI", 8, "bold"), fg=TEXT_DIM, bg=BG_CARD, anchor="w")
result_found_lbl.pack(fill="x", padx=20, pady=(14, 4))

result_pw_lbl = tk.Label(result_box, text="—",
                         font=("Segoe UI", 26, "bold"), fg=TEXT_DIM, bg=BG_CARD)
result_pw_lbl.pack(pady=(0, 16))

# ── step 3 console ────────────────────────────────────────────────────────────
hdr3 = tk.Frame(root, bg=BG)
hdr3.pack(fill="x", padx=50, pady=(8, 4))

tk.Label(hdr3, text="STEP 3  —  VIEW RESULTS", font=("Segoe UI", 8, "bold"),
         fg=TEXT_DIM, bg=BG, anchor="w").pack(side="left")

tk.Button(hdr3, text="📋  Copy Logs", command=copy_logs,
          font=("Segoe UI", 8), fg=VIOLET, bg=BG,
          activeforeground=BG, activebackground=VIOLET,
          relief="flat", bd=0, cursor="hand2",
          highlightthickness=1, highlightbackground=VIOLET_DIM,
          padx=8, pady=2).pack(side="right")

console = scrolledtext.ScrolledText(
    root, font=("Cascadia Code", 9),
    bg=BG_CONSOLE, fg=TEXT_MAIN, insertbackground=VIOLET,
    relief="flat", bd=0, highlightthickness=1, highlightbackground=BORDER,
    state="disabled", wrap="word", selectbackground=VIOLET_GLOW
)
console.pack(fill="both", expand=True, padx=50, pady=(0, 8))

console.tag_config("violet",  foreground=VIOLET)
console.tag_config("amber",   foreground=AMBER)
console.tag_config("coral",   foreground=CORAL)
console.tag_config("dim",     foreground=TEXT_DIM)
console.tag_config("default", foreground=TEXT_MAIN)

# ── status bar ────────────────────────────────────────────────────────────────
sbar = tk.Frame(root, bg=BG_CARD, height=28)
sbar.pack(fill="x", side="bottom")

tk.Label(sbar, text=" ◈ ", font=("Segoe UI", 9), fg=VIOLET, bg=BG_CARD).pack(side="left")

status_var = tk.StringVar(value="  Ready — drop a file or browse to get started.")
status_lbl = tk.Label(sbar, textvariable=status_var,
                      font=("Segoe UI", 8), fg=TEXT_DIM, bg=BG_CARD, anchor="w")
status_lbl.pack(side="left", fill="x", expand=True)

tk.Label(sbar, text="John the Ripper v1.9.0  ",
         font=("Segoe UI", 8), fg=TEXT_DIM, bg=BG_CARD).pack(side="right")

# ── startup console message ───────────────────────────────────────────────────
log("  Welcome — drag & drop or browse for a file containing hashed passwords.", "dim")
log("  ⚠  For educational and authorised use only.", "coral")

root.mainloop()