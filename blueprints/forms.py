# 注册表单，验证数据是否合理
import wtforms
from wtforms import *
from wtforms.validators import *
import email_validator
from model import *
from flask_wtf import FlaskForm
from flask_ckeditor import CKEditorField


class TempVehicleForm(wtforms.Form):
    vp = wtforms.StringField(validators=[Length(min=0, max=7, message="车牌号格式错误！"),
                                         InputRequired(message="该项不能为空！")
                                         ])
    name = wtforms.StringField(validators=[Length(min=2, max=10, message="姓名格式错误！"),
                                           InputRequired(message="该项不能为空！")
                                           ])
    # def validate_vp(self, field):
    #     vp = field.data
    #     VP = CarModel.query.filter_by(vp=vp).first()
    #     if VP:
    #         raise wtforms.ValidationError(message='该车辆已存在')
    is_holder = wtforms.SelectField(choices=(('1', '是'), ('0', '否')))


class ResidentRegForm(wtforms.Form):
    name = wtforms.StringField(validators=[Length(min=2, max=10, message="姓名格式错误！"),
                                           InputRequired(message="该项不能为空！")
                                           ])
    is_holder = wtforms.RadioField(validators=[InputRequired(message="该项不能为空！")])
    phone_num = wtforms.StringField(validators=[Length(min=11, max=11, message="手机号长度错误！"),
                                                Regexp(regex='1[38745]\d{9}', message="手机号必须是数字"),
                                                InputRequired(message="该项不能为空！")
                                                ])

    def validate_person(self, field):
        person = field.data
        PERSON = CarModel.query.filter_by(vp=person).first()
        if PERSON:
            raise wtforms.ValidationError(message='该车辆已存在')

    building = wtforms.IntegerField(validators=[Length(min=1, max=2, message="长度错误！"),
                                                InputRequired(message="该项不能为空！")
                                                ])
    room = wtforms.IntegerField(validators=[Length(min=1, max=2, message="长度错误！"),
                                            InputRequired(message="该项不能为空！")
                                            ])
    workplace = wtforms.StringField(validators=[InputRequired(message="该项不能为空！")])


# class ResidentForm(wtforms.Form):
#     name = wtforms.StringField(validators=[Length(min=2, max=10, message="姓名格式错误！"),
#                                            InputRequired(message="该项不能为空！")
#                                            ])

class ForgetForm(wtforms.Form):
    phone_num = wtforms.StringField(validators=[Length(min=11, max=11, message="手机号长度错误！"),
                                                Regexp(regex='1[38745]\d{9}', message="手机号必须是数字"),
                                                InputRequired(message="该项不能为空！")
                                                ])
    captcha = wtforms.StringField(validators=[Length(min=4, max=4, message="验证码格式错误！")])


class ConfirmForm(wtforms.Form):
    password = wtforms.StringField(validators=[Length(min=5, max=20, message="密码格式错误！")])
    confirm = wtforms.StringField(validators=[EqualTo("password", message="两次密码不一致！")])


class PasswordForm(wtforms.Form):
    password = wtforms.StringField(validators=[Length(min=5, max=20, message="密码格式错误！")])


class LoginForm(wtforms.Form):
    name = wtforms.StringField(validators=[Length(min=2, max=10, message="姓名格式错误！"),
                                           InputRequired(message="该项不能为空！")
                                           ])
    password = wtforms.StringField(validators=[Length(min=5, max=20, message="密码格式错误！"),
                                               InputRequired(message="该项不能为空！")
                                               ])


class ComposeForm(wtforms.Form):
    receiver_name = wtforms.StringField(validators=[InputRequired(message="收件人不能为空！")])
    title = wtforms.StringField(validators=[InputRequired(message="标题不能为空！")])
    content = wtforms.TextAreaField(validators=[InputRequired(message="正文不能为空！")])


class RecruitForm(wtforms.Form):
    captcha = wtforms.StringField(validators=[Length(min=4, max=4, message="验证码格式错误！")])
    password = wtforms.StringField(validators=[Length(min=5, max=20, message="密码格式错误！")])
    confirm = wtforms.StringField(validators=[EqualTo("password", message="两次密码不一致！")])
    phone_num = wtforms.StringField(validators=[Length(min=11, max=11, message="手机号长度错误！"),
                                                Regexp(regex='1[38745]\d{9}', message="手机号必须是数字"),
                                                InputRequired(message="该项不能为空！")
                                                ])

    def validate_phone_num(self, field):
        phone_num = field.data
        admin = AdminModel.query.filter_by(phone_num=phone_num).first()
        if admin:
            raise wtforms.ValidationError(message='该手机号已被使用')

    def validate_captcha(self, field):  # field 就代表下面定义的.data所赋值的变量，即captcha
        captcha = field.data
        c = CaptchaModel.query.filter_by(phone_num=self.phone_num.data, captcha=captcha)
        if not c:
            raise wtforms.ValidationError(message='验证码错误')


class VisitorRegForm(wtforms.Form):
    name = wtforms.StringField(validators=[Length(min=2, max=10, message="姓名格式错误！"),
                                           InputRequired(message="该项不能为空！")
                                           ])
    reason = wtforms.TextAreaField(validators=[InputRequired(message="原因不能为空！")])
    phone_num = wtforms.StringField(validators=[Length(min=11, max=11, message="手机号长度错误！"),
                                                Regexp(regex='1[38745]\d{9}', message="手机号必须是数字"),
                                                InputRequired(message="该项不能为空！")
                                                ])


class EditResidentForm(wtforms.Form):
    id = wtforms.IntegerField(validators=[InputRequired(message="该项不能为空！")])

    name = wtforms.StringField(validators=[Length(min=2, max=10, message="姓名格式错误！"),
                                           InputRequired(message="该项不能为空！")
                                           ])
    phone_num = wtforms.StringField(validators=[Length(min=11, max=11, message="手机号长度错误！"),
                                                Regexp(regex='1[38745]\d{9}', message="手机号必须是数字"),
                                                InputRequired(message="该项不能为空！")
                                                ])
    workplace = wtforms.StringField(validators=[InputRequired(message="该项不能为空！")])


class EditVisitorForm(wtforms.Form):
    id = wtforms.IntegerField(validators=[InputRequired(message="该项不能为空！")])

    name = wtforms.StringField(validators=[Length(min=2, max=10, message="姓名格式错误！"),
                                           InputRequired(message="该项不能为空！")
                                           ])
    reason = wtforms.StringField(validators=[InputRequired(message="该项不能为空！")])
    phone_num = wtforms.StringField(validators=[Length(min=11, max=11, message="手机号长度错误！"),
                                                Regexp(regex='1[38745]\d{9}', message="手机号必须是数字"),
                                                InputRequired(message="该项不能为空！")
                                                ])


class EditCarForm(wtforms.Form):
    id = wtforms.IntegerField(validators=[InputRequired(message="该项不能为空！")])
    vp = wtforms.StringField(validators=[Length(min=0, max=7, message="车牌号格式错误！"),
                                         InputRequired(message="该项不能为空！")
                                         ])
    owner_name = wtforms.StringField(validators=[Length(min=2, max=10, message="姓名格式错误！"),
                                           InputRequired(message="该项不能为空！")
                                           ])
    owner_id = wtforms.IntegerField(validators=[InputRequired(message="该项不能为空！")])


class AnnounceForm(FlaskForm):
    title = StringField('标题', validators=[DataRequired()])
    content = CKEditorField('正文', validators=[DataRequired()])
    submit = SubmitField('提交')


