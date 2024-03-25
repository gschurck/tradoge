package main

type viperConfig struct {
	TwitterAuthToken string
	Exchanges        []struct {
		Name     string
		User     string
		Password string
	}
}
