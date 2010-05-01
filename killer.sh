pid=$(ps -A | grep python | grep grep -v | cut -d" " -f1)
kill $pid
pid=$(ps -A | grep python | grep grep -v | cut -d" " -f2)
kill $pid


