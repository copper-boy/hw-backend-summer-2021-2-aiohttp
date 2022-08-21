import typing
from typing import Optional


from app.base.base_accessor import BaseAccessor
from app.quiz.models import Theme, Question, Answer


class QuizAccessor(BaseAccessor):
    async def create_theme(self, title: str) -> Theme:
        theme = Theme(id=self.app.database.next_theme_id, title=str(title))
        self.app.database.themes.append(theme)
        return theme

    async def get_theme_by_title(self, title: str) -> Optional[Theme]:
        try:
            return next(theme for theme in self.app.database.themes if theme.title == title)
        except StopIteration:
            return None

    async def get_theme_by_id(self, id_: int) -> Optional[Theme]:
        try:
            return next(theme for theme in self.app.database.themes if theme.id == id_)
        except StopIteration:
            return None

    async def list_themes(self) -> list[Theme]:
        return self.app.database.themes

    async def get_question_by_title(self, title: str) -> Optional[Question]:
        try:
            return next(question for question in self.app.database.questions if question.title == title)
        except StopIteration:
            return None

    async def create_question(
        self, title: str, theme_id: int, answers: list[Answer]
    ) -> Question:
        question = Question(id=self.app.database.next_question_id, title=str(title), theme_id=theme_id, answers=answers)
        self.app.database.questions.append(question)
        return question

    async def list_questions(self) -> list[Question]:
        return self.app.database.questions

    async def filter_list_questions(self, theme_id: int) -> list[Question]:
        return list(filter(lambda n: n.theme_id == theme_id, self.app.database.questions))
