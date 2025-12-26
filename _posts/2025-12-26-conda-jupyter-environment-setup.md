---
title: "【环境配置】—— Conda 虚拟环境管理与 Jupyter 内核常用指令"
date: 2025-12-26
permalink: /posts/2025/12/conda-jupyter-setup-guide/
excerpt: "本文汇总了 Anaconda 环境创建、删除、包管理以及 Jupyter Kernel 的配置与卸载等常用指令，助力高效搭建深度学习开发环境。"
tags:
  - Conda
  - Jupyter
  - 环境配置
  - Python
---

## 清华镜像加速网站

    -i https://pypi.tuna.tsinghua.edu.cn/simple

## 激活系统环境

    activate

## 创建新环境

    conda create -n env_name python=3.8

## 删除虚拟环境

    conda remove -n env_name --all

## 进入虚拟环境

    conda activate env_name

## 退出该环境
    
    conda deactivate env_name

## 查看已安装环境
   
    conda info -e

## 手动安装包
	conda install --use-local rdkit-2018.09.2.0-py36h865188c_1.tar.bz2
## 查看已安装的包
  
    conda list
    pip list

## 查看是否安装某个包（numpy为例）
	conda list numpy
## 查看配置信息
  
    conda info

## jupyter删除虚拟环境
  
    jupyter kernelspec list

## 删除jupyter虚拟环境内核
  
    jupyter kernelspec uninstall myenv


第二篇博客的命名和开头配置