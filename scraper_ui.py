#!/usr/bin/env python3
"""Simple Tkinter UI to run scraper.py with live output."""

import queue
import subprocess
import sys
import threading
import tkinter as tk
from pathlib import Path
from tkinter import font, scrolledtext, ttk

SCRAPER = Path(__file__).parent / "scraper.py"
PYTHON = sys.executable
BG = "#1e1b4b"
BG2 = "#2d2a5e"
ACCENT = "#7c3aed"
ACCENT2 = "#a78bfa"
FG = "#e0e7ff"
FG2 = "#9ca3af"
GREEN = "#34d399"
RED = "#f87171"
YELLOW = "#fbbf24"


class ScraperApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ဖြူနီဝါပြာ Music Scraper")
        self.configure(bg=BG)
        self.resizable(True, True)
        self.minsize(640, 480)

        self._process: subprocess.Popen | None = None
        self._q: queue.Queue = queue.Queue()

        self._build_ui()
        self._poll_queue()

    # ── UI layout ─────────────────────────────────────────────────────────────

    def _build_ui(self):
        header_font = font.Font(family="Segoe UI", size=13, weight="bold")
        label_font  = font.Font(family="Segoe UI", size=10)
        mono_font   = font.Font(family="Consolas", size=9)

        # ── Header ──────────────────────────────────────────────────────────
        hdr = tk.Frame(self, bg=BG2, pady=10)
        hdr.pack(fill="x")
        tk.Label(hdr, text="🎵  ဖြူနီဝါပြာ Music Scraper",
                 bg=BG2, fg=FG, font=header_font).pack(side="left", padx=16)
        tk.Label(hdr, text="phyuniwarpyar.blogspot.com",
                 bg=BG2, fg=ACCENT2, font=label_font).pack(side="right", padx=16)

        # ── Options bar ─────────────────────────────────────────────────────
        opts = tk.Frame(self, bg=BG, padx=16, pady=10)
        opts.pack(fill="x")

        self._resume_var  = tk.BooleanVar(value=False)
        self._verbose_var = tk.BooleanVar(value=True)
        self._limit_var   = tk.StringVar(value="")

        def cb(text, var):
            c = tk.Checkbutton(opts, text=text, variable=var,
                               bg=BG, fg=FG, selectcolor=ACCENT,
                               activebackground=BG, activeforeground=FG,
                               font=label_font)
            c.pack(side="left", padx=(0, 16))

        cb("--resume  (skip already-scraped URLs)", self._resume_var)
        cb("--verbose  (print per-entry details)",  self._verbose_var)

        tk.Label(opts, text="--limit:", bg=BG, fg=FG2,
                 font=label_font).pack(side="left")
        limit_entry = tk.Entry(opts, textvariable=self._limit_var, width=6,
                               bg=BG2, fg=FG, insertbackground=FG,
                               relief="flat", font=label_font)
        limit_entry.pack(side="left", padx=(4, 4))
        tk.Label(opts, text="(blank = all posts)", bg=BG, fg=FG2,
                 font=label_font).pack(side="left")

        # ── Buttons ─────────────────────────────────────────────────────────
        btn_frame = tk.Frame(self, bg=BG, padx=16, pady=4)
        btn_frame.pack(fill="x")

        self._run_btn = tk.Button(
            btn_frame, text="▶  Run Scraper", command=self._run,
            bg=ACCENT, fg="white", activebackground="#6d28d9",
            activeforeground="white", relief="flat",
            font=font.Font(family="Segoe UI", size=10, weight="bold"),
            padx=16, pady=6, cursor="hand2")
        self._run_btn.pack(side="left", padx=(0, 8))

        self._stop_btn = tk.Button(
            btn_frame, text="■  Stop", command=self._stop,
            bg=BG2, fg=FG2, activebackground="#374151",
            activeforeground=FG, relief="flat",
            font=font.Font(family="Segoe UI", size=10),
            padx=12, pady=6, cursor="hand2", state="disabled")
        self._stop_btn.pack(side="left", padx=(0, 8))

        self._clear_btn = tk.Button(
            btn_frame, text="⌫  Clear", command=self._clear_log,
            bg=BG2, fg=FG2, activebackground="#374151",
            activeforeground=FG, relief="flat",
            font=font.Font(family="Segoe UI", size=10),
            padx=12, pady=6, cursor="hand2")
        self._clear_btn.pack(side="left")

        # ── Output log ──────────────────────────────────────────────────────
        log_frame = tk.Frame(self, bg=BG, padx=16, pady=0)
        log_frame.pack(fill="both", expand=True)

        self._log = scrolledtext.ScrolledText(
            log_frame, bg="#0f0d2e", fg=FG, font=mono_font,
            relief="flat", state="disabled", wrap="word",
            insertbackground=FG)
        self._log.pack(fill="both", expand=True)

        # colour tags for log lines
        self._log.tag_config("info",    foreground=FG)
        self._log.tag_config("ok",      foreground=GREEN)
        self._log.tag_config("warn",    foreground=YELLOW)
        self._log.tag_config("err",     foreground=RED)
        self._log.tag_config("accent",  foreground=ACCENT2)
        self._log.tag_config("dim",     foreground=FG2)

        # ── Status bar ──────────────────────────────────────────────────────
        self._status_var = tk.StringVar(value="Ready")
        status = tk.Label(self, textvariable=self._status_var,
                          bg=BG2, fg=FG2,
                          font=font.Font(family="Segoe UI", size=9),
                          anchor="w", padx=16, pady=4)
        status.pack(fill="x", side="bottom")

    # ── Scraper control ──────────────────────────────────────────────────────

    def _build_cmd(self) -> list[str]:
        cmd = [PYTHON, str(SCRAPER)]
        if self._resume_var.get():
            cmd.append("--resume")
        if self._verbose_var.get():
            cmd.append("--verbose")
        limit = self._limit_var.get().strip()
        if limit:
            cmd += ["--limit", limit]
        return cmd

    def _run(self):
        if self._process and self._process.poll() is None:
            return  # already running

        cmd = self._build_cmd()
        self._log_line(f"$ {' '.join(cmd)}\n", "dim")
        self._set_running(True)

        self._process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=str(SCRAPER.parent),
        )
        threading.Thread(target=self._reader, daemon=True).start()

    def _stop(self):
        if self._process and self._process.poll() is None:
            self._process.terminate()
            self._log_line("\n[Stopped by user]\n", "warn")
            self._set_running(False)

    def _reader(self):
        """Background thread: read process stdout line by line → queue."""
        for line in self._process.stdout:
            self._q.put(line)
        self._process.wait()
        self._q.put(None)  # sentinel

    def _poll_queue(self):
        """Main-thread timer: drain queue → update log widget."""
        try:
            while True:
                line = self._q.get_nowait()
                if line is None:
                    rc = self._process.returncode if self._process else -1
                    if rc == 0:
                        self._log_line("\n✓ Scrape complete.\n", "ok")
                        self._status_var.set("Done")
                    else:
                        self._log_line(f"\n✗ Process exited with code {rc}\n", "err")
                        self._status_var.set(f"Exited ({rc})")
                    self._set_running(False)
                else:
                    self._log_line(line, self._classify(line))
        except queue.Empty:
            pass
        self.after(100, self._poll_queue)

    # ── Helpers ──────────────────────────────────────────────────────────────

    @staticmethod
    def _classify(line: str) -> str:
        l = line.lower()
        if "saved" in l or "✓" in l or "done" in l:
            return "ok"
        if "error" in l or "traceback" in l or "✗" in l:
            return "err"
        if "retry" in l or "warn" in l or "skip" in l:
            return "warn"
        if line.startswith("  [") or line.startswith("    "):
            return "accent"
        if line.startswith("─") or line.startswith("Total") or line.startswith("With"):
            return "ok"
        return "info"

    def _log_line(self, text: str, tag: str = "info"):
        self._log.configure(state="normal")
        self._log.insert("end", text, tag)
        self._log.see("end")
        self._log.configure(state="disabled")

    def _clear_log(self):
        self._log.configure(state="normal")
        self._log.delete("1.0", "end")
        self._log.configure(state="disabled")

    def _set_running(self, running: bool):
        if running:
            self._run_btn.configure(state="disabled", bg="#4c1d95")
            self._stop_btn.configure(state="normal", bg=RED, fg="white")
            self._status_var.set("Running …")
        else:
            self._run_btn.configure(state="normal", bg=ACCENT)
            self._stop_btn.configure(state="disabled", bg=BG2, fg=FG2)


if __name__ == "__main__":
    app = ScraperApp()
    app.geometry("780x560")
    app.mainloop()
