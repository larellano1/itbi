from instrumental_functions import *


df = carrega_dados_uso()
fig = px.scatter(df, x='Área Construída (m2)', y='Valor de Transação (declarado pelo contribuinte)', color='ACC (IPTU)')




app = Dash(__name__)



app.layout = html.Div([
    html.H1("Quanto vale o meu apê?"),
    html.Div(children=[
    html.Div(children=[
        html.Div(children=[
            html.H2("Filtros:"),
            html.Span("Bairro:", style={'padding': '10px'}),
            dcc.Input(id='input-bairro')
        ]),
        html.Div(children=[
            html.H2(f"Análise das transações:"),
            dcc.Graph(figure=fig),
            html.H2("Transações na região:"),
            dash_table.DataTable(df.to_dict('records'), 
                            columns=[{'name': i, 'id': j, 'type':'numeric', 'format':dash_table.FormatTemplate.money(2)} if i == 'Valor Declarado' 
                                                                                                                        else {'name': i, 'id': j} for i, j in zip(['Rua','Número','Complemento','CEP','Data','Terreno(m2)','Apartamento (m2)','Ano de Construção','Valor Declarado'],
                                                                                                                                                                    ['Nome do Logradouro','Número','Complemento','CEP', 'Data de Transação','Área do Terreno (m2)','Área Construída (m2)', 'ACC (IPTU)', 'Valor de Transação (declarado pelo contribuinte)'])],
                            filter_action="native",
                            sort_action="native",
                            sort_mode="multi",)
        ], id='output-bairro')
    ],
    style={'padding': '30px'}),
    ])
    ])

@app.callback(
    Output('output-bairro','children'),
    Input('input-bairro','value')
)
def cb_render(val):
    data = df[(df['Bairro'] == val.upper())][['Nome do Logradouro','Número','Complemento',
    'CEP', 'Data de Transação','Área do Terreno (m2)',
    'Área Construída (m2)', 'ACC (IPTU)', 'Valor de Transação (declarado pelo contribuinte)']]
    fig = px.scatter(data, x='Área Construída (m2)', y='Valor de Transação (declarado pelo contribuinte)', color='ACC (IPTU)')
    html_children = [
            html.H2(f"Análise das transações na região de {val.upper()}:"),
            dcc.Graph(figure=fig),
            html.H2(f"Transações na região de {val.upper()}:"),
            dash_table.DataTable(data.to_dict('records'), 
                            columns=[{'name': i, 'id': j, 'type':'numeric', 'format':dash_table.FormatTemplate.money(2)} if i == 'Valor Declarado' 
                                                                                                                        else {'name': i, 'id': j} for i, j in zip(['Rua','Número','Complemento','CEP','Data','Terreno(m2)','Apartamento (m2)','Ano de Construção','Valor Declarado'],
                                                                                                                                                                    ['Nome do Logradouro','Número','Complemento','CEP', 'Data de Transação','Área do Terreno (m2)','Área Construída (m2)', 'ACC (IPTU)', 'Valor de Transação (declarado pelo contribuinte)'])],
                            filter_action="native",
                            sort_action="native",
                            sort_mode="multi",)
        ]
    return html_children


if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False) 