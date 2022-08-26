import typing
from collections import namedtuple
from typing import Optional

from aiohttp.web_exceptions import HTTPServerError

from app.base.base_accessor import BaseAccessor
from app.quiz.models import Theme, Question, Answer


class QuizAccessor(BaseAccessor):
    async def create_theme(self, title: str) -> Theme:
        theme = Theme(id=self.app.database.next_theme_id, title=str(title))
        self.app.database.themes.append(theme)
        return theme

    async def create_question(
            self, title: str, theme_id: int, answers: list[Answer]
    ) -> Question:
        question = Question(id=self.app.database.next_question_id, title=str(title), theme_id=theme_id, answers=answers)
        self.app.database.questions.append(question)
        return question

    async def get_theme_by_title(self, title: str) -> Optional[Theme]:
        try:
            return next(theme for theme in self.app.database.themes if theme.title == title)
        except StopIteration:
            return None

    async def get_theme_by_id(self, id: int) -> Optional[Theme]:
        try:
            return next(theme for theme in self.app.database.themes if theme.id == id)
        except StopIteration:
            return None

    async def get_theme_by(self, attribute: str, value: object) -> Optional[Theme]:
        try:
            return next(theme for theme in self.app.database.themes if theme.__getattribute__(attribute) == value)
        except AttributeError:
            raise HTTPServerError
        except StopIteration:
            return None

    async def get_question_by(self, attribute: str, value: object) -> Optional[Question]:
        try:
            return next(question for question in self.app.database.questions if
                        question.__getattribute__(attribute) == value)
        except AttributeError:
            raise HTTPServerError
        except StopIteration:
            return None

    async def list_themes(self) -> list[Theme]:
        return self.app.database.themes

    async def list_questions(self) -> list[Question]:
        return self.app.database.questions
