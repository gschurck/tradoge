package utils

import (
	"fmt"
	"io"
	"log"
	"math"
	"os"
	"strconv"
)

func ParseFloat(s string) float64 {
	f, err := strconv.ParseFloat(s, 64)
	if err != nil {
		log.Fatalf("Failed to parse float %s: %v", s, err)
	}
	return f
}

func RoundDown(f float64) int {
	return int(math.Floor(f))
}

func CopyFile(src, dst string) error {
	sourceFile, err := os.Open(src)
	if err != nil {
		return fmt.Errorf("could not open source file: %w", err)
	}
	defer sourceFile.Close()

	destFile, err := os.Create(dst)
	if err != nil {
		return fmt.Errorf("could not create destination file: %w", err)
	}
	defer destFile.Close()

	_, err = io.Copy(destFile, sourceFile)
	if err != nil {
		return fmt.Errorf("could not copy file: %w", err)
	}

	return nil
}
