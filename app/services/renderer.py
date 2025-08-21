import os
from .template_store import TemplateStore

class Renderer:
    def __init__(self, store: TemplateStore):
        self.store = store
