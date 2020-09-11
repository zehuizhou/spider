#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  @Time    : 2020-09-09 15:26
#  @Author  : July
import time
from parsel import Selector
import requests
from tools import save_to_mysql

FLAG = 10000


def spider(topic_id):
    """
    爬取某个话题下点赞数超过 FLAG 的回答
    :param topic_id: 话题id
    :return:
    """
    break_flag = 0
    offset = 600
    while True:
        url = 'https://www.zhihu.com/api/v4/topics/{topic_id}/' \
              'feeds/essence?include=data%5B%3F%28target.type%3Dtopic_sticky_module%29%5D.target.data%5B%3F%28target.type%3Danswer%29%5D.target.content%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%3Bdata%5B%3F%28target.type%3Dtopic_sticky_module%29%5D.target.data%5B%3F%28target.type%3Danswer%29%5D.target.is_normal%2Ccomment_count%2Cvoteup_count%2Ccontent%2Crelevant_info%2Cexcerpt.author.badge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Dtopic_sticky_module%29%5D.target.data%5B%3F%28target.type%3Darticle%29%5D.target.content%2Cvoteup_count%2Ccomment_count%2Cvoting%2Cauthor.badge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Dtopic_sticky_module%29%5D.target.data%5B%3F%28target.type%3Dpeople%29%5D.target.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Danswer%29%5D.target.annotation_detail%2Ccontent%2Chermes_label%2Cis_labeled%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Canswer_type%3Bdata%5B%3F%28target.type%3Danswer%29%5D.target.author.badge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Danswer%29%5D.target.paid_info%3Bdata%5B%3F%28target.type%3Darticle%29%5D.target.annotation_detail%2Ccontent%2Chermes_label%2Cis_labeled%2Cauthor.badge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Dquestion%29%5D.target.annotation_detail%2Ccomment_count%3B' \
              '&limit=10&offset={offset}'.format(topic_id=topic_id, offset=offset)
        print(url)
        request_headers = {
            'accept': '*/*',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'
        }
        res = requests.get(url=url, headers=request_headers).json()
        data = res['data']
        need_data = []
        for d in data:
            item = {}
            item['id'] = d['target']['id']
            html = Selector(d['target']['content'])
            item['content'] = html.xpath("string(/)").get('')
            item['voteup_count'] = d['target']['voteup_count']
            item['comment_count'] = d['target']['comment_count']

            item['created_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(d.get('target').get('created_time')))
            item['updated_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(d.get('target').get('created_time')))

            item['topic_id'] = topic_id
            item['url'] = d['target']['url']
            if 'question' in d.get('target'):
                item['question_title'] = d.get('target').get('question').get('title')
                item['question_url'] = d.get('target').get('question').get('url')
                item['question_id'] = d.get('target').get('question').get('id')
                item['question_created_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(d.get('target').get('question').get('created')))
                item['question_big_type'] = d.get('target').get('question').get('type')
                item['question_is_following'] = d.get('target').get('question').get('is_following')
                item['question_type'] = d['target'].get('question').get('question_type')
            else:
                item['question_title'], item['question_url'], item['question_id'], item['question_created_time'], item['question_big_type'], item['question_is_following'], item['question_type'] = '', '', 1, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), '', '', ''
            item['author_id'] = d['target'].get('author').get('id')
            item['author_name'] = d['target'].get('author').get('name')
            item['author_type'] = d['target'].get('author').get('type')
            item['author_url'] = d['target'].get('author').get('url')
            item['author_headline'] = d['target'].get('author').get('headline')

            need_data.append(item)
            print(item)
            offset += 10
            if int(item['voteup_count']) <= FLAG:
                break_flag = 1
        save_to_mysql('top_answer', need_data)
        if break_flag == 1:
            break


if __name__ == '__main__':
    with open('topic_ids', 'r') as f:
        ids = f.readlines()
    for i in ids:
        spider(i)
