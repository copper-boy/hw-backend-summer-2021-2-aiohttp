from aiohttp.web_exceptions import HTTPConflict, HTTPNotFound, HTTPBadRequest
from aiohttp.web_response import Response
from aiohttp_apispec import request_schema, response_schema

from app.quiz.schemes import (
    ThemeAddResponseSchema, ThemeListResponseSchema, ThemeAddRequestSchema, QuestionAddRequestSchema,
    QuestionAddResponseSchema, QuestionListResponseSchema, ThemeSchema, QuestionSchema
)

from app.web.app import View
from app.web.mixins import AuthRequiredMixin
from app.web.utils import json_response, error_json_response


class ThemeAddView(AuthRequiredMixin, View):
    @request_schema(ThemeAddRequestSchema)
    @response_schema(ThemeAddResponseSchema)
    async def post(self) -> Response:
        title = self.data['title']
        if await self.request.app.store.quizzes.get_theme_by_title(title):
            raise HTTPConflict
        theme = await self.request.app.store.quizzes.create_theme(title=title)
        return json_response(data=ThemeAddResponseSchema().dump(theme))


class ThemeListView(AuthRequiredMixin, View):
    @response_schema(ThemeListResponseSchema)
    async def get(self):
        themes = await self.request.app.store.quizzes.list_themes()
        raw_themes = tuple(ThemeSchema().dump(theme) for theme in themes)
        return json_response(data={'themes': raw_themes})


class QuestionAddView(AuthRequiredMixin, View):
    @request_schema(QuestionAddRequestSchema)
    @response_schema(QuestionAddResponseSchema)
    async def post(self) -> Response:
        answers = self.data['answers']
        is_correct_count = 0
        for answer in answers:
            if answer['is_correct']:
                is_correct_count += 1
        if is_correct_count != 1 or len(answers) == 1:
            raise HTTPBadRequest
        title = self.data['title']
        if await self.request.app.store.quizzes.get_question_by(attribute='title', value=title):
            raise HTTPConflict
        theme_id = self.data['theme_id']
        if await self.request.app.store.quizzes.get_theme_by_id(theme_id) is None:
            raise HTTPNotFound
        question = await self.request.app.store.quizzes.create_question(title=title, theme_id=theme_id, answers=answers)
        return json_response(data=QuestionAddResponseSchema().dump(question))


class QuestionListView(AuthRequiredMixin, View):
    @response_schema(QuestionListResponseSchema)
    async def get(self):
        theme_id = self.request.query.get('theme_id')
        if theme_id is None:
            questions = await self.request.app.store.quizzes.list_questions()
            raw_questions = [QuestionSchema().dump(question) for question in questions]
            return json_response(data={'questions': raw_questions})
        questions = list(filter(lambda n: n.theme_id == theme_id,
                                await self.request.app.store.quizzes.list_questions())) or self.request.app.store.quizzes.list_questions()
        raw_questions = [QuestionSchema().dump(question) for question in questions]
        return json_response(data={'questions': raw_questions})
