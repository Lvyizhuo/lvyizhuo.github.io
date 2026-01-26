#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CSDN博客文章抓取脚本
抓取指定CSDN博客的文章列表并保存为YAML格式
作者: GitHub Actions Bot
"""

import requests
from bs4 import BeautifulSoup
import yaml
import re
from datetime import datetime
import time
import os

# CSDN博客配置
CSDN_USERNAME = "Lvyizhuo"
CSDN_BLOG_URL = f"https://blog.csdn.net/{CSDN_USERNAME}"
OUTPUT_FILE = "_data/csdn_posts.yml"

# 请求头，模拟浏览器访问
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Connection': 'keep-alive',
}


def fetch_article_list(max_pages=5):
    """
    抓取CSDN博客文章列表
    
    Args:
        max_pages: 最大抓取页数
        
    Returns:
        articles: 文章列表，每篇文章包含标题、链接、日期、摘要等信息
    """
    articles = []
    
    print(f"🔍 开始抓取CSDN博客: {CSDN_BLOG_URL}")
    
    # 只抓取第一页（通常已包含所有近期文章）
    page = 1
    try:
        url = f"{CSDN_BLOG_URL}?type=blog"
        
        print(f"📄 正在抓取博客文章列表: {url}")
        
        # 发送请求
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        response.encoding = 'utf-8'
        
        # 解析HTML
        soup = BeautifulSoup(response.text, 'lxml')
        
        # 查找文章列表（CSDN可能有多种布局）
        article_items = soup.find_all('div', class_='article-item-box')
        
        # 尝试其他可能的选择器
        if not article_items:
            article_items = soup.find_all('article', class_='blog-list-box')
        if not article_items:
            article_items = soup.find_all('div', class_='blog-list-box')
        
        if not article_items:
            print(f"⚠️  未找到文章，尝试备用方法...")
            # 备用：直接查找所有文章链接
            return []
        
        print(f"✅ 找到 {len(article_items)} 篇文章")
        
        for item in article_items:
            try:
                # 提取文章标题和链接 - 使用更通用的选择器
                title_elem = item.find('a', href=lambda x: x and '/article/details/' in x)
                if not title_elem:
                    title_elem = item.find('a', class_='blog-title-box')
                if not title_elem:
                    # 查找h4标签内的链接
                    h4 = item.find('h4')
                    if h4:
                        title_elem = h4.find('a')
                
                if not title_elem:
                    continue
                
                title = title_elem.get_text().strip()
                # 清理标题中的多余空白和换行
                title = ' '.join(title.split())
                # 移除"原创"标签  
                title = title.replace('原创', '').strip()
                # 如果标题过长，截取第一句话作为标题（通常标题和摘要在一起）
                if len(title) > 80:
                    # 尝试在第一个句号、问号、感叹号处截断
                    for sep in ['。', '！', '？', ' 本文', ' 这是']:
                        if sep in title:
                            title = title.split(sep)[0] + ('。' if sep in ['。', '！', '？'] else '')
                            break
                    # 如果还是太长，直接截断
                    if len(title) > 80:
                        title = title[:77] + '...'
                
                link = title_elem.get('href', '')
                
                # 确保链接是完整的URL
                if link and not link.startswith('http'):
                    link = 'https://blog.csdn.net' + link
                
                # 提取发布日期
                date_elem = item.find('span', class_='date')
                date_str = date_elem.get_text().strip() if date_elem else ''
                
                # 提取摘要
                excerpt_elem = item.find('p', class_='content')
                if not excerpt_elem:
                    excerpt_elem = item.find('div', class_='content')
                excerpt = excerpt_elem.get_text().strip() if excerpt_elem else ''
                
                # 提取阅读量、点赞等信息
                info_box = item.find('div', class_='info-box')
                views = ''
                if info_box:
                    view_elem = info_box.find('span', class_='read-num')
                    if view_elem:
                        views = view_elem.get_text().strip()
                
                # 构建文章数据
                article = {
                    'title': title,
                    'link': link,
                    'date': date_str,
                    'excerpt': excerpt[:150] + '...' if len(excerpt) > 150 else excerpt,
                    'views': views
                }
                
                articles.append(article)
                
            except Exception as e:
                print(f"⚠️  解析文章时出错: {str(e)}")
                continue
        
    except requests.RequestException as e:
        print(f"❌ 请求失败: {str(e)}")
    except Exception as e:
        print(f"❌ 处理时出错: {str(e)}")
    
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
