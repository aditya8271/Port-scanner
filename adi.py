from flask import Flask, request, jsonify, render_template_string
import socket
import threading

app = Flask(__name__)

HTML_PAGE = """
<!DOCTYPE html>
<html lang="en" >
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Port Scanner </title>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');

    :root {
      --background: #0f172a;
      --card-bg: #1e293b;
      --accent-color: #14b8a6;
      --accent-color-light: #22d3ee;
      --text-color: #e0e7ff;
      --text-color-muted: #94a3b8;
      --danger-color: #ef4444;
      --border-radius: 12px;
      --font-family: 'Poppins', sans-serif;
      --transition-speed: 0.3s;
      --shadow: 0 8px 24px rgb(20 184 166 / 0.4);
    }

    * {
      box-sizing: border-box;
    }

    body {
      margin: 0;
      background-color: var(--background);
      font-family: var(--font-family);
      color: var(--text-color);
      display: flex;
      justify-content: center;
      align-items: flex-start;
      min-height: 100vh;
      padding: 2rem 1rem 4rem;
      -webkit-font-smoothing: antialiased;
      -moz-osx-font-smoothing: grayscale;
    }

    .container {
      width: 100%;
      max-width: 480px;
      background: var(--card-bg);
      border-radius: var(--border-radius);
      padding: 2rem 2.5rem;
      box-shadow: var(--shadow);
      text-align: center;
      position: relative;
      overflow: hidden;
    }

    h1 {
      font-weight: 600;
      margin-bottom: 0.35rem;
      font-size: 2rem;
      letter-spacing: 1.5px;
      color: var(--accent-color-light);
      text-transform: uppercase;
      user-select: none;
    }

    p.subtitle {
      color: var(--text-color-muted);
      margin-top: 0;
      margin-bottom: 2rem;
      font-weight: 400;
      font-size: 1rem;
    }

    form {
      display: flex;
      flex-direction: column;
      gap: 1.2rem;
    }

    label {
      text-align: left;
      font-size: 0.9rem;
      color: var(--text-color-muted);
      user-select: none;
    }

    input[type="text"],
    input[type="number"] {
      width: 100%;
      padding: 0.6rem 1rem;
      background-color: #2e3a59;
      border: none;
      border-radius: 0.75rem;
      color: var(--text-color);
      font-size: 1rem;
      transition: background-color var(--transition-speed);
      font-weight: 500;
    }
    input[type="text"]::placeholder,
    input[type="number"]::placeholder {
      color: var(--text-color-muted);
      font-weight: 400;
    }
    input[type="text"]:focus,
    input[type="number"]:focus {
      outline: none;
      background-color: #3b4b79;
      box-shadow: 0 0 8px var(--accent-color);
      color: white;
      font-weight: 600;
    }

    button.scan-btn {
      margin-top: 1rem;
      padding: 0.75rem 1rem;
      font-size: 1.2rem;
      font-weight: 600;
      background: linear-gradient(45deg, #14b8a6, #22d3ee);
      border: none;
      border-radius: var(--border-radius);
      cursor: pointer;
      color: white;
      box-shadow: 0 6px 12px rgb(18 214 204 / 0.6);
      transition: all var(--transition-speed) ease-in-out;
      position: relative;
      overflow: hidden;
      user-select: none;
      z-index: 0;
    }
    button.scan-btn::before {
      content: "";
      position: absolute;
      top: 0;
      left: -75%;
      width: 50%;
      height: 100%;
      background: linear-gradient(
        120deg,
        rgba(255,255,255,0.35),
        rgba(255,255,255,0.1),
        rgba(255,255,255,0.35)
      );
      transform: skewX(-20deg);
      transition: all 0.5s ease-in-out;
      z-index: 1;
      pointer-events: none;
    }
    button.scan-btn:hover::before {
      left: 150%;
    }
    button.scan-btn:hover {
      box-shadow: 0 8px 20px rgb(34 211 238 / 0.8);
    }
    button.scan-btn:disabled {
      background: #6b7280;
      cursor: not-allowed;
      box-shadow: none;
    }

    #results {
      margin-top: 1.5rem;
      background-color: #17233d;
      padding: 1rem 1.25rem;
      border-radius: 1rem;
      min-height: 80px;
      color: var(--accent-color-light);
      font-family: 'Courier New', Courier, monospace;
      font-size: 1.05rem;
      box-shadow: 0 4px 20px rgb(20 184 166 / 0.25);
      user-select: text;
      position: relative;
      overflow-wrap: break-word;
    }
    #results.fade-in {
      animation: fadeInText 0.5s ease forwards;
    }
    @keyframes fadeInText {
      from {opacity: 0; transform: translateY(12px);}
      to {opacity: 1; transform: translateY(0);}
    }

    .error {
      color: var(--danger-color);
      font-weight: 600;
    }

    /* Scanning animation area */
    .scanner {
      margin-top: 2rem;
      height: 24px;
      position: relative;
      background: linear-gradient(90deg, #344563, #3e5068, #344563);
      border-radius: 12px;
      overflow: hidden;
      user-select: none;
    }
    .scanner-line {
      position: absolute;
      top: 0;
      left: -50%;
      width: 50%;
      height: 100%;
      background: linear-gradient(
        90deg,
        transparent 0%,
        var(--accent-color-light) 50%,
        transparent 100%
      );
      animation: scanAnim 2s linear infinite;
      filter: drop-shadow(0 0 4px var(--accent-color-light));
      border-radius: 12px;
    }
    @keyframes scanAnim {
      0% { left: -50%; }
      100% { left: 150%; }
    }

    /* Responsive */
    @media (max-width: 600px) {
      .container {
        padding: 1.5rem 1.8rem;
      }
      button.scan-btn {
        font-size: 1.1rem;
      }
    }
  </style>
</head>
<body>
  <main class="container" role="main" aria-label="Port Scanner Application">
    <h1>Port Scanner</h1>
    <p class="subtitle">Scan open TCP ports on a target host quickly</p>

    <form id="scanForm" aria-describedby="results" autocomplete="off">
      <label for="host">Target Host (IP address or domain):</label>
      <input type="text" id="host" name="host" placeholder="e.g. 192.168.1.1 or example.com" required aria-required="true" aria-label="Target Host" autocomplete="off" />

      <label for="startPort">Start Port (1-65535):</label>
      <input type="number" id="startPort" name="startPort" min="1" max="65535" value="1" required aria-required="true" aria-label="Start Port" />

      <label for="endPort">End Port (1-65535):</label>
      <input type="number" id="endPort" name="endPort" min="1" max="65535" value="1024" required aria-required="true" aria-label="End Port" />

      <button type="submit" class="scan-btn" aria-live="polite" aria-busy="false">Start Scan</button>
    </form>

    <div class="scanner" aria-hidden="true" style="display:none;">
      <div class="scanner-line"></div>
    </div>

    <pre id="results" aria-live="polite" aria-atomic="true"></pre>
  </main>

  <script>
    const form = document.getElementById('scanForm');
    const resultsDiv = document.getElementById('results');
    const scanButton = form.querySelector('button.scan-btn');
    const scannerAnimation = document.querySelector('.scanner');

    form.addEventListener('submit', async e => {
      e.preventDefault();

      resultsDiv.textContent = '';
      resultsDiv.classList.remove('fade-in');
      scannerAnimation.style.display = 'block';
      scanButton.disabled = true;
      scanButton.setAttribute('aria-busy', 'true');

      const host = form.host.value.trim();
      const startPort = Number(form.startPort.value);
      const endPort = Number(form.endPort.value);

      if (
        startPort < 1 || startPort > 65535 ||
        endPort < 1 || endPort > 65535 ||
        startPort > endPort
      ) {
        scannerAnimation.style.display = 'none';
        resultsDiv.innerHTML = '<span class="error">Please enter a valid port range between 1 and 65535, and ensure start port is less than or equal to end port.</span>';
        scanButton.disabled = false;
        scanButton.setAttribute('aria-busy', 'false');
        return;
      }

      try {
        const res = await fetch('/scan', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({ host, startPort, endPort })
        });

        const data = await res.json();

        scannerAnimation.style.display = 'none';
        scanButton.disabled = false;
        scanButton.setAttribute('aria-busy', 'false');

        if (data.error) {
          resultsDiv.innerHTML = '<span class="error">' + data.error + '</span>';
        } else {
          if (data.open_ports.length === 0) {
            resultsDiv.textContent = "No open ports found in the specified range.";
          } else {
            resultsDiv.textContent = 'Open Ports: ' + data.open_ports.join(', ');
          }
          resultsDiv.classList.add('fade-in');
        }
      } catch(err) {
        scannerAnimation.style.display = 'none';
        resultsDiv.innerHTML = '<span class="error">Error scanning ports: ' + err.message + '</span>';
        scanButton.disabled = false;
        scanButton.setAttribute('aria-busy', 'false');
      }
    });
  </script>
</body>
</html>
"""

