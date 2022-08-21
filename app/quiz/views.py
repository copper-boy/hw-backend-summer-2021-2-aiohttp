from aiohttp.web_response import Response
from aiohttp_apispec import request_schema, response_schema

from app.quiz.schemes import (
    ThemeAddResponseSchema, ThemeListResponseSchema, ThemeAddRequestSchema, QuestionAddRequestSchema,
    QuestionAddResponseSchema, QuestionListResponseSchema, ThemeSchema, QuestionSchema
)
from app.web.app import View
from app.web.mixins import AuthRequiredMixin
from app.web.utils import json_response, error_json_response


class ThemeAddView(View, AuthRequiredMixin):
    @request_schema(ThemeAddRequestSchema)
    @response_schema(ThemeAddResponseSchema)
    async def post(self) -> Response:
        result = await self.auth_required(self.request)
        if not isinstance(result, str):
            return result

        title = self.data['title']

        if await self.request.app.store.quizzes.get_theme_by_title(title=title):
            return error_json_response(http_status=409, message='theme is already created', status='conflict')
        theme = await self.request.app.store.quizzes.create_theme(title=title)
        return json_response(data=ThemeAddResponseSchema().dump(theme))


class ThemeListView(View, AuthRequiredMixin):
    @response_schema(ThemeListResponseSchema)
    async def get(self):
        result = await self.auth_required(self.request)
        if not isinstance(result, str):
            return result

        themes = await self.request.app.store.quizzes.list_themes()
        raw_themes = tuple(ThemeSchema().dump(theme) for theme in themes)
        return json_response(data={'themes': raw_themes})


class QuestionAddView(View, AuthRequiredMixin):
    @request_schema(QuestionAddRequestSchema)
    @response_schema(QuestionAddResponseSchema)
    async def post(self) -> Response:
        result = await self.auth_required(self.request)
        if not isinstance(result, str):
            return result

        answers = self.data['answers']
        is_correct_count = 0
        for answer in answers:
            if answer['is_correct']:
                is_correct_count += 1
        if is_correct_count != 1 or len(answers) == 1:
            return error_json_response(http_status=400, message='data in answers is not valid', status='bad_request')

        title = self.data['title']
        if await self.request.app.store.quizzes.get_question_by_title(title=title):
            return error_json_response(http_status=409, message='a question with this name already exists')
        theme_id = self.data['theme_id']
        if await self.request.app.store.quizzes.get_theme_by_id(theme_id) is None:
            return error_json_response(http_status=404, message=f'theme with {theme_id=} doesnt exists')
        question = await self.request.app.store.quizzes.create_question(title=title, theme_id=theme_id, answers=answers)
        return json_response(data=QuestionAddResponseSchema().dump(question))


class QuestionListView(View, AuthRequiredMixin):
    @response_schema(QuestionListResponseSchema)
    async def get(self):
        result = await self.auth_required(self.request)
        if not isinstance(result, str):
            return result
        theme_id = self.request.query.get('theme_id')
        if theme_id is None:
            questions = await self.request.app.store.quizzes.list_questions()
            raw_questions = [QuestionSchema().dump(question) for question in questions]
            return json_response(data={'questions': raw_questions})

        questions = await self.request.app.store.quizzes.filter_list_questions(
            theme_id=int(theme_id))

        raw_questions = [QuestionSchema().dump(question) for question in questions]
        return json_response(data={'questions': raw_questions})
