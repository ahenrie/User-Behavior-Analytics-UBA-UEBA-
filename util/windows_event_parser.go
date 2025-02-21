package util

import (
	"bufio"
	"encoding/csv"
	"fmt"
	"log"
	"os"
	"regexp"
	"strings"
	"time"
)

// Extract username from logs
func getUsers(logLine string) string {
	pattern := `User Name:#011(\w+)`
	re := regexp.MustCompile(pattern)
	matches := re.FindStringSubmatch(logLine)
	if len(matches) > 1 {
		return matches[1]
	}
	return "System"
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

// Extract EventID from logs
func getEventID(logLine string) string {
	pattern := `\[(\d+)\]`
	re := regexp.MustCompile(pattern)
	matches := re.FindStringSubmatch(logLine)
	if len(matches) > 1 {
		return matches[1]
	}
	return "Null"
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
		getEventID(logLine),
		getUsers(logLine),
		getServiceName(logLine),
		getLogMessage(logLine),
	}
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
	header := []string{"Timestamp", "Hostname", "EventID", "User", "ServiceName", "Message"}
	writer.Write(header)

	// Read and process log lines
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		logLine := scanner.Text()
		features := extractFeatures(logLine)
		writer.Write(features)
	}

	if err := scanner.Err(); err != nil {
		log.Fatal("Error reading log file:", err)
	}

	fmt.Println("Log parsing complete. CSV saved as logs_parsed.csv")
}
