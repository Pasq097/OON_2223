import plotly.graph_objects as go

def allocation_per_link_animated(mtrx_start, mtrx_fin):
    res = []
    for mtrx in mtrx_fin:
        result = {}
        for key, value in mtrx_start.items():
            result[key] = {}
            for sub_key, sub_value in value.items():
                result[key][sub_key] = mtrx_start[key][sub_key] - mtrx[key][sub_key]
        res.append(result)
    new_dictionary_2 = [{str((k, k1)): v1 for k, v in d.items() for k1, v1 in v.items()} for d in res]
    new_dictionary = {str((k, k1)): v1 for k, v in mtrx_start.items() for k1, v1 in v.items()}
    print(new_dictionary)
    print(new_dictionary_2)
    print(len(new_dictionary_2))
    frames = [go.Frame(
        data=[go.Bar(x=list(new_dictionary_2.keys()), y=list(new_dictionary_2.values()), name='mtrx_start'),
              go.Bar(x=list(new_dictionary.keys()), y=list(new_dictionary.values()), name='mtrx_fin')])]

    fig = go.Figure(data=[go.Bar(x=list(new_dictionary_2.keys()), y=list(new_dictionary_2.values()), name='mtrx_start'),
                          go.Bar(x=list(new_dictionary.keys()), y=list(new_dictionary.values()), name='result')],
                    layout=go.Layout(updatemenus=[
                        dict(type='buttons', showactive=False, buttons=[dict(label='Play', method='animate',
                                                                             args=[None, {'frame': {'duration': 200,
                                                                                                    'redraw': True},
                                                                                          'fromcurrent': True,
                                                                                          'transition': {
                                                                                              'duration': 200}}])])]))
    fig.frames = frames
    fig.show()
