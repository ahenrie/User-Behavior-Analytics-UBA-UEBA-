package util

import (
	"bufio"
	"encoding/csv"
	"fmt"
	"log"
	"os"
	"regexp"
	"strconv"
	"strings"
	"time"
)

// Extract username from logs
func getUsers(logLine string) string {
	// Pattern for 'User Name:#011'
	pattern1 := `User Name:#011(\w+)`
	// Pattern for 'User: DESKTOP-RKJA15K\USERNAME'
	pattern2 := `User: \S+\\([^\s]+)`

	// Compile both regex patterns
	re1 := regexp.MustCompile(pattern1)
	re2 := regexp.MustCompile(pattern2)

	// Try matching the first pattern
	matches1 := re1.FindStringSubmatch(logLine)
	if len(matches1) > 1 {
		return matches1[1]
	}

	// Try matching the second pattern
	matches2 := re2.FindStringSubmatch(logLine)
	if len(matches2) > 1 {
		return matches2[1] // Return the username found in the second pattern
	}

	return "System" // Return "System" if no match is found
}

// Extract timestamp and convert to Unix time
func getTimestamp(logLine string) int64 {
	pattern := `^(\S+)`
	re := regexp.MustCompile(pattern)
	matches := re.FindStringSubmatch(logLine)
	if len(matches) > 1 {
		timestampStr := matches[1]
		layout := time.RFC3339Nano
		parsedTime, err := time.Parse(layout, timestampStr)
		if err != nil {
			log.Println("Error parsing timestamp:", err)
			return 0
		}
		return parsedTime.Unix()
	}
	return 0
}

func getProcessID(logLine string) int {
	pattern := `\[(\d+)\]`
	re := regexp.MustCompile(pattern)
	matches := re.FindStringSubmatch(logLine)
	if len(matches) > 1 {
		processID, err := strconv.Atoi(matches[1])
		if err == nil {
			return processID
		}
	}
	return 0
}

// Extract Service/Process Name
func getServiceName(logLine string) string {
	pattern := `(?:\S+\s+)([^\s\[\]]+)\[\d+\]`
	re := regexp.MustCompile(pattern)
	matches := re.FindStringSubmatch(logLine)
	if len(matches) > 1 {
		return matches[1]
	}
	return "Null"
}

// Extract Hostname
func getHostName(logLine string) string {
	pattern := `^\S+\s+(\S+)`
	re := regexp.MustCompile(pattern)
	matches := re.FindStringSubmatch(logLine)
	if len(matches) > 1 {
		return matches[1]
	}
	return "Null"
}

// Extract Log Message
func getLogMessage(logLine string) string {
	pattern := `\[\d+\]\s*(.*)`
	re := regexp.MustCompile(pattern)
	matches := re.FindStringSubmatch(logLine)
	if len(matches) > 1 {
		return strings.TrimSpace(matches[1])
	}
	return "Null"
}

// Convert log line into CSV-ready features
func extractFeatures(logLine string) []string {
	return []string{
		fmt.Sprintf("%d", getTimestamp(logLine)), // Unix Timestamp as string
		getHostName(logLine),
		fmt.Sprintf("%d", getProcessID(logLine)), // Convert to string
		getUsers(logLine),
		getServiceName(logLine),
		getLogMessage(logLine),
		getAppName(logLine),
	}
}

func getAppName(logLine string) string {
	// Pattern for extracting any executable name ending in .exe
	pattern := `Process '\\Device\\[^\s]+\\([^\\]+\.exe)'`
	re := regexp.MustCompile(pattern)

	// Find the match
	matches := re.FindStringSubmatch(logLine)

	if len(matches) > 1 {
		return matches[1] // Return the executable name (e.g., opera.exe)
	}

	// If no match, check for .exe elsewhere in the line
	// This looks for any word ending in .exe
	alternatePattern := `\b([^\s]+\.exe)\b`
	reAlt := regexp.MustCompile(alternatePattern)

	// Try to find the executable name elsewhere
	matchesAlt := reAlt.FindStringSubmatch(logLine)

	if len(matchesAlt) > 0 {
		return matchesAlt[0] // Return the executable name found elsewhere
	}

	return "Null" // Return default if no match is found
}

// Read logs and write extracted features to CSV
func ParseLogs() {
	if len(os.Args) < 2 {
		fmt.Println("Usage: go run main.go <log_file>")
		return
	}

	filePath := os.Args[1]
	file, err := os.Open(filePath)
	if err != nil {
		log.Fatal("Error opening log file:", err)
	}
	defer file.Close()

	// Open CSV file for writing
	csvFile, err := os.Create("logs_parsed.csv")
	if err != nil {
		log.Fatal("Error creating CSV file:", err)
	}
	defer csvFile.Close()

	writer := csv.NewWriter(csvFile)
	defer writer.Flush()

	// Write CSV header
	header := []string{"Timestamp", "Hostname", "EventID", "User", "ServiceName", "Message", "Exe"}
	writer.Write(header)

	// Read and process log lines
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		logLine := scanner.Text()

		// Test for a propper eventID
		if getProcessID(logLine) == 0 {
			continue
		}

		features := extractFeatures(logLine)
		writer.Write(features)
	}

	if err := scanner.Err(); err != nil {
		log.Fatal("Error reading log file:", err)
	}

	fmt.Println("Log parsing complete. CSV saved as logs_parsed.csv")
}
