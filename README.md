# Jupyter helpers for IPython

[![flake8](https://github.com/krassowski/jupyter-helpers/workflows/Flake8/badge.svg)](https://github.com/krassowski/jupyter-helpers/actions?query=workflow%3A%22flake8%22)
[![pypi-version](https://img.shields.io/pypi/v/jupyter-helpers.svg)](https://python.org/pypi/jupyter-helpers)

This collection of IPython helpers optimized for JupyterLab users will help you to:

- Play a sound once the computations have finished (or failed)
- Integrate the notifications with your OS (ready for GNOME shell)
- Enable auto-completion for rpy2 (great for using  ggplot2!) - now also available in [jupyterlab-lsp](https://github.com/krassowski/jupyterlab-lsp)
- Summarize dictionaries and other structures in a nice table
- Selectively import from other notebooks
- Scroll to the recently executed cell on error or when opening the notebook
- Use interactive (following) tail for long outputs


The examples are available in [demos](https://github.com/krassowski/jupyter-helpers/tree/master/demos) directory. Please, see the [Productivity tips for Jupyter (Python)](https://medium.com/@krassowski.michal/productivity-tips-for-jupyter-python-a3614d70c770) article for introduction and more code samples. For jump-to-definition feature, please visit [jupyterlab-lsp](https://github.com/krassowski/jupyterlab-lsp).



### Installation

For basic functionality:

```bash
pip3 install jupyter_helpers
```

To include interactive widgets:

```bash
pip3 install ipywidgets
jupyter labextension install @jupyter-widgets/jupyterlab-manager
```

To use advanced GNOME integration,
run `setup.sh` script from the installation directory (PRs welcome to propose a better setup procedure).

To check if you have required system libraries for the better GNOME integration, see [notify-send.sh repository](https://github.com/vlevit/notify-send.sh).


### Showcase

#### Notifications

![Notifications](https://raw.githubusercontent.com/krassowski/jupyter-helpers/master/images/notifications_integration.gif)

#### Tailing outputs

![Following tail](https://raw.githubusercontent.com/krassowski/jupyter-helpers/master/images/tail.gif)

#### Auto-completion in R cells

![R auto-completion](https://raw.githubusercontent.com/krassowski/jupyter-helpers/master/images/r_autocomplete.gif)

#### Neat namespaces

![NeatNamespace](https://raw.githubusercontent.com/krassowski/jupyter-helpers/master/images/neat_namespace.png)

#### Selective imports

![Selective imports](https://raw.githubusercontent.com/krassowski/jupyter-helpers/master/images/selective_import.png)
