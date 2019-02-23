# Official Python 3.6 image for now
FROM python:3.6

# Add requirements first
RUN mkdir /app
ADD app/requirements.txt /app/

# Set the working directory to /app
WORKDIR /app

#Install iverilog
RUN apt-get update && apt-get -y install iverilog && apt-get clean \
	&& rm -rf /var/lib/apt/lists/*

# Install dependencies
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Compile myhdl.vpi
RUN make -C /usr/local/share/myhdl/cosimulation/icarus

# Copy the app into the container at /app
ADD app /app

# Move compiled vpi
RUN mv /usr/local/share/myhdl/cosimulation/icarus/myhdl.vpi \
	./lib/myhdl.vpi

# Environment variables here
ENV NAME MIPS32
# python path hack TODO: fix this up
ENV PYTHONPATH /app

# Try running the tests
CMD ["python", "test/test_all_modules.py"]
