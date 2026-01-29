#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CSDN博客文章抓取脚本 (RSS版本)
使用 CSDN RSS Feed 抓取博客文章列表，避免 Cloudflare 反爬虫拦截
作者: GitHub Actions Bot

优势：
- RSS Feed 不受 Cloudflare 521 拦截
- 稳定可靠，适合 GitHub Actions 自动运行
- 返回所有文章（不限制数量）

注意：
- RSS 不提供阅读量数据，views 字段将为空
"""

import requests
import yaml
import xml.etree.ElementTree as ET
from datetime import datetime
import os
import re

# CSDN博客配置
CSDN_USERNAME = "Lvyizhuo"
CSDN_RSS_URL = f"https://blog.csdn.net/{CSDN_USERNAME}/rss/list"

# 获取脚本所在目录的父目录（项目根目录）
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
OUTPUT_FILE = os.path.join(PROJECT_ROOT, "_data", "csdn_posts.yml")

# 请求头
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    'Accept': 'application/rss+xml, application/xml, text/xml, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
}


def parse_date(date_str):
    """
    解析 RSS 日期格式
    输入格式: "Thu, 29 Jan 2026 15:04:41 +0800"
    输出格式: "2026-01-29"
    """
    try:
        # RSS 标准日期格式
        dt = datetime.strptime(date_str, "%a, %d %b %Y %H:%M:%S %z")
        return dt.strftime("%Y-%m-%d")
    except ValueError:
        try:
            # 备用格式，不带时区
            dt = datetime.strptime(date_str[:25], "%a, %d %b %Y %H:%M:%S")
            return dt.strftime("%Y-%m-%d")
        except ValueError:
            # 无法解析，返回空
            return ""


def clean_description(desc):
    """
    清理文章摘要，去除 CDATA 和多余空白
    """
    if not desc:
        return ""
    
    # 去除首尾空白
    desc = desc.strip()
    
    # 限制长度
    if len(desc) > 200:
        desc = desc[:200] + "..."
    
    return desc


def fetch_articles_from_rss():
    """
    从 CSDN RSS Feed 获取文章列表
    
    Returns:
        list: 文章列表
    """
    articles = []
    
    print(f"🔍 开始从 RSS Feed 抓取CSDN博客: {CSDN_USERNAME}")
    print(f"📡 RSS URL: {CSDN_RSS_URL}")
    
    try:
        # 发送请求
        response = requests.get(CSDN_RSS_URL, headers=HEADERS, timeout=30, allow_redirects=True)
        response.raise_for_status()
        
        print(f"✅ RSS 请求成功，状态码: {response.status_code}")
        
        # 解析 XML
        root = ET.fromstring(response.content)
        
        # 查找所有 item 元素
        items = root.findall('.//item')
        
        if not items:
            print("⚠️  RSS Feed 中没有找到文章")
            return articles
        
        print(f"📄 找到 {len(items)} 篇文章")
        
        for item in items:
            try:
                # 获取标题
                title_elem = item.find('title')
                title = title_elem.text if title_elem is not None else ""
                
                # 获取链接
                link_elem = item.find('link')
                link = link_elem.text if link_elem is not None else ""
                
                # 获取发布日期
                pub_date_elem = item.find('pubDate')
                pub_date = pub_date_elem.text if pub_date_elem is not None else ""
                date_str = parse_date(pub_date)
                
                # 获取摘要
                desc_elem = item.find('description')
                description = desc_elem.text if desc_elem is not None else ""
                excerpt = clean_description(description)
                
                if title and link:
                    article = {
                        'title': title,
                        'link': link,
                        'date': date_str,
                        'excerpt': excerpt,
                        'views': ''  # RSS 不提供阅读量
                    }
                    articles.append(article)
                    
            except Exception as e:
                print(f"⚠️  解析文章时出错: {str(e)}")
                continue
        
        print(f"\n✨ 成功解析 {len(articles)} 篇文章")
        
    except requests.RequestException as e:
        print(f"❌ RSS 请求失败: {str(e)}")
    except ET.ParseError as e:
        print(f"❌ XML 解析失败: {str(e)}")
    except Exception as e:
        print(f"❌ 发生错误: {str(e)}")
    
    return articles


def load_existing_data():
    """
    加载现有的文章数据
    
    Returns:
        dict: 现有数据，如果文件不存在则返回 None
    """
    if os.path.exists(OUTPUT_FILE):
        try:
            with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
                if data and isinstance(data, dict) and 'articles' in data:
                    print(f"📂 已加载现有数据: {data.get('total_count', 0)} 篇文章")
                    return data
        except Exception as e:
            print(f"⚠️  读取现有数据失败: {str(e)}")
    return None


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
        'source': 'RSS Feed',  # 标记数据来源
        'articles': articles
    }
    
    # 保存为YAML
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, allow_unicode=True, sort_keys=False, default_flow_style=False)
    
    print(f"💾 文章列表已保存到: {OUTPUT_FILE}")


def main():
    """主函数"""
    print("=" * 60)
    print("CSDN博客文章同步工具 (RSS版本)")
    print("=" * 60)
    
    # 加载现有数据，以便在抓取失败时保留
    existing_data = load_existing_data()
    existing_count = existing_data.get('total_count', 0) if existing_data else 0
    
    try:
        # 从 RSS Feed 获取文章
        articles = fetch_articles_from_rss()
        
        if articles:
            # 成功抓取到文章，保存到YAML
            save_to_yaml(articles)
            print("\n🎉 同步完成！")
            return 0
        else:
            # 抓取失败
            print("\n⚠️  未抓取到任何文章")
            
            if existing_data and existing_count > 0:
                # 保留原有数据，不覆盖
                print(f"🛡️  保留原有 {existing_count} 篇文章数据，不进行覆盖")
                return 0
            else:
                print("⚠️  没有现有数据可保留")
                return 1
            
    except Exception as e:
        print(f"\n❌ 发生错误: {str(e)}")
        import traceback
        traceback.print_exc()
        
        # 发生异常时也保留原有数据
        if existing_data and existing_count > 0:
            print(f"\n🛡️  发生异常，保留原有 {existing_count} 篇文章数据")
            return 0
        
        return 1


if __name__ == '__main__':
    exit(main())
