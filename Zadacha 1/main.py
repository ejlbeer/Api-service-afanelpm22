from collections import Counter

def parse_line(line):
    parts = line.split()
    return {
        "ip": parts[0],
        "method": parts[5].strip('"'),
        "path": parts[6],
        "status": parts[8]
    }

def main():
    by_status = Counter()
    by_path = Counter()
    
    with open("access.log") as f:
        for line in f:
            data = parse_line(line)
            by_status[data["status"]] += 1
            by_path[data["path"]] += 1

    print("Статистика по кодам ответа:")
    for code, count in by_status.items():
        print(code, count)

if __name__ == "__main__":

    main()
