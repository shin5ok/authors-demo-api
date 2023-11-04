package main

import (
	"context"
	"fmt"
	"log/slog"
	"net/http"
	"os"
	"time"

	"cloud.google.com/go/firestore"

	"github.com/gin-gonic/gin"
	"github.com/penglongli/gin-metrics/ginmetrics"
)

var (
	projectID      = os.Getenv("PROJECT")
	servicePort    = os.Getenv("PORT")
	promPort       = os.Getenv("PROM_PORT")
	collectionName = os.Getenv("COLLECTION")
	logger         *slog.Logger
)

func init() {

	replace := func(groups []string, a slog.Attr) slog.Attr {
		if a.Key == slog.LevelKey && a.Value.String() == slog.LevelWarn.String() {
			return slog.String("severity", "WARNING")
		}
		if a.Key == "level" {
			return slog.String("severity", a.Value.String())
		}
		if a.Key == "msg" {
			return slog.String("message", a.Value.String())
		}
		return a
	}

	options := slog.HandlerOptions{
		Level:     slog.LevelInfo,
		AddSource: true, ReplaceAttr: replace,
	}

	logger = slog.New(slog.NewJSONHandler(os.Stdout, &options))
	slog.SetDefault(logger)

	if collectionName == "" {
		collectionName = "authors"
	}

	if servicePort == "" {
		servicePort = "8080"
	}

	if promPort == "" {
		promPort = "10080"
	}

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
		forProm.Run(":" + promPort)
	}()

	var portNumber = fmt.Sprintf(":%s", servicePort)

	if err := g.Run(portNumber); err != nil {
		panic(err)
	}
}

func genRouter(ctx context.Context, client *firestore.Client) *gin.Engine {

	g := gin.Default()

	g.GET("/", func(c *gin.Context) {
		logger.Info("GET to /")
		c.JSON(http.StatusOK, gin.H{"ping": "pong"})
	})

	g.GET("/api/author/:u", func(c *gin.Context) {
		start := time.Now()
		username := c.Param("u")

		var responseData = gin.H{}
		var httpStatus = http.StatusNotFound

		snap, err := client.Collection(collectionName).Doc(username).Get(c)
		if err != nil {
			logger.Error(err.Error())
		}

		if err == nil {
			responseData = snap.Data()
			httpStatus = http.StatusOK
			finish := time.Now()
			difftime := finish.Sub(start)
			logger.Info(
				"/api/author/:u",
				"path", c.Request.URL.Path,
				"host", c.Request.Host,
				"method", c.Request.Method,
				"remote_addr", c.Request.RemoteAddr,
				"user_agent", c.Request.UserAgent(),
				"process_time", difftime.Milliseconds(),
			)
		}

		c.JSON(httpStatus, responseData)

	})

	return g

}
