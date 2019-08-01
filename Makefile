PROJ_ROOT=$(HOME)/chipboard/
BOOST_ROOT := $(PROJ_ROOT)/boost_1_70_0
#PYTHON_ROOT := /gpfs/pkgs/mhpcc/anaconda3-5.0.1
PYTHON_INC := /usr/include/python3.6
PYTHON_LIB_LOCATION := /usr/lib/python3.6
BOOST_INC := $(BOOST_ROOT)
BOOST_LIB_LOCATION := $(BOOST_ROOT)/stage/lib
BOOST_LIB_FILE := boost_python36

CC := gcc
CPP := g++

CFLAGS := -fPIC -I$(BOOST_INC) -I$(PYTHON_INC)
CInc := -I$(BOOST_INC) -I$(PYTHON_INC)


CLinkFlags = -shared -Wl,-soname,$@ -Wl,-rpath -L$(BOOST_LIB_LOCATION) -L$(PYTHON_LIB_LOCATION) -lpython3.6m -l$(BOOST_LIB_FILE)

all: chipboard.so

%.so: %.cpp
	$(CPP) $^ $(CFLAGS) $(CInc) $(CLinkFlags) -o $@

clean:
	rm *.so
