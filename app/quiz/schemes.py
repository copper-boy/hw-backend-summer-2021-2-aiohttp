from marshmallow import Schema, fields


class ThemeSchema(Schema):
    id = fields.Int(required=True)
    title = fields.Str(required=True)


class ThemeAddRequestSchema(Schema):
    title = fields.Str(required=True)


class ThemeAddResponseSchema(Schema):
    id = fields.Int(required=True)
    title = fields.Str(required=True)


class ThemeListResponseSchema(Schema):
    themes = fields.Nested(ThemeSchema, many=True, required=True)


class Answer(Schema):
    title = fields.Str(required=True)
    is_correct = fields.Bool(required=True)


class QuestionSchema(Schema):
    id = fields.Int(required=True)
    title = fields.Str(required=True)
    theme_id = fields.Int(required=True)
    answers = fields.Nested(Answer, many=True, required=True)


class QuestionListResponseSchema(Schema):
    questions = fields.Nested(QuestionSchema, many=True, required=True)


class QuestionAddRequestSchema(Schema):
    title = fields.Str(required=True)
    theme_id = fields.Int(required=True)
    answers = fields.Nested(Answer, many=True)


class QuestionAddResponseSchema(Schema):
    id = fields.Int(required=True)
    title = fields.Str(required=True)
    theme_id = fields.Int(required=True)
    answers = fields.Nested(Answer, many=True, required=True)


