from fastapi import FastAPI

from app.db.database import Base, engine

# Import ALL models
from app.models.document import Document
from app.models.version import Version
from app.models.node import Node
from app.models.selection import Selection
from app.models.selection_node import SelectionNode
from app.api.search import router as search_router

from app.api.document import router as document_router
from app.api.tree import router as tree_router
from app.api.selection import router as selection_router
from app.api.generation import router as generation_router
from app.api.compare import router as compare_router

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(document_router)
app.include_router(tree_router)
app.include_router(search_router)
app.include_router(selection_router)    
app.include_router(generation_router)
app.include_router(compare_router)