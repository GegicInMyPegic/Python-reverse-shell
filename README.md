<h1>Python Reverse Shell</h1>
<p>A Python-based reverse shell with file transfer capabilities.</p>

  <h2>⚠️ Disclaimer</h2>
	<p>This project is for educational and authorized testing purposes only. Unauthorized use of this tool is illegal. The author is not responsible for any misuse.</p>

  <h2>Features</h2>
	<ul>
        <li>✅ <strong>Device Selection</strong> – Lists available devices to connect to.</li>
        <li>✅ <strong>File Transfer</strong> – Upload and download files between the client and server.</li>
        <li>✅ <strong>Persistent Access</strong> – If running on a Windows-based machine, the file will be copied into the startup folder.</li>
        <li>✅ <strong>Remote Access</strong> – Works over the internet with DDNS and port forwarding.</li>
  </ul>

  <h2>Setup</h2>

  <h3>1️⃣ Configure the Client</h3>
    <p>Update the <code>host</code> variable with your IP address:</p>
    <pre><code>host = "your.ip.address"</code></pre>
    <p>Modify the <code>port</code> variable if needed (ensure it matches the server).</p>
    <p>For external access, set up <strong>DDNS</strong> and <strong>port forwarding</strong> on your router. Then, update <code>host</code> to:</p>
    <pre><code>socket.gethostbyname("your.ddns.host")</code></pre>


  <h3>2️⃣ Commands</h3>
    <ul>
        <li><strong>Download a file:</strong> <code>download &lt;filename&gt;</code></li>
        <li><strong>Upload a file:</strong> <code>upload &lt;filename&gt;</code> (from the <code>server.py</code> directory)</li>
        <li><strong>Exit session:</strong> <code>exit</code> (returns to device selection)</li>
    </ul>

   <h2>Notes</h2>
    <ul>
        <li>If running on Windows, the client script will add itself to the startup folder for persistent access.</li>
        <li>Ensure the firewall allows the chosen port.</li>
    </ul>

  <h2>Bug Reports</h2>
  <p>If you encounter issues, please open an issue on GitHub.</p>
