import nextcord

color = 0xFF6500
key_features = {
    'temp' : 'Temperature',
    'feels_like' : 'Feels Like',
    'temp_min' : 'Minimum Temperature',
    'temp_max' : 'Maximum Temperature',
    'humidity' : 'Humidity in %',
    'pressure' : 'Pressure in mbars'
}

def parse_data(data):
    return data

def weather_message(data, location):
    location = location.title()
    message = nextcord.Embed(
        color=color
    )
    message.set_author(name=f'Weather in {location}', icon_url='https://media.discordapp.net/attachments/887755071885045810/974341847344369694/8ce446f0e6f6e99dac3494b9b113c601.gif')
    message.set_thumbnail(url="https://i.pinimg.com/originals/0e/f3/bb/0ef3bb66d9216fffcea9022628f7bb26.gif")
    for key in data:
        message.add_field(
            name=key_features[key],
            value=str(data[key]),
            inline=False
        )
    return message

def error_message(location):
    location = location.title()
    return nextcord.Embed(
        title='Error',
        description=f'There was an error retrieving weather data for {location}.',
        color=color
    )
