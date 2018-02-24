CC = gcc
CFLAGS  = -Wall
  
TARGET = parser

LDFLAGS = curl

all: $(TARGET)
  
$(TARGET): $(TARGET).c
	$(CC) $(CFLAGS) -o $(TARGET) $(TARGET).c -l$(LDFLAGS)
