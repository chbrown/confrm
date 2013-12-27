package main

import (
  "fmt"
  "log"
  // "io/ioutil"
  "net/http"
  // "regexp"
  "github.com/monnand/goredis"
  "github.com/coopernurse/gorp"
  _ "github.com/bmizerany/pq" // for PostgreSQL support
  "database/sql"
  "html/template"
)

var client goredis.Client

// import redis as redis_lib
// redis = redis_lib.StrictRedis()

func rootHandler(w http.ResponseWriter, req *http.Request) {
    // page_re, _ := regexp.Compile("/view/(\\w+)")
    // page_title := page_re.FindStringSubmatch(req.URL.Path)[1]
    // page, _ := loadPage(page_title)
    fmt.Fprintf(w, "<h1>" + "Hey!" + "</h1><p>" + req.Header.Get("REMOTE_ADDR") + "</p>")
}

func wrapLogger(handler http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        log.Printf("%s %s %s", r.RemoteAddr, r.Method, r.URL)
        handler.ServeHTTP(w, r)
    })
}

func fileHandler(w http.ResponseWriter, req *http.Request) {  {

}

func main() {
    db, err := sql.Open("postgres", "dbname=confrm_dev sslmode=disable")
    if err != nil {
      fmt.Println("Error opening database!", err)
    }
    dbmap := &gorp.DbMap{Db: db}

    fmt.Println("dbmap", dbmap)

    // http.Handle("/static/", wrapLogger(http.StripPrefix("/static", http.FileServer(http.Dir("./static")))))
    http.Handle("/static/", wrapLogger(http.FileServer(http.Dir("."))))
    http.HandleFunc("/files/", fileHandler)
    http.HandleFunc("/users/", userHandler)
    http.HandleFunc("/groups/", groupHandler)
    http.HandleFunc("/", rootHandler)
    http.ListenAndServe(":8089", nil)
}
