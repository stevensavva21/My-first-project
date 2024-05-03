def parseTimeSlot(hourRange):
    if '-' in hourRange:
        start, end = hourRange.split('-')
        return range(int(start), int(end)+1)
    return []


def processAvailability(filename):
    weekdays = ["Mon", "Tues", "Wed", "Thurs", "Fri"]
    # Map full day names to the abbreviations used
    day_map = {
        "Monday": "Mon", "Tuesday": "Tues", "Wednesday": "Wed", "Thursday": "Thurs", "Friday": "Fri"
    }
    availability = {day: [0]*10 for day in weekdays}

    with open(filename, 'r') as file:
        for line in file:
            if ':' not in line:
                continue
            person, schedule = line.strip().split(': ')
            entries = schedule.split(', ')
            for entry in entries:
                parts = entry.strip().split(' ')
                if len(parts) < 2:
                    continue
                dayOfWeek, hours = parts[0], parts[1]
                # Ensure the day is processed correctly
                day = day_map.get(dayOfWeek[:len(dayOfWeek)-1], dayOfWeek[:5])
                for hour in parseTimeSlot(hours):
                    if 8 <= hour < 18:
                        if day in availability:
                            availability[day][hour-8] += 1

    return availability


def displayAvailability(availability):
    for day, slots in availability.items():
        print(f"{day}: ", end="")
        users = max(slots)
        if users == 0:
            users = 1
        userThreshold = users / 2
        for count in slots:
            if count > userThreshold:
                color = '\033[92m'
            elif count < userThreshold:
                color = '\033[91m'
            else:
                color = '\033[93m'
            print(f"{color}{count}\033[0m", end=" ")
        print()


def main():
    filename = 'availability.txt'
    availabilityData = processAvailability(filename)
    displayAvailability(availabilityData)


if __name__ == "__main__":
    main()


