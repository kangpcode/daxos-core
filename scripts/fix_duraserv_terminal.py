#!/usr/bin/env python3
from pathlib import Path
import re

INDEX_HTML = Path("src/ui/desktop_preview/index.html")
text = INDEX_HTML.read_text(encoding="utf-8")

pattern = re.compile(r"if \(cmd === 'duraserv'\) \{[\s\S]*?if \(cmd === 'service' \|\| cmd === 'systemctl'\) \{")

replacement = r'''if (cmd === 'duraserv') {
        const sub = args[0] ? args[0].toLowerCase() : 'status';
        if (sub === 'status') {
          termHistory.textContent += `================================================================================\n  DAXOS DURASERV WEB SERVER & DEVELOPER STACK (Laragon & FlyEnv Parity)\n================================================================================\nSERVICE         VERSION     PORT       STATUS             PID    UPTIME\n--------------------------------------------------------------------------------\nNginx Proxy     1.26.2      80, 443    [RUNNING] ACTIVE   1120   04h:28m\nPHP-FPM (JIT)   8.3.12      9000       [RUNNING] ACTIVE   1124   04h:28m\nMySQL Server    8.4.2 LTS   3306       [RUNNING] ACTIVE   1130   04h:28m\nPostgreSQL      17.0        5432       [RUNNING] ACTIVE   1135   04h:28m\nRedis Cache     7.4.1       6379       [RUNNING] ACTIVE   1140   04h:28m\nNode.js (PM2)   22.9.0      3000       [STANDBY] READY    -      -\nGolang Server   1.23.2      8081       [STANDBY] READY    -      -\nV-Lang (Vweb)   0.4.8       8082       [STANDBY] READY    -      -\nPython ASGI     3.14.0      8000       [STANDBY] READY    -      -\n--------------------------------------------------------------------------------\nWeb Root     : /var/www/html, ~/Sites\nVirtual Hosts: http://localhost, http://daxos.test, http://api.daxos.test (Auto-SSL)\nDatabase GUI : Adminer 4.8.1 (http://localhost/adminer)\n`;
        } else if (sub === 'start') {
          if (typeof duraServToggleAll === 'function') duraServToggleAll();
          termHistory.textContent += "[DURASERV OK] Memulai seluruh stack layanan (Nginx, PHP 8.3, MySQL, Postgres, Redis)...\nSemua socket siap mendengarkan koneksi pada port 80, 443, 3306, 5432, 6379, 9000.\n";
        } else if (sub === 'stop') {
          if (typeof duraServToggleAll === 'function') duraServToggleAll();
          termHistory.textContent += "[DURASERV OK] Seluruh layanan DuraServ berhasil dihentikan secara anggun (SIGTERM SLA < 25 ms).\n";
        } else if (sub === 'php') {
          const ver = args[1] || '8.3';
          if (typeof duraServSwitchPhp === 'function') duraServSwitchPhp(ver);
          termHistory.textContent += `[DURASERV OK] Versi PHP sistem dialihkan ke PHP ${ver} (CLI & FPM OpCache JIT diaktifkan).\n`;
        } else {
          termHistory.textContent += "Penggunaan: duraserv [status|start|stop|restart|php <versi>|vhost|logs]\n";
        }
        if (termPane) termPane.scrollTop = termPane.scrollHeight;
        return;
      }

      // Handle Service and Systemctl
      if (cmd === 'service' || cmd === 'systemctl') {'''

text = pattern.sub(lambda m: replacement, text)
INDEX_HTML.write_text(text, encoding="utf-8")
print("Cleaned and escaped duraserv terminal handler.")
