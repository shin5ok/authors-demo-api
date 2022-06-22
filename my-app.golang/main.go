package main

import (
	"context"
	"fmt"
	"net/http"
	"os"
	"time"

	"cloud.google.com/go/firestore"

	"github.com/gin-gonic/gin"
	"github.com/rs/zerolog"
	log "github.com/rs/zerolog/log"
)

var projectID = os.Getenv("PROJECT")
var portNumber = os.Getenv("PORT")

func init() {
	log.Logger = zerolog.New(os.Stderr).With().Timestamp().Logger()
	zerolog.LevelFieldName = "severity"
	zerolog.TimestampFieldName = "timestamp"
	zerolog.TimeFieldFormat = time.RFC3339Nano
}

func main() {
	ctx := context.Background()
	client, _ := firestore.NewClient(ctx, projectID)

	g := gin.Default()

	g.GET("/", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{"ping": "pong"})
	})

	g.GET("/api/author/:u", func(c *gin.Context) {
		start := time.Now()
		username := c.Param("u")
		/* trick to get just one record */
		query := client.Collection("authors").Where("username", "==", username).Limit(1)
		itr := query.Documents(ctx)
		defer itr.Stop()

		snap, err := itr.Next()

		var responseData = gin.H{}
		var httpStatus = http.StatusNotFound

		if err == nil {
			responseData = snap.Data()
			httpStatus = http.StatusOK
			finish := time.Now()
			difftime := finish.Sub(start)
			log.Info().
				Str("path", c.Request.URL.Path).
				Str("host", c.Request.Host).
				Str("remote_addr", c.Request.RemoteAddr).
				Str("user_agent", c.Request.UserAgent()).
				Int64("process_time", difftime.Milliseconds()).
				Send()
		}

		c.JSON(httpStatus, responseData)

	})

	if portNumber == "" {
		portNumber = "8080"
	}

	portNumber = fmt.Sprintf(":%s", portNumber)

	g.Run(portNumber)
}
