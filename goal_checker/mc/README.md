# *py_MC* model checker

The *py_MC* model checker verifies traces against DLTL (Data-aware Linear
Temporal Logic) formulas.

## ➡️ Usage

```
> python MC.py [parameters]
```

- If no parameters are provided, a help message is shown.
- Parameters must be provided as key=value pairs, separated by spaces.

 

 Parameters	:	Description       				| Default value  
 ---------------------------------------------- | ------------- 
🔴 `log-file=<filename>` : The name of the log file (without the `.mod` suffix). | No value. **Required** 
🟡 `multi-line=<true\|false>` : Allows formulas to span multiple lines. Formulas must be terminated with a `$` character. 	| false
🟡 `interactive=<true\|false>` : Starts the model checker in interactive mode. 		| true
🟡 `init-file=<path>` : Path to a file containing initial setup commands. Must include the file suffix/extension. 			| ""
🟡 `formula-file=<path>` : Path to a file containing DLTL formulas to check. Must include the file suffix/extension. 			| ""

*Example (with required param only):*
```
> python MC.py log-file=system_trace
```
where `system_trace.mod` file is the trace model to be checked.

## 📜 Trace model input format
The trace model is stored in a `.mod` file and follows a strict comma-separated format:

- Line 1:   Attribute Headers List (defines columns and types)
- Lines 2-:  Log Events (one event per line)

### Line 1: Attribute Headers
The first character indicates the data type, followed by the attribute name:

Data types	| Description
------------| -----------
`a`			| The attribute is an atomic proposition.
`s`			| The attribute is a string.
`n`			| The attribute is a number (treated as a float).
`b`			| The attribute is a boolean.
`@`			| The attribute is a set of strings (e.g., `item1;item2`).
`$`			| The attribute is a dictionary of "key=value" pairs (e.g., `name=John;age=34`).

#### Note on Missing Values:
- Numeric attributes default to `0`.
- Boolean attributes default to `False`.
- String attributes default to `''`(empty string).

### Lines 2-: Log Events
Format: 
```
trace_id,event_name&attribute_1&attribute_2&attribute_3...
```

*Model example:*
```
aE,nV,@att,$p
id0,a&4&a;1&a=1;b=2
id0,a&1&a;1&a=1;b=3
id1,a&4&a;1&a=1;b=5
id1,a&1&a;1&a=1;b=2
id1,b&1&h;2&a=1;b=2
id1,a&1&a;3&a=1;b=2
id1,a&1&a;4&a=1;b=7
id1,b&1&a;1&a=1;b=1
id2,b&2&a;2&a=3;b=3
id2,b&2&234;3;j&a=1;b=2
```

## ⚙️ DLTL formulas syntax

### 💬 Propositions

- Any atomic proposition. These correspond to the values appearing in colums of type attribute
- Any function returning a boolean and involving event attributes. These functions (non-atomic propositions) must be written in a lambda-definition style, with Python syntax. This will be shown later on.


### 🔣 Operators

#### Logic

Syntax  | Operator
------  | --------
`! f`     | NOT f
`f \| g`   | f OR g
`f & g`   | f AND g
`f -> g`  | If f then g
`f <-> g` | f if and only if g

#### Linear Temporal Logic (LTL)

Syntax    | Operator
--------- | --------
`G f`     | Always f (Globally, future)
`H f`     | f happens for every past state (Historical Always)
`F f`     | Eventually f will happen (Future)
`O f`     | f happened in the past (Once)
`X f`     | f happens at the Next event (False for the last event)
`Y f`     | f happened at the previous event (False for the first event)
`f U g`   | f happens Until g is met
`f S g`   | g happens Since f happened

**Note:** Parentheses can be used for grouping expressions.

#### 🧊 Freeze Operator

The freeze operator binds the value of a non-atomic attribute at a specific trace
position to a variable (z) for use in a sub-formula.

Syntax    		| Variable
----------------|---------
`z.(<formula>)`  | Any value in the range a-z can be used as the identifier.

*Example of DLTL formulas:*
```
F a & x.("(x)x[V]<=34+7")
F x.("(x)x[p]['b']==22")
F x.("(x)x[p]['a']>0")
F x.("(x)x[p]['a']>9")
F x.("(x)'z' in x[att]")
F x.(b & "(x)    x[p]['a']>9")
a | b & x.("(x)x[V]==4 or x[V]==2")
F b & x.(F y.(a & "(x,y)x[V]==y[V]"))
F ((a | b) & z.((X false) & "(z)z[#] == 2"))
F ((a | b) & z.((X false) & F y.("(z,y)z[#] == y[#]")))
F x.(b & "(x)PROP.IN_DIC(x[p],'b',22)")
F x.(b & "(x)PROP.IN_DIC_2(x,p,'b',22)")
```

**Note 1:** 
When using freeze variables, for instance `x`, to refer to specific events the way to get access to the attributes will by means of expressions of the form `x[<attribute_name>]`, as in the example above.

**Note 2:** 
By default, `my_propositions.py` module is imported at booting time as `PROP`. 
This file is the place to write the Python functions used in the non-atomic propositions.
In the examples, we are assuming that both, `IN_DIC` and `IN_DIC_2`
are defined in `my_propositions.py`.

## 📚 Reference
The theoretical foundations are described in the following paper:

J. M. Couvreur, J. Ezpeleta --
[*A Linear Temporal Logic Model Checking Method over Finite Words with Correlated
Transition Attributes*](https://hal.science/hal-01944569v1), 
Proceedings of the 7th International Symposium on Data-driven Process Discovery
and Analysis (SIMPDA 2017), Neuchâtel, Switzerland, December 6-8, 2017,
ISSN: 1613-0073, Lecture Notes in Business Information Processing, Vol. 340,
Springer, Paolo Ceravolo, Maurice van Keulen and Kilian Stoffel (Eds.), 2019
