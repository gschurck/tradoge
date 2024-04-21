package logger

import (
	"io"
	"log"
	"os"
)

//var (
//	Log *log.Logger
//)

func SetupLogger() {
	logFile, err := os.OpenFile("data/logs.txt", os.O_CREATE|os.O_WRONLY|os.O_APPEND, 0666)
	if err != nil {
		log.Fatal(err)
	}

	// Create a multi writer
	multi := io.MultiWriter(os.Stdout, logFile)
	//Log = log.New(multi, "", log.LstdFlags)
	//Log.Println("Logger initialized")

	// Set the output of the default logger
	log.SetOutput(multi)

	// Set the prefix and flags of the default logger
	log.SetFlags(log.LstdFlags)
}
