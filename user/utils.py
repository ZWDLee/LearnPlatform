import random
import string
import time
from io import BytesIO

from PIL import Image, ImageFont
from PIL.ImageDraw import ImageDraw
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.core.mail import send_mail


def user_status(mine, request_mine):
    if mine.pk == request_mine.pk:
        if mine.profile.user_type:
            return 0
        else:
            return 1
    else:
        if mine.profile.user_type:
            return 2
        else:
            return 3


def article_all_type(articles):
    articles_set = set()
    for article in articles:
        articles_set.add(article.article_type.type_name)
    return list(articles_set)


def get_color():
    return random.randrange(100, 256)


def get_bg_color():
    return random.randrange(0, 148)


def get_code():
    code = ''.join(random.sample(string.ascii_letters + string.digits, 4))
    return code


def verification_code(request):
    """
    :param request:
    :return:
    about:生成4位随机验证码图
    """
    mode = 'RGB'
    size = (100, 34)
    color_bg = (get_bg_color(), get_bg_color(), get_bg_color())
    # 画布
    image = Image.new(mode=mode, size=size, color=color_bg)
    # 画笔
    image_draw = ImageDraw(image, mode=mode)
    image_font = ImageFont.truetype(settings.FONT_PATH, random.randrange(30, 34))
    # 绘制文字
    code = get_code()
    request.session['verification_code'] = code
    for i in range(4):
        fill = (get_color(), get_color(), get_color())
        image_draw.text(xy=(i * random.randrange(18, 28), random.randrange(5)), text=code[i], font=image_font, fill=fill)
    for i in range(2):
        fill = (get_color(), get_color(), get_color())
        xy1 = ((random.randrange(100), random.randrange(50)), (random.randrange(75), random.randrange(25)))
        image_draw.line(xy=xy1, fill=fill)
        xy2 = ((random.randrange(50), random.randrange(100)), (random.randrange(34), random.randrange(13)))
        image_draw.line(xy=xy2, fill=fill)
    for i in range(10):
        fill = (get_color(), get_color(), get_color())
        xy1 = ((random.randrange(100), random.randrange(50)), (random.randrange(75), random.randrange(25)))
        image_draw.point(xy=xy1, fill=fill)
    # 变成比特流
    fp = BytesIO()
    image.save(fp, 'png')
    return HttpResponse(fp.getvalue(), content_type='image/png')


def send_email(title, message, email):
    """
    program:发送邮件
    :return:
    """
    send_mail(
        title,
        message,
        '943318968@qq.com',
        [email],
    )


def send_verification_code(request):
    email = request.GET.get('email', '')
    send_for = request.GET.get('send_for', '')
    data = {}
    if email != '':
        code = get_code()
        now = int(time.time())
        send_code_time = request.session.get('send_code_time', 0)
        if now - send_code_time < 60:
            data['status'] = 'ERROR'
        else:
            request.session[send_for] = code
            request.session['send_code_time'] = now
            send_email('验证码', '验证码：%s' % code, email)
            data['status'] = 'SUCCESS'
    else:
        data['status'] = 'ERROR'
    return JsonResponse(data)
