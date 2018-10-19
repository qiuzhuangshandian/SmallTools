1：go build -ldflags="-w -s" main.go
减少体积，-w去掉dwarf调试信息，程序将不能通过gdb调试

2：go build -ldfalgs="-H windowsgui" main.go
运行时不显示黑框框

3：go build -ldflags="-H windowsgui -s -w" main.go
减少体积，并且运行时不显示终端