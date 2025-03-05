# Set up

```
python3 -m venv venv
venv/bin/pip install -r requirements.txt 
venv/bin/python -i testing.py
```

# Usage

# Troubleshooting


If at first start you receive the following message:

```text
 venv/bin/python -i testing.py
Starting the browser...
An error occurred: BrowserType.launch: Executable doesn't exist at […]
╔════════════════════════════════════════════════════════════╗
║ Looks like Playwright was just installed or updated.       ║
║ Please run the following command to download new browsers: ║
║                                                            ║
║     playwright install                                     ║
║                                                            ║
║ <3 Playwright Team                                         ║
╚════════════════════════════════════════════════════════════╝
Press Enter to exit...
```

Then run this command: 
`npx playwright install`

after havind made sure that you had [npm command-line interface](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm) installed.


