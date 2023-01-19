import plotly.graph_objs as go
from plotly.subplots import make_subplots


def total_capacity_allocated(route_space):
    # search all the two nodes paths
    res = list(route_space[0].index)
    zeros_list = []
    list_of_path = []
    for a in res:
        if len(a) == 4:
            list_of_path.append(a)

    for df in route_space:
        zeros_count = [df.loc[path].eq(0).sum() for path in list_of_path]
        zeros_list.append(zeros_count)



    # Create a subplot with one x-axis and one y-axis
    fig = make_subplots(rows=1, cols=1)

    # Add a bar trace to the subplot
    fig.add_trace(go.Bar(x=list_of_path, y=zeros_list[0], name="Frame 1"))

    # Update the layout to include a title and axis labels
    fig.update_layout(title='Total capacity allocated into the network',
                      yaxis_title='Total channels allocated',
                      xaxis_title='Line')

    # Create a list of frames for the animation
    frames = [go.Frame(data=[go.Bar(x=list_of_path, y=zeros_list[i], name="Frame {}".format(i + 1))]) for i in
              range(1, len(zeros_list))]

    # Add the frames to the figure
    fig.frames = frames

    # Define the animation settings
    animation_settings = dict(frame=dict(duration=500, redraw=True), fromcurrent=True)

    # Update the layout to include the animation settings
    fig.update_layout(updatemenus=[dict(type='buttons', showactive=False, buttons=[dict(label='Play',
                                                                                        method='animate', args=[None,
                                                                                                                animation_settings])])])

    # Show the figure
    fig.show()
