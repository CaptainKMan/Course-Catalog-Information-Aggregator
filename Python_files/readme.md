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

after having made sure that you had [npm command-line interface](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm) installed.


If you recieve this error on Windows:

```text
Course-Catalog-Information-Aggregator\Python_files> npx playwright install
npx : File C:\Program Files\nodejs\npx.ps1 cannot be loaded because running scripts is disabled on this system. For
more information, see about_Execution_Policies at https:/go.microsoft.com/fwlink/?LinkID=135170.
At line:1 char:1
+ npx playwright install
+ ~~~
    + CategoryInfo          : SecurityError: (:) [], PSSecurityException
    + FullyQualifiedErrorId : UnauthorizedAccess
```
Then you need to enable running scripts on your computer. Run this command in an Administrator PowerShell Prompt:
`Set-ExecutionPolicy Unrestricted`

To keep your PC secure when you are done running the script, in the same Administrator prompt, you should run:
`Set-ExecutionPolicy Restricted`


