# go-plane-go
A highly professional optimizer for Stanford Flight

# Getting Started

## Pipenv

### Install Pipenv

Pipenv is a cool package that lets us create a virtual environment, so that everyone is running on the samve version of python with the same packages.

[Install and use pipenv](https://robots.thoughtbot.com/how-to-manage-your-python-projects-with-pipenv)

If pipenv says `bash: parse_git_branch: command not found`, the issue is that your .bashrc file in your home directory doesn't have the git branch parsing function.  Edit your `~/.bashrc` file to add the following:

```bash
# Git branch in prompt.
parse_git_branch() {
    git branch 2> /dev/null | sed -e '/^[^*]/d' -e 's/* \(.*\)/ (\1)/'
}
```

### Run Pipenv

Start your pipenv virtual environment with `pipenv shell`.  Run files with `pipenv python3 file-name.py`.

### Quit Pipenv

Exit the pipenv virtual environment with the `exit` command, or ctrl+d.

## MatPlotLib

For Mac OSX only, you will need to follow [these instructions](https://github.com/JuliaPy/PyCall.jl/issues/218#issuecomment-267558858) to avoid the `ImportError: Python is not installed as a framework. The Mac OS X backend will not be able to function correctly if Python is not installed as a framework.` error.

## Miscellaneous

[How to edit this markdown file without effin it up](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet)

## Running the Program
Once the pipenv shell is activated, run the program from the home directory with `python3 src/go-plane-go.py`.