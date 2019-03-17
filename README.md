# Jupyter helpers

This collection of Jupyter helpers will help you to:

- Play a sound once the computations have finished (or failed)
- Integrate the notifications with your OS (ready for GNOME shell)
- Enable auto-completion for rpy2 (great for using  ggplot2!)
- Summarize dictionaries and other structures in a nice table
- Selectively import from other notebooks
- Scroll to the recently executed cell on error or when opening the notebook
- Use interactive (following) tail for long outputs


The detailed description is in preparation.


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

Notifications:

![Notifications](https://raw.githubusercontent.com/krassowski/jupyter-helpers/master/images/notifications_integration.gif)

Tailing outputs:

![Following tail](https://raw.githubusercontent.com/krassowski/jupyter-helpers/master/images/tail.gif)

Auto-completion in R cells:

![R auto-completion](https://raw.githubusercontent.com/krassowski/jupyter-helpers/master/images/r_autocomplete.gif)

Neat namespaces:

![NeatNamespace](https://raw.githubusercontent.com/krassowski/jupyter-helpers/master/images/neat_namespace.png)

Selective imports:

![Selective imports](https://raw.githubusercontent.com/krassowski/jupyter-helpers/master/images/selective_import.png)
