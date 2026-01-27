# Glassy Crystal Box

## Introduction

*Glassy Crystal Box* is a small tool to facilitate testing code written in any of
the supported languages, without boilerplate or needing language-specific
testing frameworks.

*Glassy Crystal Box* is a CLI tool that runs test cases against functions defined
in their respective source files, using a single JSON configuration file. It is
designed to make testing quick and frictionless, to help iterate and test logic
efficiently and organizedly.

If you've ever thought "I just want to test this specific function", then
*Glassy Crystal Box* is the tool for you.

### General Features

- No additional code needed to test, just configuration
- No framework lock-in
- Language-agnostic
- Quick feedback
- Clear summaries

### How Does it Work?

*Glassy Crystal Box* follows the general procedure detailed down below.

1. Reads the provided JSON configuration file, and runs checks to validate all the
   necessary information was provided correctly (*e.g.* ensures no missing fields,
   ensures the given files exist, etc.).

2. Locates the specified source files and extracts the specified functions. This
   process varies from language to language. For instance, Python functions can
   be imported directly into the generated test script, while this is not possible
   in other languages.

3. Generates a temporary script with the required boilerplate code to test the function.

4. Executes the script and captures the output of each test case.

5. Compares the actual outputs with the provided expected ones to determine correctness,
   and then prints the veredict summary.

## Quick Start

To run *Glassy Crystal Box*, you must first install [Python 3.12 or later](https://www.python.org/downloads/).
Then, run the following command from your terminal:

```commandline
python -m crystalbox --config-file <path to json configuration file>
```

### JSON Configuration Example

The following illustrates an example of how a small configuration file to run
two functions, from two separate files, with three test cases each would look like:

```json
{
    "base_path": "/path/to/the/root/of/the/files/to/test",

    "suites": [
        {
            "source_file": "relative/path/to/source_1.py",
            "function_name": "function_name_1",
            "test_cases": [
                { "input": [1, 3], "output": 3 },
                { "input": [1, 4], "output": 0 },
                { "input": [3, 9], "output": 6 }
            ]
        },

        {
            "source_file": "relative/path/to/source_2.py",
            "function_name": "function_name_2",
            "test_cases": [
                { "input": [1], "output": 5 },
                { "input": [4], "output": 100 },
                { "input": [50], "output": 50005 }
            ]
        }
    ]
}
```

- `base_path`: Path which will be taken as base to consider the `source_file` paths
               relative to. If omitted, `source_file` paths will be considered
               absolute paths.

- `suites`: List of descriptions of the functions to be tested:

  - `source_file`: Path to the file containing the source code to test. If `base_path`
                   is provided, it is considered relative to that path. Otherwise,
                   it is considered an absolute path.

  - `function_name`: Name of the function to test.

  - `test_cases`: List of input/output pairs to be used to run the function.

    - `input`: List of arguments the function receives. It is important to note that,
               while the JSON expects an array, Glassy Crystal Box treats them individually.
               So, for example, if you wanted to pass an `int` and an `array`, the value
               would look like `"input": [1, [2, 3]]`.

    - `output`: The expected output of running the function with the given input.

### Supported Programming Languages

**Functional:**

- Python
- JavaScript

**Planned Next:**

- C
- C++
- Go
- Java
- Ruby

#### JavaScript Note

For working with JavaScript files, make sure to export the functions you want
to test, so that Glassy Crystal Box can find them.

```javascript
export function myFunction() { ... }
```

## Scope and Limitations

- *Glassy Crystal Box* only works at function level for the time being. It does not
  function as a project build system or manager.

- Functions depending on `stdin` are currently not supported. All inputs ought to
  be provided by means of the JSON configuration file.

- Inputs are currently limited to languages' primitive types. Structs and objects
  are not supported yet, but are planned to be in the future.

- Since *Glassy Crystal Box* runs entirely locally, you need to have the necessary
  tools to build and run the source files installed (*e.g.* if you want to test C code,
  then *Glassy Crystal Box* will call `gcc` under the covers.).

## Planned Work

- Support the remaining programming languages described in the list above.

- Add support to output test veredicts to a file instead of the console,
  optionally in JSON format.

- Support complex object types for test inputs.

It is important to keep in mind this project is still in the functional
prototype stages, and will continue actively evolving!
