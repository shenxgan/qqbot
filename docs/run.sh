#!/bin/bash

usage() {
    echo "usage: $0 [dev/preview/build/deploy]"
    echo '    dev:              本地运行'
    echo '    preview|pre:      本地预览'
    echo '    build:            构建'
    echo '    deploy|up:        部署到服务器'
    exit 0
}

case "$1" in
    dev)
        npm run docs:dev
    ;;
    preview|pre)
        npm run docs:preview
    ;;
    build)
        npm run docs:build
    ;;
    deploy|up)
        scp -r .vitepress/dist/* abc:/var/www/qqbot/
    ;;
    *)
        usage
    ;;
esac
