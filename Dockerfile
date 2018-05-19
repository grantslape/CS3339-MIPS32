# Official Python 3.6 image for now
FROM python:3.6

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD app /app

# Install dependencies
RUN pip install --trusted-host pypi.python.org -r requirements.txt

#Install iverilog
RUN apt-get update && apt-get -y install iverilog && apt-get clean \
	&& rm -rf /var/lib/apt/lists/*

# Compile myhdl.vpi
RUN make -C /usr/local/share/myhdl/cosimulation/icarus
RUN mv /usr/local/share/myhdl/cosimulation/icarus/myhdl.vpi \
	./lib/myhdl.vpi

# Environment variables here
ENV NAME MIPS32
# python path hack TODO: fix this up
ENV PYTHONPATH /app

# Try running the tests
CMD ["python", "test/test_all_modules.py"]
