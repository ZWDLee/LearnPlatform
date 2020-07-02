def score_from_notification_into(deal_with_pk, deal_with_list):
    """
    :about 处理从消息页面进入时打分和评论定位
    :param deal_with_pk:
    :param deal_with_list:
    :return: page_num
    """
    comment_page_cut = int(len(deal_with_list) / 15) if len(deal_with_list) % 15 == 0 else int(
        (len(deal_with_list) + 15) / 15)
    adist = {}
    page_num = -1
    for i in range(1, comment_page_cut + 1):
        adist.update({i: deal_with_list[15 * (i - 1):15 * i]})
    for i, j in adist.items():
        for n in range(len(j)):
            if int(deal_with_pk) == j[n].pk:
                page_num = i
    return page_num