if ! ps ax | grep -q "[p]ython3 ./main.py"; then
  python3 ./main.py
fi