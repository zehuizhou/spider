#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  @Time    : 2020-09-09 15:26
#  @Author  : July
import time
import re
import requests
from parsel import Selector
from tools import save_to_mysql


def spider(topic_id):
    url = 'https://www.zhihu.com/api/v4/topics/19555513/feeds/essence?include=data%5B%3F%28target.type%3Dtopic_sticky_module%29%5D.target.data%5B%3F%28target.type%3Danswer%29%5D.target.content%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%3Bdata%5B%3F%28target.type%3Dtopic_sticky_module%29%5D.target.data%5B%3F%28target.type%3Danswer%29%5D.target.is_normal%2Ccomment_count%2Cvoteup_count%2Ccontent%2Crelevant_info%2Cexcerpt.author.badge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Dtopic_sticky_module%29%5D.target.data%5B%3F%28target.type%3Darticle%29%5D.target.content%2Cvoteup_count%2Ccomment_count%2Cvoting%2Cauthor.badge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Dtopic_sticky_module%29%5D.target.data%5B%3F%28target.type%3Dpeople%29%5D.target.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Danswer%29%5D.target.annotation_detail%2Ccontent%2Chermes_label%2Cis_labeled%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Canswer_type%3Bdata%5B%3F%28target.type%3Danswer%29%5D.target.author.badge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Danswer%29%5D.target.paid_info%3Bdata%5B%3F%28target.type%3Darticle%29%5D.target.annotation_detail%2Ccontent%2Chermes_label%2Cis_labeled%2Cauthor.badge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Dquestion%29%5D.target.annotation_detail%2Ccomment_count%3B&limit=10&offset=30'
    request_headers = {
        'accept': '*/*',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'
    }
    res = requests.get(url=url, headers=request_headers).json()
    data = res['data']
    for d in data:
        item = {}
        item['id'] = d['target']['id']
        item['content'] = d['target']['content']
        item['voteup_count'] = d['target']['voteup_count']
        item['comment_count'] = d['target']['comment_count']
        item['created_time'] = d['target']['created_time']
        item['updated_time'] = d['target']['updated_time']
        item['topic_id'] = topic_id
        item['url'] = d['target']['url']
        item['question_title'] = d['target']['question']['title']
        item['question_url'] = d['target']['question']['url']
        item['question_id'] = d['target']['question']['id']
        item['question_created_time'] = d['target']['question']['created_time']
        item['question_big_type'] = d['target']['question']['type']
        item['question_is_following'] = d['target']['question']['is_following']
        item['question_type'] = d['target']['target']['question']['question_type']
        item['author_name'] = d['target']['author']['name']
        item['author_type'] = d['target']['author']['type']
        item['author_url'] = d['target']['author']['url']
        item['author_headline'] = d['target']['author']['headline']


if __name__ == '__main__':
    spider(1)