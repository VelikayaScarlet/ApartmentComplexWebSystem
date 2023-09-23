from flask import *
from sqlalchemy.orm import relationship

from blueprints.forms import *
from decorators import *
from model import *

bp = Blueprint('mail', __name__, url_prefix='/mail')


@bp.route('/mail_main', methods=['GET', 'POST'])
@login_required
def mail_main():
    emails = EmailModel.query.order_by(EmailModel.create_time.desc()).all()
    # print(g.name, g.id)
    # print(session['admin_id'])  # 不知道为什么 g.id就没法用，会提示没有这个属性，只好从session里面取
    my_emails = [email for email in emails if session['admin_id'] == email.receiver_id and
                 email.is_trash == 0 and email.is_draft == 0]

    return render_template('d_mail.html', emails=my_emails)


@bp.route('/mail_view/<mail_id>', methods=['GET', 'POST'])
@login_required
def mail_view(mail_id):
    email = EmailModel.query.filter_by(id=mail_id)
    email[0].is_read = True
    print(email[0].id, email[0].is_read)
    admin_id = session['admin_id']
    emails = EmailModel.query.filter_by(sender_id=admin_id)
    cnt = 0
    for e in emails:
        cnt += 1
    db.session.commit()
    return render_template('d_mail_view.html', email=email[0], length=cnt)


@bp.route('/throw2trash/<mail_id>')
@login_required
def throw2trash(mail_id):
    email = EmailModel.query.filter_by(id=mail_id).first()
    if email.is_trash == 1:
        email.is_trash = 0
    else:
        email.is_trash = 1
    print('邮件状态已修改', email.is_trash)
    db.session.commit()
    return redirect(url_for('mail.trash'))


@bp.route('/delete_in_trash/<mail_id>')
@login_required
def delete_in_trash(mail_id):
    email = EmailModel.query.filter_by(id=mail_id).first()
    db.session.delete(email)
    db.session.commit()
    return redirect(url_for('mail.trash'))


@bp.route('/compose', methods=['GET', 'POST'])
@login_required
def compose():
    emails = EmailModel.query.order_by(EmailModel.create_time.desc()).all()
    my_emails = [email for email in emails if session['admin_id'] == email.receiver_id]
    recent_id = []
    recent_name = []
    for me in my_emails:
        recent_id.append(me.sender_id)
    admins = AdminModel.query.order_by(AdminModel.id).all()
    for a in admins:
        if a.id in recent_id:
            recent_name.append(a.name)

    if request.method == 'GET':
        return render_template('d_mail_compose.html', recent_name=recent_name)
    else:
        form = ComposeForm(request.form)
        if form.validate():
            receiver_name = form.receiver_name.data[0:-13]
            receiver_id = AdminModel.query.filter_by(name=receiver_name).first().id
            title = form.title.data
            content = form.content.data
            # admin = AdminModel.query.filter_by(id=receiver_id).first()
            if not receiver_id:
                return render_template('d_mail_compose.html', error_msg='无此用户', recent_name=recent_name)
            elif receiver_id == session['admin_id']:
                return render_template('d_mail_compose.html', error_msg='不能发给自己', recent_name=recent_name)
            else:
                id = session['admin_id']
                e = EmailModel(content=content,
                               create_time=datetime.now(),
                               is_trash=0,
                               is_important=0,
                               sender_id=id,
                               receiver_id=receiver_id,
                               is_read=0,
                               title=title,
                               is_draft=0)

                if 'send' in request.form:
                    print('send')
                    db.session.add(e)
                    db.session.commit()
                    return redirect(url_for('mail.sent'))
                else:
                    print('to_draft')
                    e.is_draft = 1
                    db.session.add(e)
                    db.session.commit()
                    return redirect(url_for('mail.draft'))


@bp.route('/trash', methods=['GET', 'POST'])
@login_required
def trash():
    emails = EmailModel.query.order_by(EmailModel.create_time.desc()).all()
    my_emails = [email for email in emails
                 if (session['admin_id'] == email.receiver_id
                     or session['admin_id'] == email.sender_id)
                 and email.is_trash == 1]
    return render_template('d_mail_trash.html', emails=my_emails)


@bp.route('/draft', methods=['GET', 'POST'])
@login_required
def draft():
    emails = EmailModel.query.order_by(EmailModel.create_time.desc()).all()
    my_emails = [email for email in emails
                 if (session['admin_id'] == email.receiver_id
                     or session['admin_id'] == email.sender_id)
                 and email.is_draft == 1 and email.is_trash == 0]
    return render_template('d_mail_draft.html', emails=my_emails)


@bp.route('/compose_draft/<mail_id>', methods=['GET', 'POST'])
@login_required
def compose_draft(mail_id):
    draft_mail = EmailModel.query.filter_by(id=mail_id).first()
    receiver = AdminModel.query.filter_by(id=draft_mail.receiver_id).first().name
    emails = EmailModel.query.order_by(EmailModel.create_time.desc()).all()

    my_emails = [email for email in emails if session['admin_id'] == email.receiver_id]
    recent_id = []
    recent_name = []
    for me in my_emails:
        recent_id.append(me.sender_id)
    admins = AdminModel.query.order_by(AdminModel.id).all()
    for a in admins:
        if a.id in recent_id:
            recent_name.append(a.name)
    return render_template('d_mail_compose.html', draft_mail=draft_mail, receiver=receiver, recent_name=recent_name)


@bp.route('/to_draft', methods=['GET', 'POST'])
@login_required
def to_draft():
    return render_template('d_mail_draft.html')


@bp.route('/sent', methods=['GET', 'POST'])
@login_required
def sent():
    emails = EmailModel.query.order_by(EmailModel.create_time.desc()).all()
    my_emails = [email for email in emails if session['admin_id'] == email.sender_id
                 and email.is_trash is False and email.is_draft is False]
    return render_template('d_mail_sent.html', emails=my_emails)


@bp.route('/filter_read', methods=['GET', 'POST'])
@login_required
def filter_read():
    emails = EmailModel.query.order_by(EmailModel.create_time.desc()).all()
    my_emails = [email for email in emails if
                 1 == email.is_read and email.is_trash is False and email.is_draft is False]
    return render_template('d_mail.html', emails=my_emails)


@bp.route('/filter_unread', methods=['GET', 'POST'])
@login_required
def filter_unread():
    emails = EmailModel.query.order_by(EmailModel.create_time.desc()).all()
    my_emails = [email for email in emails if
                 0 == email.is_read and email.is_trash is False and email.is_draft is False]
    return render_template('d_mail.html', emails=my_emails)


@bp.route('/filter_important', methods=['GET', 'POST'])
@login_required
def filter_important():
    emails = EmailModel.query.order_by(EmailModel.create_time.desc()).all()
    my_emails = [email for email in emails if
                 1 == email.is_important and email.is_trash is False and email.is_draft is False]
    return render_template('d_mail.html', emails=my_emails)


@bp.route('/filter_regular', methods=['GET', 'POST'])
@login_required
def filter_regular():
    emails = EmailModel.query.order_by(EmailModel.create_time.desc()).all()
    my_emails = [email for email in emails if
                 0 == email.is_important and email.is_trash is False and email.is_draft is False]
    return render_template('d_mail.html', emails=my_emails)


@bp.route('transfer', methods=['GET', 'POST'])
@login_required
def transfer():
    pass
