package utils

import (
	"log"
	"math"
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
