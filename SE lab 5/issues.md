# Lab 5 -- Static Code Analysis

## Issue Documentation

**Assigned program:** `fare_calculator.py`\
**Analysis tools:** Pylint, Bandit and Flake8\
**Stage:** Findings from the original, unmodified program

### 1. Bandit findings

  ----------------------------------------------------------------------------------------
  Issue          Type /                  Line(s) Description               Fix approach
                 Severity                                                  
  -------------- ------------- ----------------- ------------------------- ---------------
  SSH host key   Security --                  80 `AutoAddPolicy()`         Use host-key
  verification   High                            automatically trusts      verification
  disabled                                       unknown SSH host keys.    with a trusted
                                                 This can expose the       `known_hosts`
                                                 connection to a           file and reject
                                                 man-in-the-middle attack. unknown host
                                                                           keys.

  Possible shell Security --                  82 The command is built by   Validate the
  injection in   Medium                          concatenating `fare_file` filename and
  SSH command                                    into a string passed to   pass it safely;
                                                 `exec_command()`. An      avoid accepting
                                                 unsafe value could alter  arbitrary shell
                                                 the command.              syntax.

  MD5 used for   Security --                  60 MD5 is a weak hash and    Replace MD5
  ticket         Medium                          should not be used where  with SHA-256 if
  checksum                                       collision resistance is   a cryptographic
                                                 required.                 hash is
                                                                           required.

  Unsafe XML     Security --                   2 `xml.sax` is flagged      Use the
  parser import  Low                             because parsing untrusted corresponding
                                                 XML with it can be        `defusedxml`
                                                 vulnerable to XML         parser.
                                                 attacks.                  

  Unsafe XML     Security --                  75 `xml.sax.parseString()`   Replace it with
  parsing call   Medium                          parses the supplied XML   the safe
                                                 text using the standard   `defusedxml`
                                                 SAX parser.               equivalent.
  ----------------------------------------------------------------------------------------

### 2. Pylint findings

  --------------------------------------------------------------------------------------------
  Issue            Type                    Line(s) Description                 Fix approach
  ---------------- ------------- ----------------- --------------------------- ---------------
  Missing module   Code quality                  1 The module has no top-level Add a concise
  docstring                                        description.                module
                                                                               docstring.

  Lambda assigned  Code quality                 14 `baseOf` is assigned a      Replace it with
  to a variable                                    lambda expression.          a named
                                                                               function.

  Non-snake_case   Code quality             14--78 Names such as `baseOf`,     Rename
  identifiers                                      `fareForDistance`,          functions and
                                                   `isPeak`, `journeyFare`,    variables using
                                                   `dailyTotal`, `issueCard`,  `snake_case`,
                                                   `tapOut`, `topUp`,          updating their
                                                   `cheapestRoute`,            call sites.
                                                   `ticketChecksum`,           
                                                   `loadStops` and             
                                                   `pushFaresToGate` do not    
                                                   follow the recommended      
                                                   naming convention.          

  Missing function Code quality             16--85 Functions do not explain    Add useful
  docstrings                                       their purpose, parameters   docstrings to
                                                   or return values.           each function.

  Useless `else`   Code quality                 20 The `for` loop returns when Remove the
  after loop                                       a match is found, so the    `else` and
                                                   `else` is unnecessary in    return the
                                                   this implementation.        fallback value
                                                                               after the loop.

  Unnecessary list Code quality                 37 `sum([f for f in fares])`   Use
  comprehension in                                 creates an unnecessary      `sum(fares)` or
  `sum`                                            intermediate list.          a generator
                                                                               expression.

  Unnecessary `if` Code quality                 39 The code can use the        Use `min()`
  block for                                        built-in `min()` instead of where it
  minimum                                          the conditional assignment. expresses the
                                                                               intended cap
                                                                               correctly.

  Dangerous        Bug / Code                   46 `categories=[]` uses a      Use `None` as
  mutable default  quality                         mutable list as a default   the default and
  argument                                         argument.                   create a new
                                                                               list inside the
                                                                               function.

  Unnecessary      Code quality                 57 The sort key wraps `baseOf` Pass the
  lambda                                           in a lambda even though the function
                                                   function can be passed      directly as the
                                                   directly.                   sort key.

  Missing class    Code quality                 64 `StopHandler` has no        Add a class
  docstring                                        class-level description.    docstring.

  Unused import    Code quality                  1 `os` is imported but not    Remove the
                                                   used.                       unused import.
  --------------------------------------------------------------------------------------------

