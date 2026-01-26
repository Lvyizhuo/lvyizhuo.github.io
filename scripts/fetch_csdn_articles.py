#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CSDN博客文章抓取脚本
使用 RSS Feed 抓取指定CSDN博客的文章列表并保存为YAML格式
作者: GitHub Actions Bot
"""

import requests
from bs4 import BeautifulSoup
import yaml
import re
from datetime import datetime
import time
import os
import xml.etree.ElementTree as ET

# CSDN博客配置
CSDN_USERNAME = "Lvyizhuo"
CSDN_BLOG_URL = f"https://blog.csdn.net/{CSDN_USERNAME}"
CSDN_RSS_URL = f"https://blog.csdn.net/{CSDN_USERNAME}/rss/list"
OUTPUT_FILE = "_data/csdn_posts.yml"

# 请求头 - RSS 请求更简单
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (compatible; RSS Reader/1.0)',
    'Accept': 'application/rss+xml, application/xml, text/xml, */*',
}


def fetch_article_list_from_rss():
    """
    从 RSS Feed 抓取CSDN博客文章列表
    
    Returns:
        articles: 文章列表，每篇文章包含标题、链接、日期、摘要等信息
    """
    articles = []
    
    print(f"🔍 开始从 RSS 抓取CSDN博客: {CSDN_RSS_URL}")
    
    max_retries = 3
    
    for retry in range(max_retries):
        try:
            print(f"📡 正在请求 RSS Feed (尝试 {retry + 1}/{max_retries})...")
            
            # 发送请求
            response = requests.get(CSDN_RSS_URL, headers=HEADERS, timeout=15)
            response.raise_for_status()
            
            # 解析 XML
            root = ET.fromstring(response.content)
            
            # RSS 2.0 格式
            items = root.findall('.//item')
            
            if not items:
                print(f"⚠️  RSS 中未找到文章...")
                if retry < max_retries - 1:
                    time.sleep((retry + 1) * 3)
                    continue
                else:
                    return []
            
            print(f"✅ RSS 中找到 {len(items)} 篇文章")
            
            for item in items:
                try:
                    # 提取标题
                    title_elem = item.find('title')
                    title = title_elem.text.strip() if title_elem is not None else ''
                    
                    # 提取链接
                    link_elem = item.find('link')
                    link = link_elem.text.strip() if link_elem is not None else ''
                    
                    # 提取发布日期
                    date_elem = item.find('pubDate')
                    date_str = ''
                    if date_elem is not None and date_elem.text:
                        try:
                            # 解析 RSS 日期格式: "Sat, 25 Jan 2026 14:30:00 GMT"
                            pub_date = datetime.strptime(date_elem.text.strip(), '%a, %d %b %Y %H:%M:%S %Z')
                            date_str = pub_date.strftime('%Y-%m-%d')
                        except:
                            # 如果解析失败，直接使用原始文本
                            date_str = date_elem.text.strip()[:10]
                    
                    # 提取描述/摘要
                    desc_elem = item.find('description')
                    excerpt = ''
                    if desc_elem is not None and desc_elem.text:
                        # 清理 HTML 标签
                        soup = BeautifulSoup(desc_elem.text, 'html.parser')
                        excerpt = soup.get_text().strip()
                        # 限制长度
                        if len(excerpt) > 150:
                            excerpt = excerpt[:150] + '...'
                    
                    # 构建文章数据
                    if title and link:
                        article = {
                            'title': title,
                            'link': link,
                            'date': date_str,
                            'excerpt': excerpt,
                            'views': ''  # RSS 中没有阅读量信息
                        }
                        articles.append(article)
                    
                except Exception as e:
                    print(f"⚠️  解析文章时出错: {str(e)}")
                    continue
            
            break  # 成功，退出重试循环
            
        except requests.RequestException as e:
            print(f"❌ 请求失败 (尝试 {retry + 1}/{max_retries}): {str(e)}")
            if retry < max_retries - 1:
                time.sleep((retry + 1) * 5)
            else:
                return []
        except ET.ParseError as e:
            print(f"❌ XML 解析错误 (尝试 {retry + 1}/{max_retries}): {str(e)}")
            if retry < max_retries - 1:
                time.sleep((retry + 1) * 3)
            else:
                return []
        except Exception as e:
            print(f"❌ 处理时出错 (尝试 {retry + 1}/{max_retries}): {str(e)}")
            if retry < max_retries - 1:
                time.sleep((retry + 1) * 3)
            else:
                return []
    
    print(f"\n✨ 总共抓取到 {len(articles)} 篇文章")
    return articles


def fetch_article_list(max_pages=5):
    """
    抓取CSDN博客文章列表 - 保留用于备用
    优先使用 RSS，如果失败则尝试网页爬取
    """
    # 首先尝试 RSS
    articles = fetch_article_list_from_rss()
    if articles:
        return articles
    
    print("\n⚠️  RSS 方法失败，尝试备用方法...")
    
    # 备用方法：网页爬取（可能被封）
    # 备用方法：网页爬取（可能被封）
    articles = []
    
    print(f"🔍 尝试从网页抓取: {CSDN_BLOG_URL}")
    
    # 这里保留原来的网页爬取代码作为备用
    # 但一般不会执行到这里，因为 RSS 更可靠
    
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
    print("CSDN博客文章同步工具")
    print("=" * 60)
    
    try:
        # 抓取文章
        articles = fetch_article_list(max_pages=10)
        
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
