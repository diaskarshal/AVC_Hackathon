from sqlalchemy.orm import Session
from typing import List, Dict
from app.models.project import Project
from app.services.embedding_service import embed_text, cosine_similarity


class SimilarityService:
    def __init__(self, db: Session):
        self.db = db

    def build_project_embedding_text(self, project: Project) -> str:
        parts = [project.name or ""]
        if project.description:
            parts.append(project.description)
        for resource in project.resources:
            parts.append(resource.name)
        for task in project.tasks:
            parts.append(task.name)
        return " ".join(parts)

    def index_project(self, project: Project) -> None:
        text = self.build_project_embedding_text(project)
        project.embedding = embed_text(text)
        project.embedding_text = text
        self.db.commit()

    def find_similar_projects(self, query_text: str, top_k: int = 3) -> List[Dict]:
        query_embedding = embed_text(query_text)

        projects = self.db.query(Project).filter(
            Project.embedding.isnot(None)
        ).all()

        scored = []
        for project in projects:
            score = cosine_similarity(query_embedding, project.embedding)
            scored.append({
                "project": project,
                "similarity_score": round(score, 3)
            })

        scored.sort(key=lambda x: x["similarity_score"], reverse=True)
        return scored[:top_k]