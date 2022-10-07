package main

import (
	"context"
	"fmt"
	"net/http"
	"os"
	"time"

	"cloud.google.com/go/firestore"

	"github.com/gin-gonic/gin"
	"github.com/penglongli/gin-metrics/ginmetrics"
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

	g := genRouter(ctx, client)

	forProm := gin.Default()
	prom := ginmetrics.GetMonitor()

	gaugeMetric := &ginmetrics.Metric{
		Type:        ginmetrics.Gauge,
		Name:        "something_new",
		Description: "This is the something new",
		Labels:      []string{"label1"},
	}
	/* try adding custom metrics */
	prom.AddMetric(gaugeMetric)
	prom.GetMetric("something_new").Add([]string{"label1_value1"}, 0.1)
	prom.GetMetric("something_new").Add([]string{"label1_value1"}, 0.082)

	prom.SetMetricPath("/metrics")
	prom.SetSlowTime(10)
	prom.UseWithoutExposingEndpoint(g)
	prom.SetDuration([]float64{0.1, 0.3, 1, 2, 5, 10})
	prom.Expose(forProm)

	go func() {
		forProm.Run(":8000")
	}()

	if portNumber == "" {
		portNumber = "8080"
	}

	portNumber = fmt.Sprintf(":%s", portNumber)

	_ = g.Run(portNumber)
}

func genRouter(ctx context.Context, client *firestore.Client) *gin.Engine {

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
				Str("method", c.Request.Method).
				Str("remote_addr", c.Request.RemoteAddr).
				Str("user_agent", c.Request.UserAgent()).
				Int64("process_time", difftime.Milliseconds()).
				Send()
		}

		c.JSON(httpStatus, responseData)

	})

	return g

}
