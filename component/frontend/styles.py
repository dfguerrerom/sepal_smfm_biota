#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from IPython.display import display
from ipywidgets import HTML

STYLES = """
<style>
body.jp-Notebook, 
div.jp-Cell,
div.jp-OutputArea-output {

    margin: 0 !important;
    padding: 0 !important;
}

.leaflet-widgetcontrol {
    box-shadow: none !important;
}

</style>
"""

_ = display(HTML(STYLES))
