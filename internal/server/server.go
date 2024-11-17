package server

import (
	"fmt"
	"html/template"
	"log"
	"net/http"
)

func handler(w http.ResponseWriter, r *http.Request) {
	tmpl, err := template.ParseFiles("web/templates/base.gohtml", "web/templates/index.gohtml")
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	err = tmpl.ExecuteTemplate(w, "base.gohtml", nil)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
	}
}

func addExchangeHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method == http.MethodPost {
		// Parse the form data
		err := r.ParseForm()
		if err != nil {
			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}

		// Access the data
		apiKey := r.Form.Get("api-key")
		apiSecret := r.Form.Get("api-secret")
		fmt.Println("API Key:", apiKey)
		fmt.Println("API Secret:", apiSecret)

	} else {
		tmpl, err := template.ParseFiles("web/templates/base.gohtml", "web/templates/add-exchange-account.gohtml")
		if err != nil {
			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}
		err = tmpl.ExecuteTemplate(w, "base.gohtml", nil)
		if err != nil {
			http.Error(w, err.Error(), http.StatusInternalServerError)
		}
	}
}

func StartServer() {
	http.HandleFunc("/", handler)
	http.HandleFunc("/add-exchange-account", addExchangeHandler)
	log.Fatal(http.ListenAndServe(":8063", nil))
}
