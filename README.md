# Requirements
NPM ^5.6.0<br />
Python ^3.5<br />
Pip<br />

# To Install
Download folder, open the folder, and run the following<br />
`pip install -r requirements.txt`

# To use
Import: `var krow = require("krow_package/index.js")`<br />
Search: `await krow.search(QUERY, PAGE, USEID).then(function (result){})`<br />
Parameters: <br />
  1. QUERY: Search term
  2. PAGE: Results page to use
  3. USEID: Boolean, whether to return job IDs or to return actual data (much faster if returing IDs)
