
###### Eexecuting myapp

Inside /myapp dir, run:

docker build -t tempsensor:latest -

Find attached container ID using the following command:

docker images


Run:
time docker run -it --name myraspi --privileged -v /sys:/sys -d -p 2026:2030 <container ID>

Expose port 2026 for accessing web service from host OS
Port 2030 is the port for Flask web server

--privileged directive is used to access host resources

 -v /sys:/sys Docker volume is used to expose Pi's GPIO to the container. These GPIOs are present in host's file system under /sys/class/gpio directory. 
GPIOs can be accessed with certain user privileges through virtual files in host file system. 
Go to localhost on host browser to view temp and humidity at port 2026