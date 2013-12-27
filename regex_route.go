type route struct {
        re *regexp.Regexp
        handler func(http.ResponseWriter, *http.Request, []string)
}

type RegexpHandler struct {
        routes []*route
}

func (h *RegexpHandler) AddRoute(re string, handler
func(http.ResponseWriter, *http.Request, []string)) {
        r := &route{regexp.MustCompile(re), handler}
        h.routes = append(h.routes, r)
}

func (h *RegexpHandler) ServeHTTP(rw http.ResponseWriter, r *Request) {
        for _, route := range h.routes {
                matches := route.re.FindStringSubmatch(r.RawURL)
                if matches != nil {
                        route.handler(rw, r, matches)
                        break
                }
        }
}

For your case, you can do something like:

reHandler := new(RegexpHandler)
reHandler.AddRoute("/people/[0-9]+/edit$", peopleEditHandler)
http.ListenAndServe(":8080", reHandler)