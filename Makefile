# packages = rabbitmq
# 
# deps:
# 	brew update
# 	brew install $(packages)

screen-deploy:
	screen -RD sparker -c ./deploy/screen.rc