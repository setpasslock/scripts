package main

import (
	"flag"
	"fmt"
	"os"
	"path/filepath"
	"regexp"
)

const IPRegex = `(\d{1,3}\.){3}\d{1,3}`

func printIPPatterns(text string) {
	re := regexp.MustCompile(IPRegex)
	ipPatterns := re.FindAllString(text, -1)

	for _, ip := range ipPatterns {
		fmt.Println(ip)
	}
}

func main() {
	fileFlag := flag.String("f", "", "File path")
	dirFlag := flag.String("d", "", "Directory path")
	patternFlag := flag.String("p", "", "Pattern: ip,")

	flag.Parse()

	if *fileFlag != "" && *patternFlag != "" {
		filePath := *fileFlag
		content, err := os.ReadFile(filePath)
		if err != nil {
			fmt.Println("Error reading file:", err)
			return
		}

		if *patternFlag == "ip" {
			printIPPatterns(string(content))
		}

	}

	if *dirFlag != "" && *patternFlag != "" {
		dirPath := *dirFlag

		files, err := os.ReadDir(dirPath)
		if err != nil {
			fmt.Println("Error reading directory:", err)
			return
		}

		for _, file := range files {
			if !file.IsDir() {
				filePath := filepath.Join(dirPath, file.Name())
				content, err := os.ReadFile(filePath)
				if err != nil {
					fmt.Printf("Error reading file %s: %v\n", file.Name(), err)
					continue
				}

				if *patternFlag == "ip" {
					fmt.Printf("IP patterns in file %s:\n", file.Name())
					printIPPatterns(string(content))
					fmt.Println()

				}

			}
		}
	}
}
