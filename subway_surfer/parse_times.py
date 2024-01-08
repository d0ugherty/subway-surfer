import re

def parse_times(text_lines):
    # Regular expression to match time patterns like '5.45'
    time_pattern = re.compile(r'\d{1,2}\.\d{2}')

    parsed_times = []
    for line in text_lines:
        # Find all time matches in the line
        matches = time_pattern.findall(line)
        if matches:
            parsed_times.extend(matches)
    
    return parsed_times


if __name__ == '__main__':
   
    parsed_times = []
    # Parse the times from the file content
    with open('sched_test.txt', 'r') as file:
        for line in file:
            parsed_times += parse_times(line)


# Displaying the first few parsed times to verify the output
    print(parsed_times[:20])
