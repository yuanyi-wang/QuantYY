
$script_folder = Split-Path -Parent $($global:MyInvocation.MyCommand.Definition)

# if(Get-Command 'docker1' -errorAction SilentlyContinue){
#     echo "docker command does not exists, please install docker first"
# }
$redis_conf_folder = Split-Path -Parent $script_folder

docker run --name redis -p 6379:6379 -v $redis_conf_folder/redis.conf:/etc/redis/redis.conf -v D:/docker-data/redis:/data -d redis:7.2-alpine redis-server /etc/redis/redis.conf

docker run --name redis-stack -p 6379:6379 -p 8001:8001 -d redis/redis-stack