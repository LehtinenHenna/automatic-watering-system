#!/bin/bash

# Start the first process
python store.py &
  
# Start the second process
python pump_control.py &
  
# Wait for any process to exit
wait -n
  
# Exit with status of process that exited first
exit $?
