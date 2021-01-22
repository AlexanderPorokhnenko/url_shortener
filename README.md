URL shortener based on simple Base62 encryption method

Installing:
1. Execute bash-script 'setup_ubuntu.sh' with ```bash 'setup_ubuntu.sh'``` in terminal
2. To execute tests - run ```bash launch_tests```
3. Start server with ```bash launch``` command.

Application contains such endpoints:
1. POST 'api/v1/links'
Required param is 'url'. Optional - lifespan. By default - 90 days.
   API returns json with 'short_url' value.
    
2. GET 'api/v1/<short_url>'
Endpoint redirect to main url using 'short_url'.
   
3. GET 'api/v1/links'
Returns list of all entries in db with all fields - url, short_url, lifespan etc.
   