def scan_port(host, port, timeout=0.5):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            result = sock.connect_ex((host, port))
            return result == 0
    except Exception:
        return False

def threaded_scan(host, ports):
    open_ports = []
    threads = []
    lock = threading.Lock()

    def check_port(port):
        if scan_port(host, port):
            with lock:
                open_ports.append(port)

    for port in ports:
        t = threading.Thread(target=check_port, args=(port,))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    return sorted(open_ports)

@app.route('/')
def index():
    return render_template_string(HTML_PAGE)

@app.route('/scan', methods=['POST'])
def scan():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data provided'}), 400

    host = data.get('host', '').strip()
    start_port = data.get('startPort')
    end_port = data.get('endPort')

    if not host:
        return jsonify({'error': 'Host is required'}), 400

    try:
        start_port = int(start_port)
        end_port = int(end_port)
    except (ValueError, TypeError):
        return jsonify({'error': 'Ports must be integers'}), 400

    if not (1 <= start_port <= 65535) or not (1 <= end_port <= 65535) or start_port > end_port:
        return jsonify({'error': 'Invalid port range'}), 400

    try:
        socket.gethostbyname(host)
    except socket.gaierror:
        return jsonify({'error': 'Invalid host provided'}), 400

    ports = range(start_port, end_port + 1)
    open_ports = threaded_scan(host, ports)

    return jsonify({'open_ports': open_ports})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
