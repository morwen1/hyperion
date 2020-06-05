package main

func InBool(slice []string, item string) bool {
	//busqueda lineal sencilla
	r := false

	for _, val := range slice {
		if val == item {
			r = true
		}
	}
	return r
}

/*

func FormatQty(qtyBtc int32 ) string {



}*/
