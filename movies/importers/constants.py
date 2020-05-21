STUDIO_GHIBLI_API_BASE_URL = 'https://ghibliapi.herokuapp.com'
STUDIO_GHIBLI_API_FILMS_URL = f'{STUDIO_GHIBLI_API_BASE_URL}/films'
STUDIO_GHIBLI_API_PEOPLE_URL = f'{STUDIO_GHIBLI_API_BASE_URL}/people'

MOVIES_DATA_CACHE_KEY = 'movies.movies_data'
MOVIES_DATA_CACHE_TTL = 60  # 1 minute

# Backup used in case something goes wrong with importing data
MOVIES_DATA_BACKUP_CACHE_KEY = 'movies.movies_data.backup'
MOVIES_DATA_BACKUP_CACHE_TTL = 60 * 60 * 24  # 24 hours
