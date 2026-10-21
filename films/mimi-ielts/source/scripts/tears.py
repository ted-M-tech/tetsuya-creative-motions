"""Tear times of the daily calendar in the montage (pages 30 -> 1, then the test-day page shows). Shared by hf/index.html and mix.py.

usage: python3 films/mimi-ielts/source/scripts/tears.py   # prints the JS array pasted into hf/index.html
"""
START, SPAN, N, P = 9.6, 2.75, 30, 0.55
TEARS = [round(START + SPAN * (i / (N - 1)) ** P, 3) for i in range(N)]
if __name__ == '__main__':
    print(TEARS)
