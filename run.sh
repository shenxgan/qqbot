#!/bin/bash

host="abc"
project_path="/home/ubuntu/qqbot"


usage() {
    echo "usage: $0 [start/stop/restart/tail/deploy/upload]"
    echo '    start:        启动'
    echo '    stop:         停止'
    echo '    restart:      重启'
    echo '    tail:         查看日志'
    echo '    deploy:       部署到服务器'
    echo '    upload|up:    将改动的文件上传到服务器'
    exit 0
}

copy_change() {
    echo $0 $1 $2
    git_status="`git status -s`"
    i=0
    for f in $git_status; do
        ((i++))
        if [[ $((i % 2)) -eq 0 ]]; then
            if [[ "$1" == "all" ]]; then
                echo "scp $f $host:$project_path/$f"
                scp $f $host:$project_path/$f
            elif [[ "$1" == "no" ]]; then
                echo "scp $f $host:$project_path/$f"
            else
                read -p "upload $f? [yes/no]: " scp_yes
                if [[ "$scp_yes" == "yes" ]]; then
                    echo "scp $f $host:$project_path/$f"
                    scp $f $host:$project_path/$f
                else
                    echo "[only echo] scp $f $host:$project_path/$f"
                fi
            fi
        fi
    done

    if [[ "$1" == "no" ]]; then
        exit 0
    fi

    read -p "是否重启服务？[yes/no]：" _yes
    if [[ "$_yes" == "yes" ]]; then
        ssh $host "cd $project_path && ./run.sh restart"
    fi
}


case "$1" in
    start)
        docker compose up $2
    ;;
    stop)
        docker compose down
    ;;
    restart)
        docker compose down
        docker compose up $2
    ;;
    tail)
        docker compose logs -f $2
    ;;
    deploy)
        ssh $host "cd $project_path && git pull origin main && ./run.sh restart"
    ;;
    upload|up)
        shift
        copy_change "$@"
    ;;
    *)
        usage
    ;;
esac
