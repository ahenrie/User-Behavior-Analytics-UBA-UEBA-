package logparse

import (
	"bufio"
	"fmt"
	"os"
	"regexp"
)

func getUsers(logLine string) string {
	// Pattern for username in logs
	pattern := `User Name:#011(\w+)`

	// Compile the regex
	re := regexp.MustCompile(pattern)

	// Find the first match (returns slice of slices)
	matches := re.FindStringSubmatch(logLine)

	// Check if a match was found and return the captured username
	if len(matches) > 1 {
		return matches[1] // The second element is the captured group
	}

	// Return empty string if no match is found
	return ""
}

func ParseLogs() {
	if len(os.Args) < 2 {
		return
	}

	filePath := os.Args[1]
	file, err := os.Open(filePath)

	if err != nil {
		return
	}
	defer file.Close()

	//Map to hold users
	users := make(map[string]int)

	//Read line by line once the file is open
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		logLine := scanner.Text()
		fmt.Printf("Processing log line: %s", logLine)
		users[getUsers(logLine)]++
	}
}
