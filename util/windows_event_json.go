package util

import (
	"bufio"
	"encoding/csv"
	"encoding/json"
	"fmt"
	"os"
	"regexp"
	"strings"
	"time"
)

// LogEntry represents a single parsed log entry
type LogEntry struct {
	EventTime         string `json:"EventTime"`
	EventReceivedTime string `json:"EventReceivedTime"`
	Hostname          string `json:"Hostname"`
	Keywords          int64  `json:"Keywords"`
	EventType         string `json:"EventType"`
	SeverityValue     int    `json:"SeverityValue"`
	Severity          string `json:"Severity"`
	EventID           int    `json:"EventID"`
	SourceName        string `json:"SourceName"`
	ProviderGuid      string `json:"ProviderGuid"`
	Version           int    `json:"Version"`
	Task              int    `json:"Task"`
	OpcodeValue       int    `json:"OpcodeValue"`
	RecordNumber      int    `json:"RecordNumber"`
	ProcessID         int    `json:"ProcessID"`
	ThreadID          int    `json:"ThreadID"`
	Channel           string `json:"Channel"`
	Domain            string `json:"Domain"`
	AccountName       string `json:"AccountName"`
	UserID            string `json:"UserID"`
	AccountType       string `json:"AccountType"`
	LogonType         string `json:"LogonType,omitempty"`
	IpAddress         string `json:"IpAddress,omitempty"`
	IpPort            string `json:"IpPort,omitempty"`
	DeviceInstanceId  string `json:"DeviceInstanceId,omitempty"`
	DeviceCount       string `json:"DeviceCount,omitempty"`
	Message           string `json:"Message"`
	Opcode            string `json:"Opcode"`
	PackageFullName   string `json:"PackageFullName,omitempty"`
	AppUserModelId    string `json:"AppUserModelId,omitempty"`
	AppSettings       string `json:"AppSettings,omitempty"`
	FunctionName      string `json:"FunctionName,omitempty"`
	ErrorCode         string `json:"ErrorCode,omitempty"`
	SourceModuleName  string `json:"SourceModuleName"`
	SourceModuleType  string `json:"SourceModuleType"`
}

// parseJSONLog converts a JSON string into a LogEntry struct
func parseJSONLog(jsonStr string) (*LogEntry, error) {
	var entry LogEntry
	err := json.Unmarshal([]byte(jsonStr), &entry)
	if err != nil {
		return nil, err
	}
	return &entry, nil
}

// extractTimestampFeatures extracts structured time features
func extractTimestampFeatures(timestamp string) (string, string, string, string) {
	t, err := time.Parse("2006-01-02 15:04:05", timestamp)
	if err != nil {
		return "", "", "", ""
	}
	return t.Format("2006-01-02"), t.Format("15"), t.Format("Monday"), t.Format("2006-01")
}

// cleanMessage removes special characters from the log message
func cleanMessage(msg string) string {
	re := regexp.MustCompile(`[\r\n\t]+`)
	return re.ReplaceAllString(strings.TrimSpace(msg), " ")
}

// writeToCSV writes logs to a CSV file
func writeToCSV(logs []LogEntry, outputFile string) error {
	file, err := os.Create(outputFile)
	if err != nil {
		return err
	}
	defer file.Close()

	writer := csv.NewWriter(file)
	defer writer.Flush()

	// Define CSV headers
	headers := []string{
		"EventTime", "EventReceivedTime", "Date", "Hour", "DayOfWeek", "MonthYear",
		"Hostname", "Keywords", "EventType", "SeverityValue", "Severity",
		"EventID", "SourceName", "ProviderGuid", "Version", "Task",
		"OpcodeValue", "RecordNumber", "ProcessID", "ThreadID", "Channel",
		"Domain", "AccountName", "UserID", "AccountType", "LogonType",
		"IpAddress", "IpPort", "DeviceInstanceId", "DeviceCount",
		"Opcode", "PackageFullName", "AppUserModelId", "AppSettings",
		"FunctionName", "ErrorCode", "SourceModuleName", "SourceModuleType",
		"Message",
	}

	// Write header row
	writer.Write(headers)

	// Write log data
	for _, log := range logs {
		date, hour, dayOfWeek, monthYear := extractTimestampFeatures(log.EventTime)

		record := []string{
			log.EventTime, log.EventReceivedTime, date, hour, dayOfWeek, monthYear,
			log.Hostname, fmt.Sprintf("%d", log.Keywords), log.EventType,
			fmt.Sprintf("%d", log.SeverityValue), log.Severity,
			fmt.Sprintf("%d", log.EventID), log.SourceName, log.ProviderGuid,
			fmt.Sprintf("%d", log.Version), fmt.Sprintf("%d", log.Task),
			fmt.Sprintf("%d", log.OpcodeValue), fmt.Sprintf("%d", log.RecordNumber),
			fmt.Sprintf("%d", log.ProcessID), fmt.Sprintf("%d", log.ThreadID),
			log.Channel, log.Domain, log.AccountName, log.UserID, log.AccountType,
			log.LogonType, log.IpAddress, log.IpPort, log.DeviceInstanceId, log.DeviceCount,
			log.Opcode, log.PackageFullName, log.AppUserModelId, log.AppSettings,
			log.FunctionName, log.ErrorCode, log.SourceModuleName, log.SourceModuleType,
			cleanMessage(log.Message),
		}

		writer.Write(record)
	}

	fmt.Println("CSV file successfully created:", outputFile)
	return nil
}

// ProcessLogFile reads a log file, parses JSON, and writes CSV
func ProcessLogFile(inputFile, outputFile string) error {
	file, err := os.Open(inputFile)
	if err != nil {
		return err
	}
	defer file.Close()

	var logs []LogEntry

	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := scanner.Text()

		// Extract JSON part of the log line (after the IP address)
		parts := strings.SplitN(line, " ", 3)
		if len(parts) < 3 {
			continue
		}
		jsonPart := parts[2]

		// Remove trailing '#015' (carriage return issue)
		jsonPart = strings.TrimSuffix(jsonPart, "#015")

		// Parse JSON log entry
		entry, err := parseJSONLog(jsonPart)
		if err != nil {
			fmt.Println("Error parsing JSON:", err)
			continue
		}
		logs = append(logs, *entry)
	}

	if err := scanner.Err(); err != nil {
		return err
	}

	// Write logs to CSV
	return writeToCSV(logs, outputFile)
}
