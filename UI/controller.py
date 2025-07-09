import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handle_graph(self, e):
        anno = self._view._ddyear.value
        brand = self._view._ddbrand.value
        if anno is None or brand is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Attenzione, selezionare tutti i parametri!", color="red"))
            self._view.update_page()
        self._model.buildGraph(anno, brand)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Grafo correttamente creato", color="green"))
        nNodes, nEdges = self._model.getGraphDetails()
        self._view.txt_result.controls.append(ft.Text(f"Numero di nodi: {nNodes}, numero di archi {nEdges}"))
        top3 = self._model.bestNodes()
        self._view.txt_result.controls.append(ft.Text(f"I top 3 archi sono:"))
        for edge in top3:
            self._view.txt_result.controls.append(ft.Text(f"Prodotto 1: {edge[0].Product_number}, prodotto 2: {edge[1].Product_number}, con peso {edge[2]["weight"]}"))
            print(edge)
        self._view.txt_result.controls.append(ft.Text(f"I nodi che si trovano in più di un arco sono:"))
        ripetuti = self._model.getRipetuti()
        for node in ripetuti:
            self._view.txt_result.controls.append(ft.Text(node))
        self._view.update_page()

    def handle_search(self, e):
        pass

    def fillDDYear(self):
        years = self._model.getYears()
        for y in years:
            self._view._ddyear.options.append(ft.dropdown.Option(y))

    def fillDDBrands(self):
        brands = self._model.getBrands()
        for b in brands:
            self._view._ddbrand.options.append(ft.dropdown.Option(b))