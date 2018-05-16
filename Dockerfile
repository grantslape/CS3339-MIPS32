# Official Python 2.7 image for now
FROM python:2.7

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD app /app

# Install dependencies
RUN pip install --trusted-host pypi.python.org -r requirements.txt

#Install iverilog
RUN apt-get update && apt-get -y upgrade
RUN apt-get install iverilog

# Compile myhdl.vpi
RUN make -C /usr/local/share/myhdl/cosimulation/icarus
RUN mv /usr/local/share/myhdl/cosimulation/icarus/myhdl.vpi \
	./lib/myhdl.vpi

# Expose port 80 to world
EXPOSE 80

# Environment variables here
ENV NAME MIPS32
# python path hack TODO: fix this up
ENV PYTHONPATH /app

# Try running the tests
CMD ["python", "test/test_all_modules.py"]
