import plotly.graph_objects as go


def animated_chart(data):
    fig = go.Figure(data=[go.Histogram(x=data[0], name='hist')])

    frames = [go.Frame(data=[go.Histogram(x=d, name='hist')]) for d in data]

    fig.frames = frames

    fig.update_layout(updatemenus=[dict(type='buttons', showactive=False, buttons=[dict(label='Play', method='animate',
                                                                                        args=[None, {
                                                                                            'frame': {'duration': 200,
                                                                                                      'redraw': True},
                                                                                            'fromcurrent': True,
                                                                                            'transition': {
                                                                                                'duration': 200}}])])])

    fig.show()
