# packages = rabbitmq
# 
# deps:
# 	brew update
# 	brew install $(packages)

screen-deploy:
	screen -RD sparker -c ./deploy/screen.rc

simulator:
	screen -RD simulator /Developer/Platforms/iPhoneSimulator.platform/Developer/Applications/iPhone\ Simulator.app/Contents/MacOS/iPhone\ Simulator