### 3. Flake8 findings

The original Flake8 report contains **20 violations**:

  --------------------------------------------------------------------------
  Issue         Type                    Line(s) Description    Fix approach
  ------------- ------------- ----------------- -------------- -------------
  Unused import Style / Code                  1 `os` is        Remove the
  (`F401`)      quality                         imported but   import.
                                                never used.    

  Lambda        Style                        14 A lambda       Define a
  assignment                                    expression is  normal
  (`E731`)                                      assigned to a  function
                                                variable.      instead.

  Missing blank Formatting      16, 23, 27, 35, Top-level      Add the
  lines                         43, 46, 52, 56, functions and  required
  (`E302`)                      59, 64, 73, 78, the class are  blank lines.
                                             85 not separated  
                                                by the         
                                                required two   
                                                blank lines.   

  Lines too     Formatting       89, 90, 96, 98 Four lines     Wrap the
  long (`E501`)                                 exceed the     lines while
                                                79-character   preserving
                                                limit.         the code's
                                                               behavior.

  Missing blank Formatting                  100 The required   Add the
  lines after                                   blank lines    required
  definition                                    after a        blank lines.
  (`E305`)                                      top-level      
                                                definition are 
                                                missing.       
  --------------------------------------------------------------------------

### 4. Functional issues noticed while running the original program

These observations came from the program's output. They are **not
Bandit, Pylint or Flake8 findings**.

  -----------------------------------------------------------------------------------------------------
  Issue            Type           Relevant code         Description              Fix approach
  ---------------- -------------- --------------------- ------------------------ ----------------------
  Daily fare cap   Functional bug `dailyTotal()`        The function changes the Apply the cap to the
  is not applied                                        loop variable `f`, but   accumulated total or
                                                        then returns the         implement the intended
                                                        original uncapped        daily-cap calculation
                                                        `total`.                 directly.

  Smart-card       Functional bug `tapOut()`            The displayed balance    Check the available
  balance can                                           becomes `-25` after a    balance before
  become negative                                       trip when the card       deducting the fare and
                                                        starts with Rs. 25.      define the expected
                                                                                 insufficient-balance
                                                                                 behavior.

  Floating-point   Numeric issue  `topUp()`             Adding 0.1 and 0.2       Use `Decimal` for
  currency                                              displays                 currency values and
  representation                                        `0.30000000000000004`.   construct decimal
                                                                                 amounts from strings.

  Boundary         Functional     `fareForDistance()`   The output for exactly 2 Confirm the intended
  behavior in      behavior to                          km is Rs. 20, so the     slab boundaries and
  distance slabs   review                               current `< limit`        use comparisons that
                                                        comparisons place an     match the fare rules.
                                                        exact boundary in the    
                                                        next slab.               
  -----------------------------------------------------------------------------------------------------

### 5. Summary

The original source was analyzed before modification.

-   **Pylint:** score of **5.80/10**.
-   **Bandit:** 5 findings --- 1 High, 3 Medium and 1 Low.
-   **Flake8:** 20 violations.
-   The program also showed functional behavior that should be reviewed,
    including an unapplied daily cap, a negative card balance and
    floating-point currency representation.

The fixes should be made and then verified by rerunning all three tools.
The final Pylint score should be above 9.5, all Bandit findings should
be addressed, and all Flake8 formatting findings should be cleared.

**Note:** The supplied student handout asks for reflection answers but
does not include the actual reflection questions. They should be
obtained from the instructor or the separate reflection prompt rather
than guessed.
