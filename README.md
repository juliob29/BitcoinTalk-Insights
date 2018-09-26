# BitcoinTalk Insights
![Coverage](https://img.shields.io/badge/coverage-96%25-green.svg?style=flat-square)

This Bertie.ai skill adds cryptocurrency suggestions to the Insights Bar on Bertie. 
The skill sifts through titles written by the user, and detects if there are
cryptocurrencies mentioned. With this information, Bertie finds coins related 
to the cryptocurrencies that the author writes about, and suggests them in the 
`hover` section on the insights bar.

This Bertie.ai skill also uses a database, containing all of the messages from 
the popular forum [BitcoinTalk](https://bitcointalk.org/) The database is used to train a Word2Vec model,
which allows us to know related coins to a found cryptocurrency, based on the last
week of forum messages.Related Cryptocurrencies are also shown, which come from the forum 'BitcoinTalk'. 
A Word2Vec model is trained to find words most similar to the currency found.

# Usage

This application contains a total of 3 docker containers - the scraper, the scraper's database, and the main `BitcoinTalk-Insights` application. To initialize all 3 containers, we use a `docker-compose.yml` file. 

The application can be be built by using: `VERSION=v.[version] docker-compose build` and `VERSION=v.[version] docker-compose up -d`. The environment variables required for the application are located in the .env file in the repository. They include a plotly username and API_Key, the `POSTGRES_URI` for the database, a `MODELS_PATH` for the application to look for particular Word2Vec models, and a `BOARD_ID` and `WAIT_TIME` to configure the scraper.  

### Endpoints
This application contains one relevant endpoint:

* `/detect`: which returns the found Cryptocurrencies in text, their location, close prices, and Plotly graph.

That endpoint takes the following parameters:

* `text`: text input.
* `limit`: integer input. (Default is 3)

All requests have to be made using `POST` and passing a JSON object with the key above.

### Example Response
The skill returns a response in the following format.

```json
{
    "success": true,
    "message": "Searched `text` data successfully.",
    "results": [
        {
            "title": "See the latest conversation about Litecoin on bitcointalk.org",
            "entities": [
                {
                    "name": "Litecoin",
                    "start": 34,
                    "end": 42,
                    "related": [
                        {
                            "name": "Ethereum",
                            "slug": "ethereum",
                            "value": 0.7644336247,
                            "url": "https://bitcointalk.org/index.php?topic=4930155.msg44421647#msg44421647"
                        },
                        {
                            "name": "Dogecoin",
                            "slug": "dogecoin",
                            "value": 0.7105858855,
                            "url": "https://bitcointalk.org/index.php?topic=1431367.msg43996859#msg43996859"
                        },
                        {
                            "name": "Monero",
                            "slug": "monero",
                            "value": 0.6657955171,
                            "url": "https://bitcointalk.org/index.php?topic=4882509.msg43990945#msg43990945"
                        },
                        {
                            "name": "XRP",
                            "slug": "ripple",
                            "value": 0.6058622511,
                            "url": "https://bitcointalk.org/index.php?topic=4930155.msg44421301#msg44421301"
                        },
                        {
                            "name": "Zcash",
                            "slug": "zcash",
                            "value": 0.603538287,
                            "url": "https://bitcointalk.org/index.php?topic=4845288.msg43856411#msg43856411"
                        },
                        {
                            "name": "Altcoin",
                            "slug": "altcoin-alt",
                            "value": 0.5301628541,
                            "url": "https://bitcointalk.org/index.php?topic=4930636.msg44423873#msg44423873"
                        },
                        {
                            "name": "DeepOnion",
                            "slug": "deeponion",
                            "value": 0.4435027239,
                            "url": "https://bitcointalk.org/index.php?topic=4892272.msg44116536#msg44116536"
                        },
                        {
                            "name": "TRON",
                            "slug": "tron",
                            "value": 0.4411762519,
                            "url": "https://bitcointalk.org/index.php?topic=4818153.msg43611071#msg43611071"
                        },
                        {
                            "name": "Vertcoin",
                            "slug": "vertcoin",
                            "value": 0.4282983802,
                            "url": "https://bitcointalk.org/index.php?topic=4792328.msg43242155#msg43242155"
                        },
                        {
                            "name": "Lisk",
                            "slug": "lisk",
                            "value": 0.4274601026,
                            "url": "https://bitcointalk.org/index.php?topic=4451471.msg42360533#msg42360533"
                        }
                    ]
                }
            ]
        }
    ]
}
```
