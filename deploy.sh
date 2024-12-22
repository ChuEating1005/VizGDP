#!/usr/bin/env sh

# 確保腳本拋出遇到的錯誤
set -e

# 建立
npm run build

# 進入輸出產物資料夾
cd dist

# 初始化 git 並提交
git init
git add -A
git commit -m 'deploy'
git branch -M gh-pages
git remote add origin git@github.com:ChuEating1005/VizGDP.git
# 推送到 gh-pages 分支
git push -f origin gh-pages

cd -