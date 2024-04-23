package main

import (
	"flag"
	"fmt"
	"os"
	"path/filepath"
	"regexp"
	"strings"

	"github.com/gabriel-vasile/mimetype"
)

const IPRegex = `(\d{1,3}\.){3}\d{1,3}`

// unstable
const domainRegex = `^(https?://)?([a-zA-Z0-9\-_]+\.)+[a-zA-Z]{2,}(:\d+)?(/.*)?`

func printIPPatterns(text string, filePath string) {
	re := regexp.MustCompile(IPRegex)
	ipPatterns := re.FindAllString(text, -1)

	for _, ip := range ipPatterns {
		fmt.Println(ip, "<--", filePath)
	}
}

func printDomainPatterns(text string, filePath string) {
	re := regexp.MustCompile(domainRegex)
	domainPatterns := re.FindAllString(text, -1)

	for _, domain := range domainPatterns {
		fmt.Println(domain, "<--", filePath)
	}
}

func checkFileType(filePath string) bool {
	mtype, err := mimetype.DetectFile(filePath)
	mtype_s := mtype.String()
	prefix := "text"

	if err != nil {
		return false
	}
	if strings.HasPrefix(mtype_s, prefix) {
		return true

	} else {
		return false
	}

}

func processDirectory(dirPath string, patternFlag string) error {
	files, err := os.ReadDir(dirPath)
	if err != nil {
		return fmt.Errorf("Error reading directory %s: %v", dirPath, err)
	}

	for _, file := range files {
		filePath := filepath.Join(dirPath, file.Name())

		if file.IsDir() {
			err := processDirectory(filePath, patternFlag)
			if err != nil {
				fmt.Println("Error processing directory:", err)
			}
		} else {
			isPlainText := checkFileType(filePath)
			if isPlainText {
				content, err := os.ReadFile(filePath)
				if err != nil {
					fmt.Printf("Error reading file %s: %v\n", file.Name(), err)
					continue
				}

				if patternFlag == "ip" {
					// fmt.Printf("IP patterns in file %s:\n", file.Name())
					go printIPPatterns(string(content), file.Name())
					fmt.Println()

				} else if patternFlag == "domain" {
					// fmt.Printf("Domain patterns in file %s:\n", file.Name())
					go printDomainPatterns(string(content), file.Name())
					fmt.Println()
				}
			}
		}
	}
	return nil
}

func main() {
	fileFlag := flag.String("f", "", "File path")
	dirFlag := flag.String("d", "", "Directory path")
	patternFlag := flag.String("p", "", "Pattern: ip,")
	file_name := ""

	flag.Parse()

	if *fileFlag != "" && *patternFlag != "" {
		filePath := *fileFlag

		content, err := os.ReadFile(filePath)
		if err != nil {
			fmt.Println("Error reading file:", err)
			return
		}

		if *patternFlag == "ip" {
			printIPPatterns(string(content), file_name)
		} else if *patternFlag == "domain" {
			printDomainPatterns(string(content), file_name)
		}

	}

	if *dirFlag != "" && *patternFlag != "" {
		dirPath := *dirFlag
		processDirectory(dirPath, *patternFlag)

	}
}
