#!/bin/bash
# CSDN博客同步测试脚本

echo "🧪 CSDN博客同步测试"
echo "===================="
echo ""

# 检查Python环境
echo "📋 检查Python环境..."
if ! command -v python3 &> /dev/null; then
    echo "❌ 未找到Python3，请先安装Python"
    exit 1
fi
echo "✅ Python版本: $(python3 --version)"
echo ""

# 检查并安装依赖
echo "📦 检查依赖包..."
pip3 install -q requests beautifulsoup4 pyyaml lxml 2>/dev/null || {
    echo "⚠️  使用pip安装依赖..."
    pip3 install requests beautifulsoup4 pyyaml lxml
}
echo "✅ 依赖包已安装"
echo ""

# 运行抓取脚本
echo "🚀 开始抓取CSDN博客文章..."
echo "===================="
python3 scripts/fetch_csdn_articles.py

# 检查结果
if [ $? -eq 0 ]; then
    echo ""
    echo "✨ 测试完成！"
    echo ""
    echo "📁 生成的文件："
    echo "  - _data/csdn_posts.yml"
    echo ""
    
    if [ -f "_data/csdn_posts.yml" ]; then
        echo "📄 文件内容预览："
        echo "===================="
        head -n 20 _data/csdn_posts.yml
        echo "..."
        echo "===================="
        echo ""
        echo "✅ 文件生成成功！"
        echo ""
        echo "🎉 下一步："
        echo "  1. 提交更改到GitHub仓库"
        echo "  2. GitHub Pages会自动重新构建"
        echo "  3. 访问 https://Lvyizhuo.github.io/year-archive/ 查看效果"
    fi
else
    echo ""
    echo "❌ 测试失败，请检查错误信息"
    exit 1
fi
