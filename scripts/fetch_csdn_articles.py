#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CSDN博客文章抓取脚本
使用 CSDN API 抓取指定博客的所有文章列表并保存为YAML格式
作者: GitHub Actions Bot
"""

import requests
import yaml
import json
from datetime import datetime
import time
import os

# CSDN博客配置
CSDN_USERNAME = "Lvyizhuo"
CSDN_BLOG_URL = f"https://blog.csdn.net/{CSDN_USERNAME}"
# CSDN 内部 API
CSDN_ARTICLE_LIST_API = "https://blog.csdn.net/community/home-api/v1/get-business-list"
OUTPUT_FILE = "_data/csdn_posts.yml"

# 请求头 - 模拟移动端请求
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Referer': f'https://blog.csdn.net/{CSDN_USERNAME}',
}


def fetch_article_list_from_api():
    """
    使用 CSDN API 抓取博客文章列表
    
    Returns:
        articles: 文章列表
    """
    articles = []
    
    print(f"🔍 开始使用 API 抓取CSDN博客: {CSDN_USERNAME}")
    
    session = requests.Session()
    session.headers.update(HEADERS)
    
    max_retries = 3
    page = 1
    page_size = 40  # 每页获取40篇
    
    while True:
        for retry in range(max_retries):
            try:
                print(f"📡 正在请求第 {page} 页 (尝试 {retry + 1}/{max_retries})...")
                
                # 构建 API 请求参数
                params = {
                    'page': page,
                    'size': page_size,
                    'businessType': 'blog',
                    'orderby': '',
                    'noMore': 'false',
                    'year': '',
                    'month': '',
                    'username': CSDN_USERNAME
                }
                
                # 发送请求到 API
                response = session.get(CSDN_ARTICLE_LIST_API, params=params, timeout=15)
                response.raise_for_status()
                
                # 解析 JSON 响应
                data = response.json()
                
                if data.get('code') != 200:
                    print(f"⚠️  API 返回错误: {data.get('message', 'Unknown error')}")
                    if retry < max_retries - 1:
                        time.sleep((retry + 1) * 3)
                        continue
                    else:
                        break
                
                # 获取文章列表
                article_list = data.get('data', {}).get('list', [])
                
                if not article_list:
                    print(f"✅ 第 {page} 页无更多文章，已获取全部")
                    break
                
                print(f"✅ 第 {page} 页找到 {len(article_list)} 篇文章")
                
                # 解析文章信息
                for item in article_list:
                    try:
                        title = item.get('title', '').strip()
                        article_id = item.get('articleId', '')
                        link = f"https://blog.csdn.net/{CSDN_USERNAME}/article/details/{article_id}"
                        
                        # 处理日期 - 转换时间戳
                        post_time = item.get('postTime', '')
                        date_str = ''
                        if post_time:
                            try:
                                # CSDN 返回的时间戳是毫秒级
                                timestamp = int(post_time) / 1000 if len(str(post_time)) > 10 else int(post_time)
                                date_obj = datetime.fromtimestamp(timestamp)
                                date_str = date_obj.strftime('%Y-%m-%d')
                            except:
                                date_str = str(post_time)[:10]
                        
                        # 获取摘要
                        description = item.get('description', '').strip()
                        if len(description) > 150:
                            description = description[:150] + '...'
                        
                        # 获取阅读量
                        view_count = item.get('viewCount', 0)
                        views = str(view_count) if view_count else ''
                        
                        if title and link:
                            article = {
                                'title': title,
                                'link': link,
                                'date': date_str,
                                'excerpt': description,
                                'views': views
                            }
                            articles.append(article)
                        
                    except Exception as e:
                        print(f"⚠️  解析文章时出错: {str(e)}")
                        continue
                
                # 成功获取，跳出重试循环
                break
                
            except requests.RequestException as e:
                print(f"❌ 请求失败 (尝试 {retry + 1}/{max_retries}): {str(e)}")
                if retry < max_retries - 1:
                    time.sleep((retry + 1) * 5)
                else:
                    # 最后一次重试也失败了，返回已获取的文章
                    print(f"⚠️  第 {page} 页获取失败，返回已获取的 {len(articles)} 篇文章")
                    return articles
            except json.JSONDecodeError as e:
                print(f"❌ JSON 解析错误 (尝试 {retry + 1}/{max_retries}): {str(e)}")
                if retry < max_retries - 1:
                    time.sleep((retry + 1) * 3)
                else:
                    return articles
            except Exception as e:
                print(f"❌ 处理时出错 (尝试 {retry + 1}/{max_retries}): {str(e)}")
                if retry < max_retries - 1:
                    time.sleep((retry + 1) * 3)
                else:
                    return articles
        else:
            # 重试全部失败
            break
        
        # 检查是否还有更多文章
        if len(article_list) < page_size:
            print(f"✅ 已获取所有文章")
            break
        
        # 继续获取下一页
        page += 1
        time.sleep(2)  # 礼貌地等待2秒再请求下一页
    
    print(f"\n✨ 总共抓取到 {len(articles)} 篇文章")
    return articles


def save_to_yaml(articles):
    """
    将文章列表保存为YAML文件
    
    Args:
        articles: 文章列表
    """
    # 确保目录存在
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    
    # 添加元数据
    data = {
        'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'total_count': len(articles),
        'articles': articles
    }
    
    # 保存为YAML
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, allow_unicode=True, sort_keys=False, default_flow_style=False)
    
    print(f"💾 文章列表已保存到: {OUTPUT_FILE}")


def main():
    """主函数"""
    print("=" * 60)
    print("CSDN博客文章同步工具 - 使用 API 方法")
    print("=" * 60)
    
    try:
        # 抓取文章
        articles = fetch_article_list_from_api()
        
        if articles:
            # 保存到YAML
            save_to_yaml(articles)
            print("\n🎉 同步完成！")
            return 0
        else:
            print("\n⚠️  未抓取到任何文章")
            return 1
            
    except Exception as e:
        print(f"\n❌ 发生错误: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    exit(main())
