@echo off
echo generating proto...
python -m grpc_tools.protoc -I=../../protos --python_out=. --grpc_python_out=. ../../protos/chat.proto
echo DONE