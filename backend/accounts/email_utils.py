from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def send_verification_email(user, token):
    """이메일 인증 메일 발송"""
    verification_url = f"{settings.FRONTEND_URL}/auth/verify-email?token={token.token}"

    subject = '[Tripify] 이메일 인증을 완료해주세요'

    html_message = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background-color: #3498db; color: white; padding: 20px; text-align: center; border-radius: 8px 8px 0 0; }}
            .content {{ background-color: #f9f9f9; padding: 30px; border-radius: 0 0 8px 8px; }}
            .button {{ display: inline-block; padding: 12px 30px; background-color: #3498db; color: white; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
            .footer {{ margin-top: 20px; text-align: center; color: #666; font-size: 12px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Tripify 이메일 인증</h1>
            </div>
            <div class="content">
                <p>안녕하세요, <strong>{user.username}</strong>님!</p>
                <p>Tripify 회원가입을 환영합니다.</p>
                <p>아래 버튼을 클릭하여 이메일 인증을 완료해주세요:</p>
                <p style="text-align: center;">
                    <a href="{verification_url}" class="button">이메일 인증하기</a>
                </p>
                <p>또는 아래 링크를 복사하여 브라우저에 붙여넣으세요:</p>
                <p style="word-break: break-all; background-color: #fff; padding: 10px; border-radius: 5px;">
                    {verification_url}
                </p>
                <p style="color: #e74c3c; margin-top: 20px;">
                    ⚠️ 이 링크는 24시간 동안만 유효합니다.
                </p>
                <p>본인이 요청하지 않은 경우 이 메일을 무시하셔도 됩니다.</p>
            </div>
            <div class="footer">
                <p>© 2024 Tripify. All rights reserved.</p>
            </div>
        </div>
    </body>
    </html>
    """

    plain_message = f"""
    안녕하세요, {user.username}님!

    Tripify 회원가입을 환영합니다.

    아래 링크를 클릭하여 이메일 인증을 완료해주세요:
    {verification_url}

    ⚠️ 이 링크는 24시간 동안만 유효합니다.

    본인이 요청하지 않은 경우 이 메일을 무시하셔도 됩니다.

    © 2024 Tripify. All rights reserved.
    """

    send_mail(
        subject=subject,
        message=plain_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        html_message=html_message,
        fail_silently=False,
    )


def send_password_reset_email(user, token):
    """비밀번호 재설정 메일 발송"""
    reset_url = f"{settings.FRONTEND_URL}/auth/reset-password?token={token.token}"

    subject = '[Tripify] 비밀번호 재설정 안내'

    html_message = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background-color: #e74c3c; color: white; padding: 20px; text-align: center; border-radius: 8px 8px 0 0; }}
            .content {{ background-color: #f9f9f9; padding: 30px; border-radius: 0 0 8px 8px; }}
            .button {{ display: inline-block; padding: 12px 30px; background-color: #e74c3c; color: white; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
            .footer {{ margin-top: 20px; text-align: center; color: #666; font-size: 12px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>비밀번호 재설정</h1>
            </div>
            <div class="content">
                <p>안녕하세요, <strong>{user.username}</strong>님!</p>
                <p>비밀번호 재설정을 요청하셨습니다.</p>
                <p>아래 버튼을 클릭하여 새로운 비밀번호를 설정해주세요:</p>
                <p style="text-align: center;">
                    <a href="{reset_url}" class="button">비밀번호 재설정하기</a>
                </p>
                <p>또는 아래 링크를 복사하여 브라우저에 붙여넣으세요:</p>
                <p style="word-break: break-all; background-color: #fff; padding: 10px; border-radius: 5px;">
                    {reset_url}
                </p>
                <p style="color: #e74c3c; margin-top: 20px;">
                    ⚠️ 이 링크는 1시간 동안만 유효합니다.
                </p>
                <p>본인이 요청하지 않은 경우 이 메일을 무시하셔도 됩니다.</p>
            </div>
            <div class="footer">
                <p>© 2024 Tripify. All rights reserved.</p>
            </div>
        </div>
    </body>
    </html>
    """

    plain_message = f"""
    안녕하세요, {user.username}님!

    비밀번호 재설정을 요청하셨습니다.

    아래 링크를 클릭하여 새로운 비밀번호를 설정해주세요:
    {reset_url}

    ⚠️ 이 링크는 1시간 동안만 유효합니다.

    본인이 요청하지 않은 경우 이 메일을 무시하셔도 됩니다.

    © 2024 Tripify. All rights reserved.
    """

    send_mail(
        subject=subject,
        message=plain_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        html_message=html_message,
        fail_silently=False,
    )


def send_username_recovery_email(user):
    """아이디 찾기 메일 발송"""
    subject = '[Tripify] 아이디 찾기 안내'

    html_message = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background-color: #2ecc71; color: white; padding: 20px; text-align: center; border-radius: 8px 8px 0 0; }}
            .content {{ background-color: #f9f9f9; padding: 30px; border-radius: 0 0 8px 8px; }}
            .username-box {{ background-color: #fff; padding: 15px; border-radius: 5px; border-left: 4px solid #2ecc71; margin: 20px 0; }}
            .footer {{ margin-top: 20px; text-align: center; color: #666; font-size: 12px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>아이디 찾기</h1>
            </div>
            <div class="content">
                <p>안녕하세요!</p>
                <p>요청하신 아이디는 다음과 같습니다:</p>
                <div class="username-box">
                    <strong>아이디:</strong> {user.username}
                </div>
                <p>가입일: {user.created_at.strftime('%Y년 %m월 %d일')}</p>
                <p>본인이 요청하지 않은 경우 이 메일을 무시하셔도 됩니다.</p>
            </div>
            <div class="footer">
                <p>© 2024 Tripify. All rights reserved.</p>
            </div>
        </div>
    </body>
    </html>
    """

    plain_message = f"""
    안녕하세요!

    요청하신 아이디는 다음과 같습니다:

    아이디: {user.username}
    가입일: {user.created_at.strftime('%Y년 %m월 %d일')}

    본인이 요청하지 않은 경우 이 메일을 무시하셔도 됩니다.

    © 2024 Tripify. All rights reserved.
    """

    send_mail(
        subject=subject,
        message=plain_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        html_message=html_message,
        fail_silently=False,
    )
